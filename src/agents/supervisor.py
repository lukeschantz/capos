"""
Supervisor Agent for VC Digital Twin multi-agent system.

The Supervisor coordinates all worker agents, making routing decisions and
synthesizing findings to guide the investment evaluation workflow.
"""

import os
import json
from typing import Literal, Optional
from datetime import datetime

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langgraph.types import Command
from pydantic import BaseModel, Field

from src.state.schema import VCDigitalTwinState, add_audit_entry
from src.config.loader import InvestmentThesisConfig, get_config
from src.prompts.templates import get_template_manager


class SupervisorDecision(BaseModel):
    """Structured output from the Supervisor Agent."""

    next: str = Field(
        description="Name of the next agent to call, or 'FINISH' to complete the workflow"
    )
    reasoning: str = Field(description="Detailed explanation of why this routing decision was made")
    task_description: str = Field(
        description="Comprehensive instructions for the next agent, including specific questions to answer and output format"
    )


class SupervisorAgent:
    """
    Supervisor Agent that orchestrates the VC Digital Twin workflow.

    The Supervisor analyzes the current state, delegates tasks to specialized
    worker agents, monitors progress, and synthesizes findings.
    """

    def __init__(self, config: Optional[InvestmentThesisConfig] = None):
        """
        Initialize the Supervisor Agent.

        Args:
            config: Investment thesis configuration. If None, loads default config.
        """
        self.config = config or get_config()
        self.template_manager = get_template_manager(self.config)

        # Initialize LLM based on config
        agent_config = self.config.agent_config.get("supervisor", {})
        model_name = agent_config.get("model", os.getenv("SUPERVISOR_MODEL", "gpt-4o"))
        temperature = agent_config.get("temperature", 0.3)
        max_tokens = agent_config.get("max_tokens", 4096)

        # Choose LLM provider based on model name
        if "gpt" in model_name:
            self.llm = ChatOpenAI(
                model=model_name, temperature=temperature, max_tokens=max_tokens
            )
        elif "claude" in model_name:
            self.llm = ChatAnthropic(
                model=model_name, temperature=temperature, max_tokens=max_tokens
            )
        else:
            # Default to OpenAI
            self.llm = ChatOpenAI(
                model="gpt-4o", temperature=temperature, max_tokens=max_tokens
            )

        # Add structured output
        self.llm_with_structure = self.llm.with_structured_output(SupervisorDecision)

    def __call__(self, state: VCDigitalTwinState) -> Command[Literal[
        "market_analysis",
        "competitor_intelligence",
        "industry_research",
        "financial_analysis",
        "technical_assessment",
        "team_evaluation",
        "legal_review",
        "performance_tracking",
        "milestone_monitoring",
        "portfolio_support",
        "__end__",
    ]]:
        """
        Process the current state and make a routing decision.

        Args:
            state: Current system state

        Returns:
            Command object with next agent and state updates
        """
        # Generate supervisor prompt based on current state
        prompt = self.template_manager.get_supervisor_prompt(
            user_query=state.get("user_query", ""),
            current_phase=state.get("current_phase", "research"),
            completed_tasks=state.get("completed_tasks", []),
            pending_tasks=state.get("pending_tasks", []),
        )

        # Get recent messages for context
        messages = state.get("messages", [])
        recent_messages = messages[-10:] if len(messages) > 10 else messages

        # Create the message list for LLM
        llm_messages = [
            SystemMessage(content=prompt),
        ]

        # Add recent conversation history
        if recent_messages:
            llm_messages.extend(recent_messages)

        # Add current state summary as a human message
        state_summary = self._create_state_summary(state)
        llm_messages.append(HumanMessage(content=f"Current State:\n{state_summary}"))

        # Get decision from LLM
        try:
            decision: SupervisorDecision = self.llm_with_structure.invoke(llm_messages)
        except Exception as e:
            # Fallback decision if LLM fails
            print(f"Error getting supervisor decision: {e}")
            decision = SupervisorDecision(
                next="FINISH",
                reasoning=f"Error occurred: {str(e)}",
                task_description="Complete workflow due to error",
            )

        # Determine next node
        next_agent = decision.next.lower()

        # Map "FINISH" to the end node
        if next_agent == "finish":
            goto = "__end__"
        else:
            # Validate agent name
            valid_agents = [
                "market_analysis",
                "competitor_intelligence",
                "industry_research",
                "financial_analysis",
                "technical_assessment",
                "team_evaluation",
                "legal_review",
                "performance_tracking",
                "milestone_monitoring",
                "portfolio_support",
            ]

            if next_agent not in valid_agents:
                # Default to ending if invalid agent
                print(f"Warning: Invalid agent name '{next_agent}', ending workflow")
                goto = "__end__"
            else:
                goto = next_agent

        # Prepare state updates
        updates = {
            "next_agent": decision.next,
            "updated_at": datetime.utcnow().isoformat(),
        }

        # Add supervisor's decision to messages
        supervisor_message = HumanMessage(
            content=f"**Supervisor Decision:**\n\n"
            f"Next: {decision.next}\n\n"
            f"Reasoning: {decision.reasoning}\n\n"
            f"Task: {decision.task_description}",
            name="supervisor",
        )

        # Add audit entry
        audit_update = add_audit_entry(
            state=state,
            agent="supervisor",
            action="routing_decision",
            details={
                "next_agent": decision.next,
                "reasoning": decision.reasoning,
                "task": decision.task_description,
            },
        )

        # Combine updates
        final_update = {
            **updates,
            **audit_update,
            "messages": [supervisor_message],
        }

        # Return Command with routing and state update
        return Command(goto=goto, update=final_update)

    def _create_state_summary(self, state: VCDigitalTwinState) -> str:
        """
        Create a concise summary of the current state for the LLM.

        Args:
            state: Current system state

        Returns:
            Formatted state summary
        """
        company_name = state.get("company_data", {}).get("name", "Unknown")
        sector = state.get("company_data", {}).get("sector", "Not specified")
        stage = state.get("company_data", {}).get("stage", "Not specified")

        # Get due diligence status
        dd_status = state.get("due_diligence", {})
        completed_phases = dd_status.get("completed_phases", [])
        red_flags = dd_status.get("red_flags", [])

        # Get market data if available
        market_data = state.get("market_data", {})
        tam = market_data.get("tam")
        market_growth = market_data.get("market_growth_rate")

        # Get financial data if available
        financial_data = state.get("financial_data", {})
        revenue = financial_data.get("revenue")
        runway = financial_data.get("runway_months")

        summary = f"""
**Company:** {company_name}
**Sector:** {sector}
**Stage:** {stage}

**Completed Analysis:**
{', '.join(completed_phases) if completed_phases else 'None yet'}

**Key Findings:**
"""

        if tam:
            summary += f"- TAM: ${tam / 1e9:.1f}B\n"
        if market_growth:
            summary += f"- Market Growth: {market_growth}% CAGR\n"
        if revenue:
            summary += f"- Revenue: ${revenue / 1e6:.1f}M\n"
        if runway:
            summary += f"- Runway: {runway} months\n"

        if red_flags:
            summary += f"\n**Red Flags:** {len(red_flags)} identified\n"
            for flag in red_flags[:3]:  # Show top 3
                summary += f"  - {flag.get('category', 'Unknown')}: {flag.get('description', '')[:100]}\n"

        return summary


def create_supervisor_node(config: Optional[InvestmentThesisConfig] = None):
    """
    Create a supervisor node function for the StateGraph.

    Args:
        config: Investment thesis configuration

    Returns:
        Supervisor node function
    """
    supervisor = SupervisorAgent(config=config)
    return supervisor
