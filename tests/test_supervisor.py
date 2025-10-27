"""
Tests for the Supervisor Agent.
"""

import pytest
from unittest.mock import Mock, patch
from src.agents.supervisor import SupervisorAgent, SupervisorDecision
from src.state.schema import create_initial_state
from src.config.loader import InvestmentThesisConfig


class TestSupervisorAgent:
    """Test cases for Supervisor Agent."""

    @pytest.fixture
    def mock_config(self):
        """Create a minimal mock configuration."""
        # This would normally load from YAML, but for testing we create minimal config
        # In real tests, use a test config file
        return None  # Will use default config

    def test_supervisor_initialization(self, mock_config):
        """Test that supervisor initializes correctly."""
        supervisor = SupervisorAgent(config=mock_config)

        assert supervisor is not None
        assert supervisor.llm is not None
        assert supervisor.template_manager is not None

    def test_supervisor_routing_decision_structure(self, mock_config):
        """Test that supervisor returns properly structured routing decisions."""
        supervisor = SupervisorAgent(config=mock_config)

        # Create test state
        state = create_initial_state(
            user_query="Evaluate this SaaS company",
            company_name="Test Corp",
        )

        # Mock the LLM to return a predictable decision
        with patch.object(
            supervisor.llm_with_structure, "invoke"
        ) as mock_llm:
            mock_llm.return_value = SupervisorDecision(
                next="market_analysis",
                reasoning="Market analysis is the first step in evaluation",
                task_description="Analyze the TAM, SAM, SOM and competitive landscape",
            )

            # Call supervisor
            result = supervisor(state)

            # Check that result is a Command
            assert hasattr(result, "goto")
            assert hasattr(result, "update")

            # Check routing
            assert result.goto == "market_analysis"

            # Check that state was updated
            assert "updated_at" in result.update
            assert "messages" in result.update

    def test_supervisor_completion_routing(self, mock_config):
        """Test that supervisor routes to END when analysis is complete."""
        supervisor = SupervisorAgent(config=mock_config)

        state = create_initial_state(
            user_query="Evaluate this SaaS company",
            company_name="Test Corp",
        )

        # Set state to show analysis is complete
        state["completed_tasks"] = [
            "market_analysis",
            "financial_analysis",
            "team_evaluation",
        ]

        with patch.object(
            supervisor.llm_with_structure, "invoke"
        ) as mock_llm:
            mock_llm.return_value = SupervisorDecision(
                next="FINISH",
                reasoning="All required analysis is complete",
                task_description="Complete the workflow",
            )

            result = supervisor(state)

            # Should route to end
            assert result.goto == "__end__"

    def test_supervisor_audit_trail(self, mock_config):
        """Test that supervisor adds audit trail entries."""
        supervisor = SupervisorAgent(config=mock_config)

        state = create_initial_state(
            user_query="Evaluate this SaaS company",
            company_name="Test Corp",
        )

        initial_audit_count = len(state.get("audit_trail", []))

        with patch.object(
            supervisor.llm_with_structure, "invoke"
        ) as mock_llm:
            mock_llm.return_value = SupervisorDecision(
                next="market_analysis",
                reasoning="Start with market analysis",
                task_description="Analyze the market",
            )

            result = supervisor(state)

            # Check audit trail was updated
            assert "audit_trail" in result.update
            new_audit_count = len(result.update["audit_trail"])
            assert new_audit_count > initial_audit_count

    def test_supervisor_invalid_agent_handling(self, mock_config):
        """Test that supervisor handles invalid agent names gracefully."""
        supervisor = SupervisorAgent(config=mock_config)

        state = create_initial_state(
            user_query="Evaluate this company",
            company_name="Test Corp",
        )

        with patch.object(
            supervisor.llm_with_structure, "invoke"
        ) as mock_llm:
            # Return invalid agent name
            mock_llm.return_value = SupervisorDecision(
                next="invalid_agent_name",
                reasoning="This should be handled gracefully",
                task_description="Test invalid routing",
            )

            result = supervisor(state)

            # Should default to end on invalid agent
            assert result.goto == "__end__"


# Run tests with: pytest tests/test_supervisor.py -v
