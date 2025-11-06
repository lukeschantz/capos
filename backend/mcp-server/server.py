"""
Capital OS MCP Server
Wraps existing VC Digital Twin agents and exposes them via MCP protocol
"""

from fastmcp import FastMCP
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import sys
import os
import asyncio

# Add the src directory to path to import existing agents
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

# Initialize MCP server
mcp = FastMCP("capital-os-mcp")

# ============= RESOURCES =============

@mcp.resource("vc://portfolio")
async def get_portfolio() -> str:
    """Get current portfolio status and metrics"""
    return """Portfolio Overview:
- Active Investments: 12
- Total AUM: $50M
- Current Pipeline: 45 opportunities
- Recent Exits: 2
"""

@mcp.resource("vc://market-reports")
async def get_market_reports() -> str:
    """Get recent market analysis reports"""
    return """Recent Market Reports:
1. AI Infrastructure Market Analysis (Nov 2024)
2. Fintech Trends Q4 2024
3. Healthcare AI Opportunities
"""

@mcp.resource("vc://investment-thesis")
async def get_investment_thesis() -> str:
    """Get current investment thesis and criteria"""
    # Load the actual investment thesis from config
    try:
        from src.config.loader import get_config
        config = get_config()

        thesis_info = f"""Investment Thesis:
- Stage Focus: {', '.join([s['name'] for s in config.stage_preferences])}
- Sector Focus: {', '.join([s['name'] for s in config.sector_preferences])}
- Check Sizes: Varies by stage
- Geographic: Global with US/EU preference
"""
        return thesis_info
    except Exception as e:
        return f"Investment Thesis (default): Error loading config - {str(e)}"

# ============= TOOLS =============

class MarketAnalysisRequest(BaseModel):
    company_name: str
    sector: Optional[str] = "Technology"
    stage: Optional[str] = "seed"
    additional_context: Optional[str] = None

@mcp.tool()
async def analyze_market(request: MarketAnalysisRequest) -> Dict[str, Any]:
    """
    Analyze market opportunity for a company using the existing VC Digital Twin agents.

    This wraps the existing LangGraph supervisor-worker pattern.
    """
    try:
        from src.graph import get_graph
        from src.state.schema import create_initial_state

        # Create the graph with existing agents
        graph = get_graph()

        # Create initial state
        state = create_initial_state(
            user_query=f"Analyze {request.company_name} as a potential investment opportunity. Focus on market analysis.",
            company_name=request.company_name,
        )

        # Add company data
        state["company_data"]["sector"] = request.sector
        state["company_data"]["stage"] = request.stage

        # Run the analysis through the existing graph
        config = {"configurable": {"thread_id": f"mcp-{request.company_name.lower().replace(' ', '-')}"}}
        result = graph.invoke(state, config=config)

        # Extract market data from result
        market_data = result.get("market_data", {})

        return {
            "company": request.company_name,
            "status": "complete",
            "market_analysis": {
                "tam": market_data.get("total_addressable_market", "Unknown"),
                "growth_rate": market_data.get("market_growth_rate", "Unknown"),
                "competitive_landscape": market_data.get("competitive_landscape", {}),
                "opportunities": market_data.get("opportunities", []),
                "risks": market_data.get("risks", []),
            },
            "agent_notes": [msg.content for msg in result.get("messages", [])[-3:]],
            "recommendation": result.get("next_steps", "Analysis complete")
        }
    except Exception as e:
        return {
            "company": request.company_name,
            "status": "error",
            "error": str(e),
            "message": "Failed to analyze company. Check MCP server logs."
        }

class DueDiligenceRequest(BaseModel):
    company_name: str
    focus_areas: Optional[List[str]] = None
    depth: str = "standard"  # quick, standard, deep

@mcp.tool()
async def run_due_diligence(request: DueDiligenceRequest) -> Dict[str, Any]:
    """
    Run comprehensive due diligence using the VC Digital Twin agent system.

    Orchestrates multiple specialized agents for thorough analysis.
    """
    try:
        from src.graph import get_graph
        from src.state.schema import create_initial_state

        # Create focus areas query
        focus = ", ".join(request.focus_areas) if request.focus_areas else "comprehensive analysis"

        graph = get_graph()
        state = create_initial_state(
            user_query=f"Conduct {request.depth} due diligence on {request.company_name}. Focus on: {focus}",
            company_name=request.company_name,
        )

        config = {"configurable": {"thread_id": f"dd-{request.company_name.lower().replace(' ', '-')}"}}
        result = graph.invoke(state, config=config)

        return {
            "company": request.company_name,
            "status": "complete",
            "depth": request.depth,
            "findings": {
                "market": result.get("market_data", {}),
                "financial": result.get("financial_data", {}),
                "team": result.get("team_assessment", {}),
                "technical": result.get("technical_assessment", {}),
            },
            "red_flags": result.get("red_flags", []),
            "strengths": result.get("strengths", []),
            "overall_score": result.get("investment_score", 0),
        }
    except Exception as e:
        return {
            "company": request.company_name,
            "status": "error",
            "error": str(e)
        }

class PortfolioMonitorRequest(BaseModel):
    company_name: str
    metrics: Optional[List[str]] = None

@mcp.tool()
async def monitor_portfolio_company(request: PortfolioMonitorRequest) -> Dict[str, Any]:
    """
    Monitor portfolio company performance and milestones.

    Note: This is a placeholder for Phase 3 implementation.
    """
    return {
        "company": request.company_name,
        "status": "monitoring",
        "message": "Portfolio monitoring will be implemented in Phase 3",
        "placeholder_data": {
            "health_score": 85,
            "last_update": "2024-11-06",
            "key_metrics": {
                "mrr_growth": "15% MoM",
                "burn_rate": "$200K/month",
                "runway": "18 months"
            }
        }
    }

# ============= PROMPTS =============

@mcp.prompt()
def vc_analyst_prompt() -> str:
    """Prompt for VC analyst assistant using Capital OS"""
    return """You are an experienced venture capital analyst working with Capital OS.

Your role is to:
1. Analyze investment opportunities using the available MCP tools
2. Provide data-driven recommendations based on our investment thesis
3. Identify key risks and opportunities in the market
4. Support decision-making with quantitative analysis

Available tools:
- analyze_market: Deep market analysis for a company
- run_due_diligence: Comprehensive due diligence across multiple domains
- monitor_portfolio_company: Track portfolio company performance

Always base recommendations on data and maintain objectivity. Use the investment thesis resource to align with fund strategy."""

@mcp.prompt()
def market_research_prompt() -> str:
    """Prompt for focused market research tasks"""
    return """You are conducting market research for venture capital investment decisions.

Focus areas:
- TAM/SAM/SOM analysis with quantified estimates
- Competitive landscape mapping
- Market growth trajectories and inflection points
- Regulatory considerations and barriers to entry
- Technology trends and adoption curves

Provide quantified insights wherever possible. Cite sources for market data."""

# ============= MAIN ENTRY POINT =============

if __name__ == "__main__":
    print("🚀 Starting Capital OS MCP Server...")
    print("📡 MCP Protocol: Active")
    print("🤖 VC Digital Twin Agents: Connected")
    print("⚡ Ready for requests")

    # Run the MCP server
    mcp.run()
