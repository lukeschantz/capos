"""
Core state schema for the VC Digital Twin multi-agent system.

This module defines the comprehensive state structure that is shared across
all agents in the system, following the specification's hybrid state architecture.
"""

from typing import TypedDict, Annotated, List, Dict, Any, Optional, Literal
from datetime import datetime
from langchain_core.messages import BaseMessage, AnyMessage
from langgraph.graph.message import add_messages


# Type definitions for better type safety
RiskLevel = Literal["low", "medium", "high", "critical"]
WorkflowPhase = Literal["research", "due_diligence", "decision", "portfolio_monitoring"]
AgentStatus = Literal["pending", "in_progress", "completed", "failed"]
InvestmentStage = Literal["pre-seed", "seed", "series-a", "series-b", "series-c", "series-d-plus"]
ConfidenceLevel = Literal["high", "medium", "low"]


class CompanyData(TypedDict, total=False):
    """Basic company information."""
    name: str
    website: Optional[str]
    founded_date: Optional[str]
    founding_team: List[Dict[str, str]]  # [{"name": "...", "role": "...", "linkedin": "..."}]
    description: Optional[str]
    sector: Optional[str]
    stage: Optional[InvestmentStage]
    target_market: Optional[str]
    headquarters: Optional[str]


class FinancialData(TypedDict, total=False):
    """Financial metrics and data."""
    revenue: Optional[float]
    arr_mrr: Optional[float]  # Annual/Monthly Recurring Revenue
    burn_rate: Optional[float]  # Monthly burn
    cash_balance: Optional[float]
    runway_months: Optional[float]
    gross_margin: Optional[float]
    customer_count: Optional[int]
    cac: Optional[float]  # Customer Acquisition Cost
    ltv: Optional[float]  # Lifetime Value
    ltv_cac_ratio: Optional[float]
    payback_period_months: Optional[float]
    growth_rate: Optional[float]  # YoY or MoM
    valuation: Optional[float]
    last_round_amount: Optional[float]
    last_round_date: Optional[str]


class MarketData(TypedDict, total=False):
    """Market analysis and competitive intelligence."""
    tam: Optional[float]  # Total Addressable Market
    tam_confidence: Optional[ConfidenceLevel]
    sam: Optional[float]  # Serviceable Addressable Market
    som: Optional[float]  # Serviceable Obtainable Market
    market_growth_rate: Optional[float]
    competitive_landscape: Optional[str]
    key_competitors: List[str]
    market_timing: Optional[str]
    barriers_to_entry: Optional[str]


class DueDiligenceStatus(TypedDict, total=False):
    """Tracking due diligence progress."""
    completed_phases: List[str]
    pending_phases: List[str]
    open_questions: List[str]
    red_flags: List[Dict[str, Any]]  # [{"severity": "high", "category": "...", "description": "..."}]
    findings: Dict[str, Any]  # Agent-specific findings
    overall_risk_level: Optional[RiskLevel]


class AgentTask(TypedDict, total=False):
    """Individual agent task tracking."""
    agent_name: str
    status: AgentStatus
    task_description: str
    started_at: Optional[str]
    completed_at: Optional[str]
    result: Optional[Dict[str, Any]]
    error: Optional[str]


class InvestmentContext(TypedDict, total=False):
    """Investment thesis and evaluation parameters."""
    stage_focus: List[InvestmentStage]
    sector_preferences: List[str]
    check_size_min: Optional[float]
    check_size_max: Optional[float]
    evaluation_priorities: List[str]
    automatic_disqualifiers: List[str]
    custom_criteria: Dict[str, Any]


class AuditEntry(TypedDict):
    """Single audit trail entry."""
    timestamp: str
    agent: str
    action: str
    details: Dict[str, Any]


