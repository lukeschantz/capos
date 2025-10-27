# VC Digital Twin: Multi-Agent Investment Evaluation System

A comprehensive multi-agent AI system that transforms venture capital operations by orchestrating specialized agents for investment research, due diligence, and portfolio monitoring. Built with LangGraph's supervisor-worker pattern, this system enables VC firms to scale their analytical capabilities while maintaining thesis-specific customization.

## Overview

The VC Digital Twin employs a **hierarchical supervisor-worker architecture** where a central Supervisor Agent orchestrates specialized worker teams across three domains:

- **Research Agents**: Market Analysis, Competitor Intelligence, Industry Research
- **Due Diligence Agents**: Financial Analysis, Technical Assessment, Team Evaluation, Legal Review
- **Portfolio Management Agents**: Performance Tracking, Milestone Monitoring, Portfolio Support

Each agent uses chain-of-thought reasoning with configurable prompts that adapt to any VC firm's investment thesis, stage focus, and sector preferences.

## Key Features

- **Thesis-Driven Customization**: Configure evaluation criteria, stage preferences, sector expertise, and red flags via YAML
- **Intelligent Orchestration**: Supervisor agent dynamically routes tasks to specialized workers
- **Deep Reasoning**: Agents employ structured chain-of-thought with explicit calculations and citations
- **Production-Ready**: Built on LangGraph with checkpointing, error handling, and audit trails
- **Multi-LLM Support**: Works with OpenAI (GPT-4o), Anthropic (Claude), or Google (Gemini)
- **Extensible**: Modular design enables easy addition of new agents and tools

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Supervisor Agent                      │
│        (Coordination & Routing Logic)                   │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Research   │  │     Due      │  │  Portfolio   │
│    Agents    │  │  Diligence   │  │ Management   │
│              │  │   Agents     │  │   Agents     │
│ • Market     │  │ • Financial  │  │ • Tracking   │
│ • Competitor │  │ • Technical  │  │ • Milestones │
│ • Industry   │  │ • Team       │  │ • Support    │
│              │  │ • Legal      │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
        │                 │                 │
        └─────────────────┴─────────────────┘
                          │
                          ▼
              ┌─────────────────────┐
              │   Shared State      │
              │  (Messages, Data,   │
              │  Audit Trail)       │
              └─────────────────────┘
```

## Current Implementation Status

**Phase 1: Foundation & Single-Agent Prototype** ✅ COMPLETE

- ✅ Core StateGraph with comprehensive state schema
- ✅ Supervisor Agent with intelligent routing
- ✅ Market Analysis Agent (first worker)
- ✅ Configuration system for investment thesis
- ✅ Prompt templates with COSTAR framework
- ✅ Web search & calculator tools
- ✅ CLI interface for testing
- ✅ Checkpointing infrastructure

**Phase 2: Complete Due Diligence Agent Set** 🚧 PLANNED

- Financial Analysis Agent
- Technical Assessment Agent
- Team Evaluation Agent
- Legal Review Agent
- Parallel agent execution
- Comprehensive test suite

**Phase 3: Portfolio Monitoring** 🚧 PLANNED
**Phase 4: Production Deployment** 🚧 PLANNED

## Installation

### Prerequisites

- Python 3.10 or higher
- API key for at least one LLM provider (OpenAI, Anthropic, or Google)
- (Optional) Tavily API key for web search
- (Optional) PostgreSQL for persistent checkpointing

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd capos
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

Required environment variables:
```bash
# At least one LLM provider
OPENAI_API_KEY=sk-...
# OR
ANTHROPIC_API_KEY=sk-ant-...

# Optional but recommended
TAVILY_API_KEY=tvly-...  # For web search
LANGSMITH_API_KEY=...     # For monitoring
```

5. **Review and customize configuration**
```bash
# Edit the investment thesis configuration
nano config/investment_thesis.yaml
```

## Quick Start

### Evaluate a Company

```bash
# Basic evaluation
python cli.py evaluate --company "Acme Corp"

# With sector and stage
python cli.py evaluate --company "TechCo" --sector SaaS --stage seed

# With custom focus
python cli.py evaluate --company "FinTech Inc" --query "Focus on unit economics and regulatory risk"
```

### View Configuration

```bash
python cli.py config
```

## Usage Examples

### Programmatic Usage

```python
from src.graph import get_graph
from src.state.schema import create_initial_state, InvestmentContext

# Create the graph
graph = get_graph()

# Configure your investment thesis
investment_context = InvestmentContext()

# Create initial state
state = create_initial_state(
    user_query="Evaluate this SaaS company for Series A investment",
    company_name="Example Corp",
    investment_context=investment_context,
)

# Add company details
state["company_data"]["sector"] = "SaaS"
state["company_data"]["stage"] = "series-a"

# Run the evaluation
config = {"configurable": {"thread_id": "eval-001"}}
result = graph.invoke(state, config=config)

# Access findings
market_analysis = result["market_data"]
due_diligence = result["due_diligence"]
```

### Streaming Execution

```python
# Stream for real-time updates
for event in graph.stream(state, config=config, stream_mode="values"):
    messages = event.get("messages", [])
    if messages:
        print(messages[-1].content)
```

### With Checkpointing

```python
from src.graph import get_graph

# Use PostgreSQL checkpointing for production
graph = get_graph(use_postgres=True, database_url="postgresql://...")

# Run with checkpointing
config = {"configurable": {"thread_id": "investment-eval-001"}}
result = graph.invoke(state, config=config)

# Later, resume from checkpoint
saved_state = graph.get_state(config)
# Continue execution...
```

## Configuration

### Investment Thesis Customization

The system adapts to your firm's specific investment approach through `config/investment_thesis.yaml`:

```yaml
# Stage preferences
stage_preferences:
  - name: "seed"
    min_check_size: 500000
    max_check_size: 2000000
    target_ownership: 15.0
    priority: 1

