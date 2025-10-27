"""
Configuration loader for investment thesis customization.

This module handles loading and validating YAML/JSON configuration files
that define the VC firm's investment thesis, evaluation criteria, and
agent behavior parameters.
"""

import os
import yaml
import json
from typing import Dict, Any, List, Optional
from pathlib import Path
from pydantic import BaseModel, Field, field_validator


class StageConfig(BaseModel):
    """Configuration for investment stage preferences."""
    name: str = Field(..., description="Stage name (pre-seed, seed, series-a, etc.)")
    min_check_size: float = Field(..., description="Minimum check size in USD")
    max_check_size: float = Field(..., description="Maximum check size in USD")
    target_ownership: float = Field(..., description="Target ownership percentage")
    priority: int = Field(default=3, description="Priority level (1=highest, 5=lowest)")


class SectorConfig(BaseModel):
    """Configuration for sector preferences."""
    name: str = Field(..., description="Sector name")
    expertise_level: str = Field(..., description="Expertise level: high, moderate, learning, avoid")
    specific_guidance: Optional[str] = Field(None, description="Sector-specific evaluation guidance")
    sub_sectors: List[str] = Field(default_factory=list, description="Specific sub-sectors of interest")


class EvaluationCriterion(BaseModel):
    """Individual evaluation criterion with weight and guidance."""
    name: str = Field(..., description="Criterion name")
    weight: int = Field(..., description="Weight 0-100")
    guidance: str = Field(..., description="Specific guidance for this criterion")
    threshold: Optional[float] = Field(None, description="Optional numeric threshold")
    required: bool = Field(default=False, description="Is this criterion required?")

    @field_validator('weight')
    @classmethod
    def validate_weight(cls, v):
        if not 0 <= v <= 100:
            raise ValueError("Weight must be between 0 and 100")
        return v


class RedFlag(BaseModel):
    """Configuration for red flags and deal-breakers."""
    name: str = Field(..., description="Red flag name")
    severity: str = Field(..., description="Severity: blocking, concerning, warning")
    description: str = Field(..., description="Description of the red flag")
    exceptions: Optional[str] = Field(None, description="Conditions for exceptions")


class FundStrategy(BaseModel):
    """Fund-level strategy configuration."""
    fund_size: float = Field(..., description="Total fund size in USD")
    deployment_target_years: int = Field(..., description="Target years for deployment")
    reserve_ratio: float = Field(..., description="Percentage reserved for follow-ons")
    target_portfolio_size: int = Field(..., description="Target number of companies")
    concentration_strategy: str = Field(..., description="Concentrated or diversified")


class OutputPreferences(BaseModel):
    """Output formatting preferences."""
    executive_summary_max_paragraphs: int = Field(default=3, description="Max paragraphs in exec summary")
    include_scenarios: bool = Field(default=True, description="Include bull/base/bear scenarios")
    confidence_indicators: bool = Field(default=True, description="Show confidence levels")
    require_citations: bool = Field(default=True, description="Require source citations")
    visualization_format: str = Field(default="markdown", description="markdown, html, or json")


