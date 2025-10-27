#!/usr/bin/env python3
"""
CLI interface for the VC Digital Twin system.

This provides a simple command-line interface for testing and using
the multi-agent VC evaluation system.
"""

import os
import sys
import argparse
from typing import Optional
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

from src.graph import get_graph
from src.state.schema import create_initial_state, InvestmentContext
from src.config.loader import get_config


def setup_environment():
    """Load environment variables from .env file."""
    load_dotenv()

    # Check for required API keys
    required_vars = []
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        required_vars.append("OPENAI_API_KEY or ANTHROPIC_API_KEY")

    if required_vars:
        print("❌ Missing required environment variables:")
        for var in required_vars:
            print(f"   - {var}")
        print("\nPlease set these in your .env file or environment.")
        print("See .env.example for reference.")
        sys.exit(1)


def print_message(msg, indent=0):
    """Print a formatted message."""
    prefix = "  " * indent
    if hasattr(msg, "name") and msg.name:
        print(f"\n{prefix}[{msg.name.upper()}]")
    if hasattr(msg, "content"):
        print(f"{prefix}{msg.content}")
    else:
        print(f"{prefix}{msg}")


def run_evaluation(
    company_name: str,
    user_query: Optional[str] = None,
    stage: Optional[str] = None,
    sector: Optional[str] = None,
    stream: bool = True,
    use_postgres: bool = False,
):
    """
    Run an investment evaluation.

    Args:
        company_name: Name of the company to evaluate
        user_query: Specific evaluation request
        stage: Investment stage
        sector: Company sector
        stream: Whether to stream output in real-time
        use_postgres: Whether to use PostgreSQL checkpointing
    """
    print(f"\n{'='*80}")
    print(f"VC Digital Twin - Investment Evaluation")
    print(f"{'='*80}")
    print(f"\nCompany: {company_name}")
    if stage:
        print(f"Stage: {stage}")
    if sector:
        print(f"Sector: {sector}")
    print(f"\n{'='*80}\n")

    # Create the graph
    print("Initializing multi-agent system...")
    try:
        graph = get_graph(use_postgres=use_postgres)
    except Exception as e:
        print(f"❌ Error creating graph: {e}")
        return

    # Create investment context
    investment_context = InvestmentContext()

    # Create initial state
    query = user_query or f"Evaluate {company_name} for potential investment"

    state = create_initial_state(
        user_query=query,
        company_name=company_name,
        investment_context=investment_context,
    )

    # Add company details if provided
    if stage:
        state["company_data"]["stage"] = stage
    if sector:
        state["company_data"]["sector"] = sector

    # Configuration for checkpointing
    config = {"configurable": {"thread_id": f"eval-{company_name}-{datetime.now().timestamp()}"}}

    print("Starting evaluation...\n")

    try:
        if stream:
            # Stream execution for real-time feedback
            for event in graph.stream(state, config=config, stream_mode="values"):
                # Print new messages
                messages = event.get("messages", [])
                if messages:
                    latest_msg = messages[-1]
                    print_message(latest_msg, indent=0)
                    print("\n" + "-" * 80)

            print("\n✅ Evaluation complete!")

            # Get final state
            final_state = graph.get_state(config)
            print_final_summary(final_state.values)

        else:
            # Run without streaming
            result = graph.invoke(state, config=config)

            print("\n✅ Evaluation complete!")
            print_final_summary(result)

    except Exception as e:
        print(f"\n❌ Error during evaluation: {e}")
        import traceback

        traceback.print_exc()


