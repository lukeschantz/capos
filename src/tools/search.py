"""
Web search and data retrieval tools for VC Digital Twin agents.

This module provides tools for agents to gather information from the web,
databases, and other external sources during their analysis.
"""

import os
from typing import List, Dict, Any, Optional
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import Tool


class SearchToolkit:
    """Collection of search and data retrieval tools for agents."""

    def __init__(self, max_results: int = 5):
        """
        Initialize the search toolkit.

        Args:
            max_results: Maximum number of search results to return
        """
        self.max_results = max_results
        self._tavily_search = None

    def get_web_search_tool(self) -> Tool:
        """
        Get the web search tool (Tavily).

        Returns:
            LangChain Tool for web searching

        Raises:
            ValueError: If TAVILY_API_KEY is not set
        """
        if not os.getenv("TAVILY_API_KEY"):
            raise ValueError(
                "TAVILY_API_KEY environment variable not set. "
                "Web search functionality requires a Tavily API key."
            )

        if self._tavily_search is None:
            self._tavily_search = TavilySearchResults(
                max_results=self.max_results,
                search_depth="advanced",  # Use advanced search for better results
                include_answer=True,  # Include AI-generated answer summary
                include_raw_content=False,  # Don't include full HTML
            )

        return self._tavily_search

    def get_company_research_tool(self) -> Tool:
        """
        Get a specialized tool for company research.

        This tool is optimized for searching company information,
        funding data, competitor analysis, etc.

        Returns:
            LangChain Tool for company research
        """

        def search_company_info(query: str) -> str:
            """
            Search for company information.

            Args:
                query: Search query about a company

            Returns:
                Formatted search results
            """
            search_tool = self.get_web_search_tool()

            # Enhance query with company research keywords
            enhanced_query = f"{query} company funding valuation revenue"

            try:
                results = search_tool.invoke({"query": enhanced_query})

                if isinstance(results, list):
                    formatted_results = []
                    for i, result in enumerate(results[:self.max_results], 1):
                        if isinstance(result, dict):
                            title = result.get("title", "No title")
                            url = result.get("url", "")
                            content = result.get("content", "")
                            formatted_results.append(
                                f"{i}. {title}\n   URL: {url}\n   {content}\n"
                            )
                        else:
                            formatted_results.append(f"{i}. {result}\n")

                    return "\n".join(formatted_results)
                else:
                    return str(results)

            except Exception as e:
                return f"Error searching for company information: {str(e)}"

        return Tool(
            name="company_research",
            description=(
                "Search for information about a company including funding, "
                "valuation, revenue, team, products, and competitors. "
                "Input should be a search query about the company."
            ),
            func=search_company_info,
        )

    def get_market_research_tool(self) -> Tool:
        """
        Get a specialized tool for market research.

        This tool is optimized for market size, growth rates, trends, etc.

        Returns:
            LangChain Tool for market research
        """

        def search_market_info(query: str) -> str:
            """
            Search for market information.

            Args:
                query: Search query about a market

            Returns:
                Formatted search results
            """
            search_tool = self.get_web_search_tool()

            # Enhance query with market research keywords
            enhanced_query = f"{query} market size TAM growth rate trends forecast"

            try:
                results = search_tool.invoke({"query": enhanced_query})

                if isinstance(results, list):
                    formatted_results = []
                    for i, result in enumerate(results[:self.max_results], 1):
                        if isinstance(result, dict):
                            title = result.get("title", "No title")
                            url = result.get("url", "")
                            content = result.get("content", "")
                            formatted_results.append(
                                f"{i}. {title}\n   URL: {url}\n   {content}\n"
                            )

                    return "\n".join(formatted_results)
                else:
                    return str(results)

            except Exception as e:
                return f"Error searching for market information: {str(e)}"

        return Tool(
            name="market_research",
            description=(
                "Search for market information including market size (TAM/SAM), "
                "growth rates, trends, forecasts, and industry analysis. "
                "Input should be a search query about the market."
            ),
            func=search_market_info,
        )

    def get_competitor_research_tool(self) -> Tool:
        """
        Get a specialized tool for competitor research.

        Returns:
            LangChain Tool for competitor research
        """

        def search_competitor_info(query: str) -> str:
            """
            Search for competitor information.

            Args:
                query: Search query about competitors

            Returns:
                Formatted search results
            """
            search_tool = self.get_web_search_tool()

            # Enhance query with competitor keywords
            enhanced_query = f"{query} competitors competition market share alternatives"

            try:
                results = search_tool.invoke({"query": enhanced_query})

                if isinstance(results, list):
                    formatted_results = []
                    for i, result in enumerate(results[:self.max_results], 1):
                        if isinstance(result, dict):
                            title = result.get("title", "No title")
                            url = result.get("url", "")
                            content = result.get("content", "")
                            formatted_results.append(
                                f"{i}. {title}\n   URL: {url}\n   {content}\n"
                            )

                    return "\n".join(formatted_results)
                else:
                    return str(results)

            except Exception as e:
                return f"Error searching for competitor information: {str(e)}"

        return Tool(
            name="competitor_research",
            description=(
                "Search for information about competitors including market share, "
                "products, funding, positioning, and competitive dynamics. "
                "Input should be a search query about competitors or competitive landscape."
            ),
            func=search_competitor_info,
        )

    def get_all_tools(self) -> List[Tool]:
        """
        Get all available search tools.

        Returns:
            List of all search tools
        """
        try:
            return [
                self.get_web_search_tool(),
                self.get_company_research_tool(),
                self.get_market_research_tool(),
                self.get_competitor_research_tool(),
            ]
        except ValueError:
            # If Tavily API key is not set, return empty list
            return []


def get_search_tools(max_results: int = 5) -> List[Tool]:
    """
    Get search tools for agents.

    Args:
        max_results: Maximum number of search results

    Returns:
        List of search tools
    """
    toolkit = SearchToolkit(max_results=max_results)
    return toolkit.get_all_tools()


# Calculator tool for financial analysis
def create_calculator_tool() -> Tool:
    """
    Create a calculator tool for financial computations.

    Returns:
        LangChain Tool for calculations
    """
    from langchain.tools import StructuredTool
    from pydantic import BaseModel, Field

    class CalculatorInput(BaseModel):
        expression: str = Field(description="Mathematical expression to evaluate")

    def calculate(expression: str) -> str:
        """
        Safely evaluate a mathematical expression.

        Args:
            expression: Mathematical expression (e.g., "100 * 0.85")

        Returns:
            Result of the calculation
        """
        try:
            # Use a safe eval with limited scope
            allowed_names = {
                "abs": abs,
                "round": round,
                "min": min,
                "max": max,
                "sum": sum,
                "pow": pow,
            }
            # Remove any potentially dangerous characters
            safe_expression = expression.replace("__", "").replace("import", "")

            result = eval(safe_expression, {"__builtins__": {}}, allowed_names)
            return str(result)
        except Exception as e:
            return f"Error calculating: {str(e)}"

    return StructuredTool(
        name="calculator",
        description=(
            "Useful for performing mathematical calculations. "
            "Input should be a mathematical expression like '1000000 * 3 / 100'. "
            "Use this for financial calculations like LTV:CAC ratios, burn rates, etc."
        ),
        func=calculate,
        args_schema=CalculatorInput,
    )
