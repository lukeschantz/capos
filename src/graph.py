"""
Main StateGraph for the VC Digital Twin multi-agent system.

This module builds the complete graph connecting the supervisor and all worker agents.
"""

import os
from typing import Optional

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.postgres import PostgresSaver

from src.state.schema import VCDigitalTwinState
from src.config.loader import InvestmentThesisConfig, get_config
from src.agents.supervisor import create_supervisor_node
from src.agents.market_analysis import create_market_analysis_node


def create_vc_digital_twin_graph(
    config: Optional[InvestmentThesisConfig] = None,
    checkpointer: Optional[any] = None,
) -> StateGraph:
    """
    Create the complete VC Digital Twin StateGraph.

    This function builds the graph with all nodes and edges according to the
    supervisor-worker pattern defined in the specification.

    Args:
        config: Investment thesis configuration. If None, loads default config.
        checkpointer: Optional checkpointer for state persistence.
                     If None, uses MemorySaver for development.

    Returns:
        Compiled StateGraph ready for execution
    """
    # Load config
    if config is None:
        config = get_config()

    # Create the StateGraph
    workflow = StateGraph(VCDigitalTwinState)

    # Create agent nodes
    supervisor = create_supervisor_node(config)
    market_analysis = create_market_analysis_node(config)

    # Add nodes to the graph
    workflow.add_node("supervisor", supervisor)
    workflow.add_node("market_analysis", market_analysis)

    # TODO: Add additional worker agents (Phase 2)
    # workflow.add_node("financial_analysis", create_financial_analysis_node(config))
    # workflow.add_node("technical_assessment", create_technical_assessment_node(config))
    # workflow.add_node("team_evaluation", create_team_evaluation_node(config))
    # etc.

    # Define edges
    # Start with supervisor
    workflow.add_edge(START, "supervisor")

    # Supervisor uses Command to route dynamically, so no conditional edge needed here
    # The Command return from supervisor handles routing

    # All worker agents return to supervisor
    # (Market analysis already returns Command with goto="supervisor")

    # Set up checkpointing
    if checkpointer is None:
        # Use in-memory checkpointer for development
        checkpointer = MemorySaver()

    # Compile the graph
    compiled_graph = workflow.compile(
        checkpointer=checkpointer,
        # Optional: Add interrupt_before for human-in-the-loop
        # interrupt_before=["supervisor"] if needed for review gates
    )

    return compiled_graph


def create_graph_with_postgres_checkpoint(
    database_url: Optional[str] = None, config: Optional[InvestmentThesisConfig] = None
) -> StateGraph:
    """
    Create the graph with PostgreSQL checkpointing for production.

    Args:
        database_url: PostgreSQL connection URL. If None, uses DATABASE_URL env var.
        config: Investment thesis configuration

    Returns:
        Compiled StateGraph with PostgreSQL checkpointing
    """
    # Get database URL
    db_url = database_url or os.getenv("DATABASE_URL")

    if not db_url:
        raise ValueError(
            "DATABASE_URL not provided and not set in environment. "
            "Either provide database_url parameter or set DATABASE_URL env var."
        )

    # Create PostgreSQL checkpointer
    checkpointer = PostgresSaver.from_conn_string(db_url)

    # Setup the checkpointer (create tables if needed)
    checkpointer.setup()

    return create_vc_digital_twin_graph(config=config, checkpointer=checkpointer)


# Convenience function to get a ready-to-use graph
def get_graph(
    use_postgres: bool = False,
    database_url: Optional[str] = None,
    config: Optional[InvestmentThesisConfig] = None,
) -> StateGraph:
    """
    Get a compiled VC Digital Twin graph ready for use.

    Args:
        use_postgres: Whether to use PostgreSQL checkpointing (default: False)
        database_url: Optional PostgreSQL URL (only used if use_postgres=True)
        config: Investment thesis configuration

    Returns:
        Compiled StateGraph
    """
    if use_postgres:
        return create_graph_with_postgres_checkpoint(
            database_url=database_url, config=config
        )
    else:
        return create_vc_digital_twin_graph(config=config)


# Example usage in module docstring
__doc__ += """

## Usage Example

```python
from src.graph import get_graph
from src.state.schema import create_initial_state

# Create the graph
graph = get_graph()

# Create initial state
state = create_initial_state(
    user_query="Evaluate this SaaS company for Series A investment",
    company_name="Example Corp",
)

# Run the graph
result = graph.invoke(state)

# Or stream for real-time updates
for event in graph.stream(state):
    print(event)
```

## With Checkpointing

```python
from src.graph import get_graph
from src.state.schema import create_initial_state

# Create graph with checkpointing
graph = get_graph(use_postgres=True)

# Create initial state with session ID for checkpointing
state = create_initial_state(
    user_query="Evaluate this SaaS company",
    company_name="Example Corp",
)

# Run with config to enable checkpointing
config = {"configurable": {"thread_id": "investment-eval-001"}}
result = graph.invoke(state, config=config)

# Later, resume from checkpoint
state2 = graph.get_state(config)
# Continue execution...
```
"""
