"""
Market Analysis Agent for VC Digital Twin system.

This agent conducts comprehensive market analysis including TAM/SAM/SOM calculations,
competitive landscape mapping, market timing assessment, and growth rate analysis.
"""

import os
from typing import Optional, Dict, Any
from datetime import datetime

from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langgraph.types import Command

from src.state.schema import VCDigitalTwinState, add_audit_entry, update_agent_task
from src.config.loader import InvestmentThesisConfig, get_config
from src.prompts.templates import get_template_manager
from src.tools.search import get_search_tools, create_calculator_tool


class MarketAnalysisAgent:
    """
    Market Analysis Agent using LangGraph's ReAct pattern.

    This agent gathers market intelligence, calculates market size,
    analyzes competitive dynamics, and assesses market timing.
    """

    def __init__(self, config: Optional[InvestmentThesisConfig] = None):
        """
        Initialize the Market Analysis Agent.

        Args:
            config: Investment thesis configuration
        """
        self.config = config or get_config()
        self.template_manager = get_template_manager(self.config)

        # Get agent-specific config
        agent_config = self.config.agent_config.get("market_analysis", {})
        model_name = agent_config.get("model", os.getenv("WORKER_MODEL", "gpt-4o"))
        temperature = agent_config.get("temperature", 0.5)
        max_tokens = agent_config.get("max_tokens", 8192)

        # Initialize LLM
        if "gpt" in model_name:
            self.llm = ChatOpenAI(
                model=model_name, temperature=temperature, max_tokens=max_tokens
            )
        elif "claude" in model_name:
            self.llm = ChatAnthropic(
                model=model_name, temperature=temperature, max_tokens=max_tokens
            )
        else:
            self.llm = ChatOpenAI(
                model="gpt-4o", temperature=temperature, max_tokens=max_tokens
            )

        # Initialize tools
        self.tools = self._get_tools()

        # Create the ReAct agent
        self.agent = create_react_agent(
            model=self.llm,
            tools=self.tools,
            state_modifier=self._create_state_modifier,
        )

    def _get_tools(self):
        """Get tools for the market analysis agent."""
        tools = []

        # Add search tools if available
        search_tools = get_search_tools(max_results=10)
        tools.extend(search_tools)

        # Add calculator for market size calculations
        tools.append(create_calculator_tool())

        return tools

    def _create_state_modifier(self, state: VCDigitalTwinState) -> str:
        """
        Create a system message for the agent based on current state.

        This injects the agent's prompt template with context from the state.

        Args:
            state: Current system state

        Returns:
            System message for the agent
        """
        company_data = state.get("company_data", {})
        company_name = company_data.get("name", "Unknown Company")
        sector = company_data.get("sector")
        stage = company_data.get("stage")

        # Get task description from supervisor if available
        task_description = None
        messages = state.get("messages", [])
        for msg in reversed(messages):
            if hasattr(msg, "name") and msg.name == "supervisor":
                # Extract task description from supervisor message
                content = msg.content
                if "Task:" in content:
                    task_description = content.split("Task:")[1].strip()
                    break

        # Generate the market analysis prompt
        prompt = self.template_manager.get_market_analysis_prompt(
            company_name=company_name,
            sector=sector,
            stage=stage,
            task_description=task_description,
        )

        return prompt

    def __call__(self, state: VCDigitalTwinState) -> Command[Literal["supervisor"]]:
        """
        Execute the market analysis agent.

        Args:
            state: Current system state

        Returns:
            Command object to return to supervisor with state updates
        """
        # Update agent status to in_progress
        state_update = update_agent_task(
            state=state, agent_name="market_analysis", status="in_progress"
        )

        # Add audit entry
        audit_update = add_audit_entry(
            state=state,
            agent="market_analysis",
            action="analysis_started",
            details={"company": state.get("company_data", {}).get("name")},
        )

        try:
            # Run the ReAct agent
            result = self.agent.invoke(state)

            # Extract the agent's response
            agent_messages = result.get("messages", [])
            if agent_messages:
                # Get the last AI message as the final analysis
                last_message = agent_messages[-1]
                if isinstance(last_message, AIMessage):
                    analysis_content = last_message.content

                    # Parse the analysis to extract structured data
                    market_data_update = self._parse_market_analysis(analysis_content)

                    # Create a formatted message
                    response_message = AIMessage(
                        content=f"**Market Analysis Complete**\n\n{analysis_content}",
                        name="market_analysis",
                    )

                    # Update state with findings
                    task_complete_update = update_agent_task(
                        state=state,
                        agent_name="market_analysis",
                        status="completed",
                        result={
                            "analysis": analysis_content,
                            "market_data": market_data_update,
                        },
                    )

                    # Update completed and pending tasks
                    completed_tasks = state.get("completed_tasks", []) + ["market_analysis"]
                    pending_tasks = [t for t in state.get("pending_tasks", []) if t != "market_analysis"]

                    # Update due diligence status
                    dd_status = state.get("due_diligence", {})
                    completed_phases = dd_status.get("completed_phases", []) + ["market_research"]

                    # Combine all updates
                    final_update = {
                        **state_update,
                        **audit_update,
                        **task_complete_update,
                        "market_data": {**state.get("market_data", {}), **market_data_update},
                        "completed_tasks": completed_tasks,
                        "pending_tasks": pending_tasks,
                        "due_diligence": {
                            **dd_status,
                            "completed_phases": completed_phases,
                        },
                        "messages": [response_message],
                    }

                    return Command(goto="supervisor", update=final_update)

        except Exception as e:
            # Handle errors
            error_message = f"Error in market analysis: {str(e)}"
            print(error_message)

            error_update = update_agent_task(
                state=state,
                agent_name="market_analysis",
                status="failed",
                error=error_message,
            )

            error_msg = AIMessage(
                content=f"**Market Analysis Failed**\n\n{error_message}",
                name="market_analysis",
            )

            final_update = {
                **state_update,
                **audit_update,
                **error_update,
                "messages": [error_msg],
            }

            return Command(goto="supervisor", update=final_update)

        # Fallback if no messages
        return Command(goto="supervisor", update={**state_update, **audit_update})

    def _parse_market_analysis(self, analysis_content: str) -> Dict[str, Any]:
        """
        Parse the market analysis to extract structured data.

        This is a simple parser - in production, you might use more sophisticated
        extraction or ask the LLM to return structured output.

        Args:
            analysis_content: The analysis text

        Returns:
            Dictionary of market data fields
        """
        market_data = {}

        # Simple keyword-based extraction
        # In production, use regex or structured output from LLM

        content_lower = analysis_content.lower()

        # Try to extract TAM
        if "tam:" in content_lower or "total addressable market" in content_lower:
            # Mark that TAM was analyzed
            market_data["tam_analyzed"] = True

        # Try to extract market growth rate
        if "growth rate:" in content_lower or "cagr" in content_lower:
            market_data["growth_analyzed"] = True

        # Try to extract competitive landscape
        if "competitor" in content_lower or "competitive" in content_lower:
            market_data["competitive_landscape_analyzed"] = True

        # Try to extract market timing
        if "timing" in content_lower or "market readiness" in content_lower:
            market_data["timing_analyzed"] = True

        # Store the full analysis
        market_data["analysis_text"] = analysis_content
        market_data["analysis_date"] = datetime.utcnow().isoformat()

        return market_data


def create_market_analysis_node(config: Optional[InvestmentThesisConfig] = None):
    """
    Create a market analysis node function for the StateGraph.

    Args:
        config: Investment thesis configuration

    Returns:
        Market analysis node function
    """
    agent = MarketAnalysisAgent(config=config)
    return agent