class VCDigitalTwinState(TypedDict):
    """
    Main state schema for the VC Digital Twin system.

    This state is shared across all agents and maintains the complete
    context for investment evaluation and portfolio monitoring.

    Uses Annotated with add_messages reducer for message history,
    ensuring proper message handling as per LangGraph best practices.
    """

    # Message history with automatic message addition
    messages: Annotated[List[AnyMessage], add_messages]

    # Company being evaluated
    company_data: CompanyData
    financial_data: FinancialData
    market_data: MarketData

    # Due diligence tracking
    due_diligence: DueDiligenceStatus

    # Agent coordination
    active_agents: List[str]
    agent_tasks: List[AgentTask]
    completed_tasks: List[str]
    pending_tasks: List[str]

    # Workflow management
    current_phase: WorkflowPhase
    next_agent: Optional[str]  # Used by supervisor for routing

    # Investment context (thesis parameters)
    investment_context: InvestmentContext

    # Audit trail
    audit_trail: List[AuditEntry]

    # User query and session info
    user_query: str
    session_id: Optional[str]
    created_at: str
    updated_at: str


# Helper functions for state updates

def create_initial_state(
    user_query: str,
    company_name: str,
    investment_context: Optional[InvestmentContext] = None,
) -> VCDigitalTwinState:
    """
    Create an initial state for a new investment evaluation.

    Args:
        user_query: The initial user request
        company_name: Name of the company to evaluate
        investment_context: Optional investment thesis parameters

    Returns:
        Initialized VCDigitalTwinState
    """
    now = datetime.utcnow().isoformat()

    return VCDigitalTwinState(
        messages=[],
        company_data=CompanyData(name=company_name),
        financial_data=FinancialData(),
        market_data=MarketData(),
        due_diligence=DueDiligenceStatus(
            completed_phases=[],
            pending_phases=["research", "financial_analysis", "technical_assessment",
                          "team_evaluation", "legal_review"],
            open_questions=[],
            red_flags=[],
            findings={},
        ),
        active_agents=[],
        agent_tasks=[],
        completed_tasks=[],
        pending_tasks=["market_analysis"],  # Start with market analysis
        current_phase="research",
        next_agent="supervisor",
        investment_context=investment_context or InvestmentContext(),
        audit_trail=[
            AuditEntry(
                timestamp=now,
                agent="system",
                action="state_initialized",
                details={"company": company_name, "query": user_query}
            )
        ],
        user_query=user_query,
        session_id=None,
        created_at=now,
        updated_at=now,
    )


def add_audit_entry(
    state: VCDigitalTwinState,
    agent: str,
    action: str,
    details: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Add an audit trail entry to the state.

    Args:
        state: Current state
        agent: Name of the agent performing the action
        action: Description of the action
        details: Additional details about the action

    Returns:
        State update dict
    """
    entry = AuditEntry(
        timestamp=datetime.utcnow().isoformat(),
        agent=agent,
        action=action,
        details=details
    )

    return {
        "audit_trail": state["audit_trail"] + [entry],
        "updated_at": entry["timestamp"]
    }


def update_agent_task(
    state: VCDigitalTwinState,
    agent_name: str,
    status: AgentStatus,
    result: Optional[Dict[str, Any]] = None,
    error: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update the status of an agent task.

    Args:
        state: Current state
        agent_name: Name of the agent
        status: New status
        result: Optional result data if completed
        error: Optional error message if failed

    Returns:
        State update dict
    """
    now = datetime.utcnow().isoformat()

    # Find existing task or create new one
    tasks = state.get("agent_tasks", [])
    task_index = None
    for i, task in enumerate(tasks):
        if task["agent_name"] == agent_name and task["status"] in ["pending", "in_progress"]:
            task_index = i
            break

    if task_index is not None:
        # Update existing task
        updated_task = tasks[task_index].copy()
        updated_task["status"] = status
        if status == "completed":
            updated_task["completed_at"] = now
            updated_task["result"] = result
        elif status == "failed":
            updated_task["error"] = error

        new_tasks = tasks.copy()
        new_tasks[task_index] = updated_task
    else:
        # Create new task
        new_task = AgentTask(
            agent_name=agent_name,
            status=status,
            task_description=f"Task for {agent_name}",
            started_at=now if status == "in_progress" else None,
            completed_at=now if status == "completed" else None,
            result=result,
            error=error
        )
        new_tasks = tasks + [new_task]

    return {
        "agent_tasks": new_tasks,
        "updated_at": now
    }