class InvestmentThesisConfig(BaseModel):
    """
    Complete investment thesis configuration.

    This configuration shapes how all agents behave, what they prioritize,
    and how they evaluate opportunities.
    """

    # Metadata
    config_version: str = Field(..., description="Configuration version for tracking")
    firm_name: str = Field(..., description="VC firm name")
    created_date: str = Field(..., description="Configuration creation date")
    last_updated: str = Field(..., description="Last update date")

    # Strategic parameters
    stage_preferences: List[StageConfig] = Field(..., description="Preferred investment stages")
    sector_preferences: List[SectorConfig] = Field(..., description="Sector preferences and expertise")
    geographic_scope: List[str] = Field(..., description="Preferred geographies")
    fund_strategy: FundStrategy = Field(..., description="Fund-level strategy")

    # Evaluation criteria
    team_criteria: List[EvaluationCriterion] = Field(..., description="Team evaluation criteria")
    market_criteria: List[EvaluationCriterion] = Field(..., description="Market evaluation criteria")
    product_criteria: List[EvaluationCriterion] = Field(..., description="Product evaluation criteria")
    financial_criteria: List[EvaluationCriterion] = Field(..., description="Financial metrics criteria")
    traction_criteria: List[EvaluationCriterion] = Field(..., description="Traction metrics criteria")

    # Red flags
    red_flags: List[RedFlag] = Field(..., description="Red flags and deal-breakers")

    # Agent configuration
    agent_config: Dict[str, Any] = Field(default_factory=dict, description="Agent-specific configurations")

    # Output preferences
    output_preferences: OutputPreferences = Field(
        default_factory=OutputPreferences,
        description="Output formatting preferences"
    )

    # Human-in-the-loop
    human_review_required_for: List[str] = Field(
        default_factory=list,
        description="Actions requiring human review"
    )

    def get_stage_config(self, stage: str) -> Optional[StageConfig]:
        """Get configuration for a specific stage."""
        for stage_config in self.stage_preferences:
            if stage_config.name.lower() == stage.lower():
                return stage_config
        return None

    def get_sector_config(self, sector: str) -> Optional[SectorConfig]:
        """Get configuration for a specific sector."""
        for sector_config in self.sector_preferences:
            if sector_config.name.lower() == sector.lower():
                return sector_config
        return None

    def get_criteria_by_category(self, category: str) -> List[EvaluationCriterion]:
        """Get evaluation criteria for a specific category."""
        category_map = {
            "team": self.team_criteria,
            "market": self.market_criteria,
            "product": self.product_criteria,
            "financial": self.financial_criteria,
            "traction": self.traction_criteria,
        }
        return category_map.get(category.lower(), [])

    def is_blocking_red_flag(self, red_flag_name: str) -> bool:
        """Check if a red flag is blocking (vs just concerning)."""
        for flag in self.red_flags:
            if flag.name.lower() == red_flag_name.lower():
                return flag.severity == "blocking"
        return False


class ConfigLoader:
    """Loads and manages investment thesis configurations."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the config loader.

        Args:
            config_path: Path to config file. If None, uses CONFIG_PATH env var
                        or defaults to config/investment_thesis.yaml
        """
        if config_path:
            self.config_path = Path(config_path)
        else:
            config_path_env = os.getenv("CONFIG_PATH", "config/investment_thesis.yaml")
            self.config_path = Path(config_path_env)

        self._config: Optional[InvestmentThesisConfig] = None

    def load(self) -> InvestmentThesisConfig:
        """
        Load configuration from file.

        Returns:
            InvestmentThesisConfig instance

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config is invalid
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        # Load based on file extension
        if self.config_path.suffix in ['.yaml', '.yml']:
            with open(self.config_path, 'r') as f:
                config_data = yaml.safe_load(f)
        elif self.config_path.suffix == '.json':
            with open(self.config_path, 'r') as f:
                config_data = json.load(f)
        else:
            raise ValueError(f"Unsupported config file format: {self.config_path.suffix}")

        # Validate and parse with Pydantic
        self._config = InvestmentThesisConfig(**config_data)
        return self._config

    def get_config(self) -> InvestmentThesisConfig:
        """
        Get loaded configuration, loading if necessary.

        Returns:
            InvestmentThesisConfig instance
        """
        if self._config is None:
            self.load()
        return self._config

    def reload(self) -> InvestmentThesisConfig:
        """
        Reload configuration from file.

        Returns:
            InvestmentThesisConfig instance
        """
        self._config = None
        return self.load()

    def save(self, config: InvestmentThesisConfig, path: Optional[Path] = None) -> None:
        """
        Save configuration to file.

        Args:
            config: Configuration to save
            path: Optional path to save to (defaults to loaded path)
        """
        save_path = path or self.config_path

        # Convert to dict
        config_dict = config.model_dump()

        # Save based on file extension
        if save_path.suffix in ['.yaml', '.yml']:
            with open(save_path, 'w') as f:
                yaml.safe_dump(config_dict, f, default_flow_style=False, sort_keys=False)
        elif save_path.suffix == '.json':
            with open(save_path, 'w') as f:
                json.dump(config_dict, f, indent=2)
        else:
            raise ValueError(f"Unsupported config file format: {save_path.suffix}")


# Singleton instance for easy access
_default_loader: Optional[ConfigLoader] = None


def get_config() -> InvestmentThesisConfig:
    """
    Get the default configuration instance.

    Returns:
        InvestmentThesisConfig instance
    """
    global _default_loader
    if _default_loader is None:
        _default_loader = ConfigLoader()
    return _default_loader.get_config()


def reload_config() -> InvestmentThesisConfig:
    """
    Reload the default configuration from file.

    Returns:
        InvestmentThesisConfig instance
    """
    global _default_loader
    if _default_loader is None:
        _default_loader = ConfigLoader()
    return _default_loader.reload()