def print_final_summary(state):
    """Print a summary of the final state."""
    print(f"\n{'='*80}")
    print("EVALUATION SUMMARY")
    print(f"{'='*80}\n")

    # Company info
    company_data = state.get("company_data", {})
    print(f"Company: {company_data.get('name', 'Unknown')}")
    print(f"Sector: {company_data.get('sector', 'Not specified')}")
    print(f"Stage: {company_data.get('stage', 'Not specified')}\n")

    # Completed tasks
    completed = state.get("completed_tasks", [])
    if completed:
        print(f"Completed Analysis: {', '.join(completed)}")

    # Due diligence status
    dd_status = state.get("due_diligence", {})
    completed_phases = dd_status.get("completed_phases", [])
    red_flags = dd_status.get("red_flags", [])

    if completed_phases:
        print(f"Completed Phases: {', '.join(completed_phases)}")

    if red_flags:
        print(f"\n⚠️  Red Flags Identified: {len(red_flags)}")
        for flag in red_flags[:5]:
            print(f"   - {flag.get('category', 'Unknown')}: {flag.get('description', '')}")

    # Market data if available
    market_data = state.get("market_data", {})
    if market_data.get("tam"):
        print(f"\n💰 Market Analysis:")
        print(f"   TAM: ${market_data.get('tam', 0)/1e9:.1f}B")
        if market_data.get("market_growth_rate"):
            print(f"   Growth Rate: {market_data.get('market_growth_rate')}% CAGR")

    # Financial data if available
    financial_data = state.get("financial_data", {})
    if financial_data.get("revenue"):
        print(f"\n💵 Financial Metrics:")
        print(f"   Revenue: ${financial_data.get('revenue', 0)/1e6:.1f}M")
        if financial_data.get("runway_months"):
            print(f"   Runway: {financial_data.get('runway_months')} months")
        if financial_data.get("ltv_cac_ratio"):
            print(f"   LTV:CAC: {financial_data.get('ltv_cac_ratio'):.1f}:1")

    print(f"\n{'='*80}\n")


def list_config():
    """Display the current configuration."""
    print(f"\n{'='*80}")
    print("INVESTMENT THESIS CONFIGURATION")
    print(f"{'='*80}\n")

    try:
        config = get_config()

        print(f"Firm: {config.firm_name}")
        print(f"Config Version: {config.config_version}")
        print(f"Last Updated: {config.last_updated}\n")

        print("Stage Preferences:")
        for stage in config.stage_preferences[:5]:
            print(f"  - {stage.name}: ${stage.min_check_size:,.0f} - ${stage.max_check_size:,.0f}")

        print("\nSector Preferences:")
        for sector in config.sector_preferences[:5]:
            print(f"  - {sector.name}: {sector.expertise_level}")

        print(f"\nGeographic Scope: {', '.join(config.geographic_scope)}")

        print(f"\nFund Strategy:")
        print(f"  - Fund Size: ${config.fund_strategy.fund_size/1e6:.0f}M")
        print(f"  - Target Portfolio: {config.fund_strategy.target_portfolio_size} companies")
        print(f"  - Reserve Ratio: {config.fund_strategy.reserve_ratio*100:.0f}%")

    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        print("\nMake sure config/investment_thesis.yaml exists.")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="VC Digital Twin - Multi-Agent Investment Evaluation System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Evaluate a company
  python cli.py evaluate --company "Acme Corp" --sector SaaS --stage seed

  # Show current configuration
  python cli.py config

  # Run evaluation with custom query
  python cli.py evaluate --company "TechCo" --query "Focus on unit economics"
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Evaluate command
    eval_parser = subparsers.add_parser("evaluate", help="Evaluate a company for investment")
    eval_parser.add_argument("--company", "-c", required=True, help="Company name")
    eval_parser.add_argument("--sector", "-s", help="Company sector (e.g., SaaS, Fintech)")
    eval_parser.add_argument("--stage", help="Investment stage (e.g., seed, series-a)")
    eval_parser.add_argument(
        "--query", "-q", help="Specific evaluation request or focus area"
    )
    eval_parser.add_argument(
        "--no-stream", action="store_true", help="Don't stream output (wait for completion)"
    )
    eval_parser.add_argument(
        "--postgres", action="store_true", help="Use PostgreSQL checkpointing"
    )

    # Config command
    config_parser = subparsers.add_parser("config", help="Show investment thesis configuration")

    # Parse arguments
    args = parser.parse_args()

    # Setup environment
    setup_environment()

    # Execute command
    if args.command == "evaluate":
        run_evaluation(
            company_name=args.company,
            user_query=args.query,
            stage=args.stage,
            sector=args.sector,
            stream=not args.no_stream,
            use_postgres=args.postgres,
        )
    elif args.command == "config":
        list_config()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