# Sector expertise
sector_preferences:
  - name: "SaaS"
    expertise_level: "high"
    specific_guidance: "Focus on Rule of 40 trajectory..."

# Evaluation criteria with weights
market_criteria:
  - name: "TAM Size"
    weight: 30
    threshold: 1000000000
    required: true
    guidance: "Minimum $1B TAM for seed stage..."

# Red flags and deal-breakers
red_flags:
  - name: "Founder Departure"
    severity: "blocking"
    description: "Founding team member left within last 6 months"
```

See `config/investment_thesis.yaml` for the complete schema.

## Project Structure

```
capos/
├── src/
│   ├── agents/          # Agent implementations
│   │   ├── supervisor.py       # Supervisor coordinator
│   │   └── market_analysis.py  # Market analysis agent
│   ├── config/          # Configuration management
│   │   └── loader.py           # Config loader with Pydantic validation
│   ├── prompts/         # Prompt templates
│   │   └── templates.py        # COSTAR-based prompts
│   ├── state/           # State management
│   │   └── schema.py           # TypedDict state schema
│   ├── tools/           # Agent tools
│   │   └── search.py           # Web search & calculator tools
│   └── graph.py         # Main StateGraph definition
├── config/              # Configuration files
│   └── investment_thesis.yaml  # Investment thesis config
├── tests/               # Test suite
├── examples/            # Example scripts
├── cli.py              # Command-line interface
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_supervisor.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type checking
mypy src/
```

### Adding New Agents

1. Create agent file in `src/agents/your_agent.py`
2. Implement agent using ReAct pattern or custom logic
3. Add prompt template in `src/prompts/templates.py`
4. Register agent in `src/graph.py`
5. Update supervisor to route to new agent
6. Add tests in `tests/agents/test_your_agent.py`

Example:
```python
# src/agents/your_agent.py
from langgraph.prebuilt import create_react_agent
from src.state.schema import VCDigitalTwinState

class YourAgent:
    def __init__(self, config):
        self.config = config
        # Initialize LLM, tools, etc.

    def __call__(self, state: VCDigitalTwinState):
        # Agent logic
        # Return Command with routing and updates
        pass
```

## Roadmap

### Phase 2: Complete Due Diligence (Q2 2025)
- [ ] Financial Analysis Agent
- [ ] Technical Assessment Agent
- [ ] Team Evaluation Agent
- [ ] Legal Review Agent
- [ ] Parallel agent execution
- [ ] Comprehensive test coverage

### Phase 3: Portfolio Monitoring (Q3 2025)
- [ ] Performance Tracking Agent
- [ ] Milestone Monitoring Agent
- [ ] Portfolio Support Agent
- [ ] Automated data collection
- [ ] Portfolio dashboards

### Phase 4: Production Deployment (Q4 2025)
- [ ] Web interface
- [ ] CRM integrations (Affinity, Harmonic)
- [ ] Advanced security & compliance
- [ ] Multi-tenant support
- [ ] LP reporting automation

## Technical Details

### LangGraph Implementation

The system uses LangGraph's latest patterns:

- **StateGraph**: Type-safe state management with reducers
- **Command**: Dynamic routing with simultaneous state updates
- **create_react_agent**: Pre-built ReAct pattern for workers
- **Checkpointing**: State persistence for fault tolerance
- **Streaming**: Real-time execution monitoring

### State Management

State uses TypedDict with annotated reducers:

```python
class VCDigitalTwinState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]  # Auto-appends
    company_data: CompanyData
    financial_data: FinancialData
    market_data: MarketData
    # ... other fields
```

### Agent Coordination

Supervisor uses structured output for routing:

```python
class SupervisorDecision(BaseModel):
    next: str  # Agent name or "FINISH"
    reasoning: str
    task_description: str

# Supervisor returns Command for routing
return Command(goto=agent_name, update=state_updates)
```

## Performance & Costs

### Token Usage

- Typical market analysis: 5,000-10,000 tokens
- Complete due diligence: 30,000-50,000 tokens
- Cost per evaluation: $0.50-$2.00 (depending on model)

### Execution Time

- Market analysis only: 30-60 seconds
- Full due diligence: 3-5 minutes
- Portfolio monitoring: 1-2 minutes per company

### Optimization Tips

- Use GPT-4o-mini or Claude Haiku for simple tasks
- Enable caching for repeated analyses
- Batch portfolio monitoring operations
- Use PostgreSQL checkpointing in production

## Troubleshooting

### Common Issues

**Import errors:**
```bash
# Ensure src is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**API key errors:**
```bash
# Verify .env file exists and has valid keys
cat .env | grep API_KEY
```

**Config not found:**
```bash
# Check config file exists
ls config/investment_thesis.yaml
# Verify CONFIG_PATH environment variable
echo $CONFIG_PATH
```

**Graph execution errors:**
Enable debug mode:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

[Your License Here]

## Citation

If you use this system in your research or practice, please cite:

```bibtex
@software{vc_digital_twin,
  title = {VC Digital Twin: Multi-Agent Investment Evaluation System},
  author = {Your Name},
  year = {2025},
  url = {https://github.com/your-repo}
}
```

## Support

- Documentation: [docs/](docs/)
- Issues: [GitHub Issues](https://github.com/your-repo/issues)
- Discussions: [GitHub Discussions](https://github.com/your-repo/discussions)

## Acknowledgments

This system implements patterns and best practices from:

- Anthropic's multi-agent system guidelines
- LangGraph documentation and examples
- Established VC due diligence frameworks
- Production multi-agent deployments

---

**Built with LangGraph** | **Powered by Claude & GPT-4** | **Designed for VC Excellence**
