#!/usr/bin/env python3
"""
Simple example of using the VC Digital Twin system.

This demonstrates the basic workflow for evaluating a company.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from src.graph import get_graph
from src.state.schema import create_initial_state, InvestmentContext


def main():
    """Run a simple evaluation example."""
    # Load environment variables
    load_dotenv()

    print("=" * 80)
    print("VC Digital Twin - Simple Evaluation Example")
    print("=" * 80)

    # Create the graph
    print("\n1. Creating multi-agent system...")
    graph = get_graph()

    # Create investment context (uses default from config)
    investment_context = InvestmentContext()

    # Create initial state for a SaaS company evaluation
    print("\n2. Setting up evaluation for 'Example SaaS Corp'...")
    state = create_initial_state(
        user_query="Evaluate this SaaS company for seed investment, focusing on market opportunity and unit economics",
        company_name="Example SaaS Corp",
        investment_context=investment_context,
    )

    # Add company details
    state["company_data"]["sector"] = "SaaS"
    state["company_data"]["stage"] = "seed"
    state["company_data"]["description"] = "B2B project management tool for remote teams"

    # Run the evaluation with streaming
    print("\n3. Running evaluation (streaming)...\n")
    print("-" * 80)

    config = {"configurable": {"thread_id": "example-001"}}

    try:
        for event in graph.stream(state, config=config, stream_mode="values"):
            # Print new messages
            messages = event.get("messages", [])
            if messages:
                latest_msg = messages[-1]
                if hasattr(latest_msg, "name") and latest_msg.name:
                    print(f"\n[{latest_msg.name.upper()}]")
                print(latest_msg.content if hasattr(latest_msg, "content") else latest_msg)
                print("\n" + "-" * 80)

        print("\n4. Evaluation complete!")

        # Get final state
        final_state = graph.get_state(config)
        state_values = final_state.values

        # Print summary
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)

        completed = state_values.get("completed_tasks", [])
        print(f"\nCompleted: {', '.join(completed)}")

        market_data = state_values.get("market_data", {})
        if market_data:
            print(f"\nMarket Data Available: {len(market_data)} fields")

        dd_status = state_values.get("due_diligence", {})
        red_flags = dd_status.get("red_flags", [])
        if red_flags:
            print(f"\nRed Flags: {len(red_flags)} identified")

    except Exception as e:
        print(f"\n❌ Error during evaluation: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
