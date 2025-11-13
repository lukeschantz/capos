# Capital OS Repository Index

**Last Updated:** 2025-11-13
**Repository:** Capital OS - AI-native Intelligence & Orchestration Platform

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Reference](#quick-reference)
3. [Core Files](#core-files)
4. [Python Backend](#python-backend)
5. [Frontend Application](#frontend-application)
6. [Configuration](#configuration)
7. [Scripts & Tools](#scripts--tools)
8. [Examples & Tests](#examples--tests)
9. [File Type Summary](#file-type-summary)

---

## Overview

**What is this repository?**
Capital OS is a modular AI platform that combines a Next.js frontend with a Python LangGraph backend to create intelligent, autonomous systems. The first module is a VC Digital Twin that helps venture capitalists evaluate investment opportunities using multi-agent AI.

**Tech Stack:**
- Frontend: Next.js 14, React 18, TypeScript, Tailwind CSS
- Backend: Python, LangGraph, FastAPI, FastMCP
- Agents: OpenAI GPT-4, Anthropic Claude
- Tools: Web search (Tavily), PostgreSQL (optional)

**Total Files:** 47 tracked files
**Lines of Code:** ~6,000+ lines

---

## Quick Reference

### What Can I Run Right Now?

| Command | What It Does | Where It's Defined |
|---------|--------------|-------------------|
| `./scripts/setup.sh` | First-time setup: install dependencies, copy env files | `/scripts/setup.sh` |
| `./scripts/quick-start.sh` | Start both frontend and backend servers | `/scripts/quick-start.sh` |
| `npm run dev` | Start frontend (3000) + MCP server (8000) | `/package.json` |
| `python cli.py evaluate --company "Acme" --sector SaaS --stage seed` | Run company evaluation from CLI | `/cli.py` |
| `python cli.py config` | Display investment thesis configuration | `/cli.py` |
| `pytest tests/` | Run test suite | `requirements.txt` |

### Key Entry Points

| What You Want To Do | Start Here |
|---------------------|------------|
| Change investment strategy/criteria | `/config/investment_thesis.yaml` |
| Modify frontend UI | `/frontend/app/page.tsx` or `/modules/vc-digital-twin/index.tsx` |
| Add/modify agents | `/src/agents/*.py` |
| Change agent prompts | `/src/prompts/templates.py` |
| Add search/tools | `/src/tools/search.py` |
| Configure agent workflow | `/src/graph.py` |
| Set environment variables | `.env` (copy from `.env.example`) |

---

## Core Files

### Root Directory Files

#### `.env.example`
**Type:** Configuration template
**What it does:** Shows all environment variables you need to set up. Copy this to `.env` and fill in your API keys.

**Key variables:**
- LLM API keys (OpenAI, Anthropic, Google)
- Web search API key (Tavily)
- Database config
- Monitoring (LangSmith)
- Model selection

#### `cli.py`
**Type:** Python executable script
**What it does:** Command-line interface to run evaluations without the web UI. You can evaluate companies directly from your terminal.

**Main functions:**
- `evaluate` command: Analyze a company for investment
- `config` command: Display current investment thesis
- `setup_environment()`: Check that API keys are set
- `run_evaluation()`: Execute the multi-agent workflow
- `print_final_summary()`: Format and display results

**Example usage:**
```bash
python cli.py evaluate \
  --company "Acme Corp" \
  --sector SaaS \
  --stage seed \
  --query "Focus on competitive landscape"
```

#### `package.json`
**Type:** Node.js configuration
**What it does:** Defines npm scripts for running the entire platform. This is the orchestrator for development.

**Key scripts:**
- `npm run dev` - Runs frontend + backend together
- `npm run dev:frontend` - Just the Next.js UI (port 3000)
- `npm run dev:mcp` - Just the Python MCP server (port 8000)
- `npm run setup` - Calls setup.sh

#### `requirements.txt`
**Type:** Python dependencies
**What it does:** Lists all Python packages needed. Run `pip install -r requirements.txt` to install.

**Key packages:**
- `langgraph>=0.2.0` - Multi-agent orchestration framework
- `langchain>=0.3.0` - LLM abstraction layer
- `fastapi` - Web API framework
- `tavily-python` - Web search
- `pytest` - Testing

#### `README.md`
**Type:** Documentation
**What it does:** Main documentation with quick start, architecture overview, and development instructions.

#### `README-CAPITAL-OS.md`
**Type:** Documentation
**What it does:** High-level vision document explaining the modular Capital OS architecture and roadmap.

---

## Python Backend

### Agent System (`/src/`)

#### `/src/graph.py`
**Type:** Python module
**What it does:** Creates the LangGraph workflow that connects all agents together. This is the "brain" that orchestrates how agents talk to each other.

**Key functions:**
- `create_vc_digital_twin_graph()` - Builds the agent workflow
- `create_graph_with_postgres_checkpoint()` - Production version with database
- `get_graph()` - Gets a ready-to-use compiled graph

**How it works:**
1. Supervisor agent decides which worker agent to call next
2. Worker agent (e.g., market analysis) does its job
3. Results go back to supervisor
4. Supervisor decides next step or finishes

#### `/src/state/schema.py`
**Type:** Python module
**What it does:** Defines the data structures (state schema) that agents pass around. Think of it as the "shape" of all data in the system.

**Main classes:**
- `CompanyData` - Company info (name, website, sector, stage)
- `FinancialData` - Money stuff (revenue, burn rate, margins)
- `MarketData` - Market info (TAM, competitors, growth)
- `DueDiligenceStatus` - Due diligence progress tracking
- `VCDigitalTwinState` - The main state that contains everything

**Helper functions:**
- `create_initial_state()` - Start a new evaluation
- `add_audit_entry()` - Log what agents are doing
- `update_agent_task()` - Track agent progress

### Agents (`/src/agents/`)

#### `/src/agents/supervisor.py`
**Type:** Python agent class
**What it does:** The "manager" agent that orchestrates the workflow. It looks at the current state and decides which worker agent should run next.

**Key responsibilities:**
- Analyzes what information is still needed
- Routes to the right agent (market_analysis, financial_analysis, etc.)
- Synthesizes findings
- Decides when the evaluation is complete

**How it works:**
1. Reads current state
2. Generates a summary of what's been done
3. Uses an LLM to decide next step
4. Returns a Command: which agent to call next OR "FINISH"

#### `/src/agents/market_analysis.py`
**Type:** Python agent class
**What it does:** Analyzes the market opportunity for a company. It searches the web, calculates market sizes, and evaluates competition.

**Key responsibilities:**
- Estimate TAM (Total Addressable Market)
- Research competitors
- Evaluate market timing
- Identify opportunities and risks

**Tools it uses:**
- Web search (Tavily)
- Calculator (for market math)
- Company research
- Competitor intelligence

**Output:**
- Market analysis report
- TAM/SAM/SOM estimates
- Competitive landscape
- Growth rate
- Confidence levels

### Configuration (`/src/config/`)

#### `/src/config/loader.py`
**Type:** Python module
**What it does:** Loads and validates the investment thesis YAML file. Turns configuration into Python objects that agents can use.

**Key classes:**
- `StageConfig` - Investment stage preferences (check size, ownership)
- `SectorConfig` - Sector expertise and focus
- `EvaluationCriterion` - Weighted scoring criteria
- `RedFlag` - Deal-breakers to watch for
- `InvestmentThesisConfig` - Complete configuration

**Main class:**
- `ConfigLoader` - Singleton that loads config once and caches it

**Methods:**
- `load(filepath)` - Load from YAML/JSON
- `get_config()` - Get the loaded config
- `get_stage_config(stage)` - Get config for a specific stage
- `get_sector_config(sector)` - Get config for a specific sector

### Prompts (`/src/prompts/`)

#### `/src/prompts/templates.py`
**Type:** Python module
**What it does:** Generates dynamic prompts for all agents using the COSTAR framework (Context, Objective, Style, Tone, Audience, Response). Injects configuration into prompts.

**Main class:**
- `PromptTemplateManager` - Creates prompts for each agent

**Key methods:**
- `get_supervisor_prompt()` - For the orchestrator agent
- `get_market_analysis_prompt()` - For market sizing
- `get_financial_analysis_prompt()` - For financial analysis
- `get_team_evaluation_prompt()` - For founder assessment
- `get_portfolio_tracking_prompt()` - For portfolio monitoring

**Why this matters:** Changing prompts here changes how all agents behave.

### Tools (`/src/tools/`)

#### `/src/tools/search.py`
**Type:** Python module
**What it does:** Provides tools that agents can use, like web search and calculator.

**Main class:**
- `SearchToolkit` - Collection of search tools

**Tools provided:**
- `web_search` - General web search
- `company_research` - Company-specific search
- `market_research` - Market trends and data
- `competitor_research` - Competitor information
- `calculator` - Safe math evaluation

**How agents use it:** Agents can call these tools during their analysis to get real-time information.

### MCP Server (`/backend/mcp-server/`)

#### `/backend/mcp-server/server.py`
**Type:** FastMCP server application
**What it does:** Exposes the agents via HTTP API using the Model Context Protocol. This is what the frontend talks to.

**Port:** 8000

**Resources (read-only data):**
- `vc://portfolio` - Portfolio status
- `vc://market-reports` - Recent analyses
- `vc://investment-thesis` - Current configuration

**Tools (actions you can call):**

1. `analyze_market`
   - **Input:** company_name, sector, stage
   - **Output:** Market analysis report
   - **What it does:** Runs the market analysis agent

2. `run_due_diligence`
   - **Input:** company_name, focus_areas, depth
   - **Output:** Comprehensive due diligence report
   - **What it does:** Orchestrates multiple agents

3. `monitor_portfolio_company` (coming soon)
   - **Input:** company_name, metrics
   - **Output:** Portfolio tracking data

**Prompts:**
- `vc_analyst_prompt()` - General VC analyst assistant
- `market_research_prompt()` - Market research assistant

#### `/backend/mcp-server/requirements.txt`
**Type:** Python dependencies
**What it does:** Lists dependencies specific to the MCP server.

---

## Frontend Application

### Root Frontend Files (`/frontend/`)

#### `/frontend/package.json`
**Type:** Node.js configuration
**What it does:** Defines frontend dependencies and build scripts.

**Key scripts:**
- `dev` - Development server (port 3000)
- `build` - Production build
- `start` - Production server
- `lint` - Code quality check

**Key dependencies:**
- React 18.2 - UI framework
- Next.js 14 - React framework
- Tailwind CSS - Styling
- Radix UI - UI primitives
- Lucide React - Icons
- TanStack Query - Data fetching
- Zustand - State management

#### `/frontend/app/page.tsx`
**Type:** React component (TypeScript)
**What it does:** The home page that shows the module gallery. This is what you see when you visit http://localhost:3000

**What's on the page:**
- Platform header
- 6 module cards:
  - VC Digital Twin (active - you can click it)
  - Note Intelligence (in development)
  - Spec Orchestrator (planned)
  - Agent Control Manager (planned)
  - Intelligence Dashboard (planned)
  - Knowledge Graph Builder (planned)
- System status:
  - MCP Server: Connected ✅
  - Supabase: Pending Setup ⏳
  - Neo4j: Pending Setup ⏳

#### `/frontend/app/layout.tsx`
**Type:** React component (TypeScript)
**What it does:** Root layout that wraps all pages. Sets up fonts, metadata, and overall page structure.

#### `/frontend/app/globals.css`
**Type:** CSS stylesheet
**What it does:** Global styles and Tailwind CSS configuration.

#### `/frontend/app/modules/vc-digital-twin/page.tsx`
**Type:** Next.js page route
**What it does:** Page route that renders the VC Digital Twin module. When you click "VC Digital Twin" on the home page, you go here.

### Module Components (`/modules/`)

#### `/modules/registry.ts`
**Type:** TypeScript module
**What it does:** Central registry of all modules in the platform. Defines metadata for each module.

**Module definitions include:**
- ID and name
- Description
- Status (active, development, planned)
- Icon
- Dependencies
- Permissions
- Phase number

**Utility functions:**
- `getModule(id)` - Get module by ID
- `getActiveModules()` - Get only active modules
- `hasPermission(moduleId, permission)` - Check permissions

#### `/modules/vc-digital-twin/index.tsx`
**Type:** React component (TypeScript)
**What it does:** The main UI for the VC Digital Twin module. This is the actual interface where you evaluate companies.

**Features:**

1. **Search Bar:**
   - Company name input
   - Sector dropdown (Technology, SaaS, Fintech, Healthcare, AI/ML)
   - Stage dropdown (Pre-Seed, Seed, Series A, Series B)
   - Analyze button

2. **Pipeline Tab:**
   - Shows all companies you've analyzed
   - Status badges (analyzing, complete, error)
   - Market analysis results
   - TAM, growth rate, competitive landscape
   - Opportunities and risks
   - Action buttons (view full report, start due diligence)

3. **Research Tab:**
   - Coming in Phase 2
   - Industry analysis
   - Competitor research

4. **Due Diligence Tab:**
   - Coming in Phase 2
   - Financial analysis
   - Technical assessment
   - Team evaluation
   - Legal review

5. **Portfolio Tab:**
   - Key metrics display (Total AUM, Portfolio Cos, Avg Multiple, Exits)
   - Coming in Phase 3: Portfolio company tracking

6. **Agent Status Footer:**
   - Shows real-time status of agents:
     - Supervisor: Ready
     - Market Analysis: Ready
     - System: Operational

**How it works:**
1. User enters company info and clicks "Analyze"
2. Component calls MCP server: POST to http://localhost:8000/tools/analyze_market
3. Shows "analyzing..." status
4. When results come back, displays them in Pipeline tab
5. User can click "Full Report" or "Due Diligence" (coming soon)

**State management:**
- Uses React hooks (useState, useEffect)
- Stores companies array
- Tracks analyzing status
- Manages active tab

### UI Components (`/frontend/components/ui/`)

These are reusable UI components from shadcn/ui library:

#### `badge.tsx`
**What it does:** Colored badges for status indicators (e.g., "Complete", "In Progress")

#### `button.tsx`
**What it does:** Interactive buttons with different styles (default, outline, ghost, etc.)

#### `card.tsx`
**What it does:** Card containers with header, content, and footer sections

#### `input.tsx`
**What it does:** Text input fields

#### `progress.tsx`
**What it does:** Progress bars for loading states

#### `tabs.tsx`
**What it does:** Tab navigation (Pipeline, Research, Due Diligence, Portfolio)

---

## Configuration

### `/config/investment_thesis.yaml`
**Type:** YAML configuration file
**What it does:** THE MOST IMPORTANT CONFIG FILE. This defines your VC firm's investment strategy and drives all agent behavior.

**Sections:**

1. **Metadata**
   - Firm name: "Acme Ventures"
   - Version: 1.0
   - Last updated date

2. **Stage Preferences**
   - Pre-seed: $250K-$750K checks, 10% ownership target
   - Seed: $500K-$2M checks, 15% ownership target
   - Series A: $2M-$10M checks, 12% ownership target

3. **Sector Preferences**
   - SaaS: High expertise, priority focus
   - Fintech: Moderate expertise, selective
   - Healthcare Tech: Learning, cautious
   - Consumer Social: Avoid

4. **Geographic Scope**
   - Primary: United States, Canada
   - Secondary: Western Europe

5. **Fund Strategy**
   - Fund size: $100M
   - Deployment period: 3 years
   - Reserve ratio: 50%
   - Target portfolio size: 25 companies
   - Portfolio concentration: Moderate

6. **Evaluation Criteria** (weighted scoring)

   **Team (35% weight):**
   - Founder-market fit: 40%
   - Technical capability: 30%
   - Previous experience: 20%
   - Team completeness: 10%

   **Market (30% weight):**
   - TAM size: 30%
   - Market growth rate: 25%
   - Market timing: 25%
   - Competitive dynamics: 20%

   **Product (20% weight):**
   - Product differentiation: 35%
   - Product-market fit: 35%
   - Technical scalability: 20%
   - IP/moat: 10%

   **Financial (10% weight):**
   - Revenue trajectory: 30%
   - LTV:CAC ratio: 25%
   - Gross margin: 20%
   - Burn multiple: 15%
   - Capital efficiency: 10%

   **Traction (5% weight):**
   - Growth rate: 35%
   - Retention metrics: 30%
   - Customer concentration: 20%
   - Sales efficiency: 15%

7. **Red Flags**

   **Blocking (deal-breakers):**
   - Founder departure
   - Undisclosed litigation
   - IP disputes
   - Regulatory violations

   **Concerning (need mitigation):**
   - Customer concentration >40%
   - Negative gross margins
   - Team turnover >30%
   - Missed projections >50%

   **Warning (watch closely):**
   - High burn rate
   - Single customer dependency
   - Unproven market
   - Intense competition

8. **Agent Configuration**
   - Supervisor: gpt-4o, temperature 0.3
   - Market Analysis: gpt-4o, temperature 0.5, max 8192 tokens
   - Financial Analysis: gpt-4o, temperature 0.2
   - Team Evaluation: gpt-4o, temperature 0.4
   - Portfolio Tracking: gpt-4o-mini, temperature 0.3

**How to customize:**
- Edit this file to change investment strategy
- Agents will automatically use new config
- No code changes needed

---

## Scripts & Tools

### `/scripts/setup.sh`
**Type:** Bash script
**What it does:** First-time setup script. Run this once when you first clone the repo.

**What it does:**
1. Checks Python 3 is installed
2. Checks Node.js is installed
3. Installs Python dependencies (requirements.txt)
4. Installs FastMCP dependencies
5. Installs root npm dependencies
6. Installs frontend npm dependencies
7. Copies .env.example to .env (if not exists)
8. Copies frontend/.env.example to frontend/.env.local (if not exists)
9. Prints next steps

**Usage:**
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### `/scripts/quick-start.sh`
**Type:** Bash script
**What it does:** Quick start development servers. Run this every time you want to start working.

**What it does:**
1. Checks if setup.sh has been run
2. Verifies API keys are set in .env
3. Starts frontend (port 3000) and MCP server (port 8000) together
4. Uses `npm run dev` which runs both with concurrently

**Usage:**
```bash
./scripts/quick-start.sh
```

---

## Examples & Tests

### Examples (`/examples/`)

#### `/examples/simple_evaluation.py`
**Type:** Python example script
**What it does:** Demonstrates how to use the evaluation system programmatically.

**What it shows:**
1. How to create the multi-agent graph
2. How to initialize evaluation state
3. How to run with streaming output
4. How to display results

**Usage:**
```bash
python examples/simple_evaluation.py
```

#### `/examples/config_early_stage.yaml`
**Type:** YAML configuration
**What it does:** Example configuration for an early-stage focused fund (pre-seed, seed only)

#### `/examples/config_fintech_focused.yaml`
**Type:** YAML configuration
**What it does:** Example configuration for a fintech-focused fund

### Tests (`/tests/`)

#### `/tests/test_supervisor.py`
**Type:** Pytest test suite
**What it does:** Unit tests for the Supervisor Agent

**Test cases:**
1. `test_supervisor_initialization` - Verify agent is created properly
2. `test_supervisor_routing_decision_structure` - Check Command output structure
3. `test_supervisor_completion_routing` - Verify it returns END when done
4. `test_supervisor_audit_trail` - Check audit logging works
5. `test_supervisor_invalid_agent_handling` - Graceful error handling

**Usage:**
```bash
pytest tests/test_supervisor.py -v
```

#### `/tests/__init__.py`
**Type:** Python package marker
**What it does:** Makes tests directory a Python package

#### `/tests/agents/__init__.py`
**Type:** Python package marker
**What it does:** Makes tests/agents directory a Python package

#### `/tests/integration/__init__.py`
**Type:** Python package marker
**What it does:** Makes tests/integration directory a Python package (future integration tests)

---

## File Type Summary

### By Category

**Configuration Files (7):**
- `.env.example` - Environment variables template
- `package.json` - Root npm configuration
- `frontend/package.json` - Frontend npm configuration
- `config/investment_thesis.yaml` - Investment strategy
- `frontend/tsconfig.json` - TypeScript config
- `frontend/next.config.js` - Next.js config
- `frontend/tailwind.config.ts` - Tailwind config

**Python Agent Files (8):**
- `src/graph.py` - LangGraph workflow
- `src/state/schema.py` - State definitions
- `src/agents/supervisor.py` - Supervisor agent
- `src/agents/market_analysis.py` - Market analysis agent
- `src/config/loader.py` - Config loader
- `src/prompts/templates.py` - Prompt templates
- `src/tools/search.py` - Search and calculator tools
- `backend/mcp-server/server.py` - MCP server

**Frontend Files (11):**
- `frontend/app/page.tsx` - Home page
- `frontend/app/layout.tsx` - Root layout
- `frontend/app/globals.css` - Global styles
- `frontend/app/modules/vc-digital-twin/page.tsx` - VC module page
- `modules/registry.ts` - Module registry
- `modules/vc-digital-twin/index.tsx` - VC module component
- `frontend/components/ui/badge.tsx` - Badge component
- `frontend/components/ui/button.tsx` - Button component
- `frontend/components/ui/card.tsx` - Card component
- `frontend/components/ui/input.tsx` - Input component
- `frontend/components/ui/tabs.tsx` - Tabs component

**Scripts (3):**
- `cli.py` - Command-line interface
- `scripts/setup.sh` - Initial setup
- `scripts/quick-start.sh` - Start dev servers

**Examples & Tests (4):**
- `examples/simple_evaluation.py` - Example usage
- `examples/config_early_stage.yaml` - Example config
- `examples/config_fintech_focused.yaml` - Example config
- `tests/test_supervisor.py` - Supervisor tests

**Documentation (3):**
- `README.md` - Main documentation
- `README-CAPITAL-OS.md` - Platform documentation
- `.gitignore` - Git ignore rules

**Dependencies (3):**
- `requirements.txt` - Python dependencies
- `backend/mcp-server/requirements.txt` - MCP server dependencies
- Various package.json files

### By Language

- **Python:** 15 files (~2,500 lines)
- **TypeScript/TSX:** 12 files (~2,000 lines)
- **Configuration:** 10 files (YAML, JSON, etc.)
- **Shell Scripts:** 2 files (~150 lines)
- **Documentation:** 3 files (~1,000 lines)
- **CSS:** 1 file (~200 lines)

---

## What's Working vs. What's Planned

### ✅ Working Now (Phase 1 Complete)

**Infrastructure:**
- Next.js frontend with module gallery
- FastMCP server exposing agents
- LangGraph multi-agent orchestration
- Setup and quick-start scripts
- Module registry system

**VC Digital Twin - MVP:**
- Market analysis agent
- Web search capability
- Market sizing (TAM estimation)
- Competitive analysis
- Investment thesis configuration
- CLI interface
- Basic web UI with Pipeline tab

### 🚧 In Development (Phase 2)

**VC Digital Twin - Complete:**
- Financial analysis agent
- Team evaluation agent
- Technical assessment agent
- Legal review agent
- Full due diligence reports
- Research tab functionality
- Due Diligence tab functionality

### 📋 Planned (Phase 3+)

**Portfolio Tracking:**
- Portfolio company monitoring
- Performance metrics
- Alert system

**New Modules:**
- Note Intelligence (OCR, knowledge graphs)
- Specification Orchestrator (PRD generation)
- Agent Control Manager (agent lifecycle)
- Intelligence Dashboard (analytics)
- Knowledge Graph Builder (Neo4j integration)

---

## Common Workflows

### 1. Evaluate a Company (Web UI)
1. Start servers: `./scripts/quick-start.sh`
2. Open browser: http://localhost:3000
3. Click "VC Digital Twin"
4. Enter company name, select sector and stage
5. Click "Analyze Company"
6. Wait for results in Pipeline tab

### 2. Evaluate a Company (CLI)
```bash
python cli.py evaluate \
  --company "Stripe" \
  --sector Fintech \
  --stage "Series A" \
  --query "Focus on competitive moat"
```

### 3. Change Investment Strategy
1. Edit `/config/investment_thesis.yaml`
2. Change stage preferences, sectors, or criteria
3. Restart MCP server (Ctrl+C, then restart)
4. New evaluations will use updated strategy

### 4. Add a New Agent
1. Create new file in `/src/agents/` (e.g., `financial_analysis.py`)
2. Implement agent class with `process()` method
3. Add to graph in `/src/graph.py`
4. Add routing logic in supervisor
5. Add prompt template in `/src/prompts/templates.py`

### 5. Modify the UI
1. Edit `/modules/vc-digital-twin/index.tsx`
2. Change component code
3. Save (hot reload will update browser)

### 6. Add a New Tool
1. Edit `/src/tools/search.py`
2. Add new tool function
3. Register in `SearchToolkit.get_tools()`
4. Agents can now use it

---

## Troubleshooting

### "Import Error: No module named..."
→ Run `pip install -r requirements.txt`

### "Cannot find module 'react'"
→ Run `cd frontend && npm install`

### "API key not found"
→ Copy `.env.example` to `.env` and add your keys

### Frontend won't connect to backend
→ Check MCP server is running on port 8000

### Agents returning errors
→ Check API keys are valid and have credits

### Tests failing
→ Run `pytest tests/ -v` to see detailed errors

---

## Key Insights for Product Workflows

### What's Production-Ready

**Stable Components:**
- Module registry system (`/modules/registry.ts`)
- Configuration loader (`/src/config/loader.py`)
- State schema (`/src/state/schema.py`)
- Prompt templates (`/src/prompts/templates.py`)
- Search tools (`/src/tools/search.py`)
- MCP server (`/backend/mcp-server/server.py`)
- Setup scripts (`/scripts/`)

### What Needs More Work

**In Progress:**
- Additional agents (financial, team, technical, legal)
- Full due diligence workflow
- Report generation
- Portfolio tracking

**Gaps:**
- No authentication yet
- No database persistence (optional PostgreSQL exists)
- No user management
- No API rate limiting
- No production deployment config

### Recommended Migration Path

1. **Phase 1 → Production:**
   - Add authentication (Supabase)
   - Add database persistence
   - Deploy MCP server to cloud
   - Deploy frontend to Vercel

2. **Complete Phase 2:**
   - Finish remaining VC agents
   - Full due diligence reports
   - PDF export functionality

3. **Add New Modules (Phase 3+):**
   - Note Intelligence
   - Spec Orchestrator
   - etc.

---

## Dependencies Map

### Frontend Depends On:
- MCP Server (port 8000)
- Module registry
- shadcn/ui components

### MCP Server Depends On:
- Python agents (LangGraph)
- Configuration (investment_thesis.yaml)
- LLM API keys

### Agents Depend On:
- LangGraph framework
- LangChain LLMs
- Search tools (Tavily)
- Configuration system
- Prompt templates

### Configuration Depends On:
- YAML file (`config/investment_thesis.yaml`)

---

## Quick File Lookup

Need to find something fast? Use this table:

| I need to... | Look in... |
|--------------|------------|
| Change investment criteria | `/config/investment_thesis.yaml` |
| Change what agents say | `/src/prompts/templates.py` |
| Add a new agent | `/src/agents/*.py` + `/src/graph.py` |
| Change the UI | `/modules/vc-digital-twin/index.tsx` |
| Change the home page | `/frontend/app/page.tsx` |
| Add a new module | `/modules/registry.ts` + create new module |
| Change agent workflow | `/src/graph.py` |
| Add search tools | `/src/tools/search.py` |
| Change state structure | `/src/state/schema.py` |
| Set environment variables | `.env` |
| Run evaluations from terminal | `cli.py` |
| Set up first time | `scripts/setup.sh` |
| Start dev servers | `scripts/quick-start.sh` |
| See example usage | `examples/simple_evaluation.py` |
| Run tests | `tests/test_supervisor.py` |

---

## Architecture Diagram (ASCII)

```
┌─────────────────────────────────────────────────────────┐
│                    USER BROWSER                          │
│              http://localhost:3000                       │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              NEXT.JS FRONTEND                            │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Home Page (Module Gallery)                      │   │
│  │  - VC Digital Twin ✅                            │   │
│  │  - Note Intelligence 🚧                          │   │
│  │  - 4 more modules 📋                             │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │  VC Digital Twin Module                          │   │
│  │  - Search bar                                    │   │
│  │  - Pipeline tab                                  │   │
│  │  - Research tab                                  │   │
│  │  - Due Diligence tab                             │   │
│  │  - Portfolio tab                                 │   │
│  └─────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP POST
                       │ /tools/analyze_market
                       ▼
┌─────────────────────────────────────────────────────────┐
│              FASTMCP SERVER                              │
│              http://localhost:8000                       │
│  ┌─────────────────────────────────────────────────┐   │
│  │  MCP Tools:                                      │   │
│  │  - analyze_market                                │   │
│  │  - run_due_diligence                             │   │
│  │  - monitor_portfolio_company                     │   │
│  └─────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              LANGGRAPH MULTI-AGENT SYSTEM                │
│  ┌─────────────────────────────────────────────────┐   │
│  │         SUPERVISOR AGENT (Orchestrator)          │   │
│  │         - Routes to worker agents                │   │
│  │         - Synthesizes findings                   │   │
│  │         - Decides next steps                     │   │
│  └───┬────────────────────────────────────────┬────┘   │
│      │                                         │         │
│      ▼                                         ▼         │
│  ┌────────────────┐                    ┌────────────┐  │
│  │ MARKET         │                    │ FINANCIAL  │  │
│  │ ANALYSIS       │                    │ ANALYSIS   │  │
│  │ AGENT ✅       │                    │ AGENT 🚧   │  │
│  │ - TAM          │                    │ - Revenue  │  │
│  │ - Competition  │                    │ - Metrics  │  │
│  │ - Growth       │                    │ - Burn     │  │
│  └────────────────┘                    └────────────┘  │
│      │                                         │         │
│      ▼                                         ▼         │
│  ┌────────────────┐                    ┌────────────┐  │
│  │ TEAM           │                    │ TECHNICAL  │  │
│  │ EVALUATION     │                    │ ASSESSMENT │  │
│  │ AGENT 🚧       │                    │ AGENT 🚧   │  │
│  │ - Founders     │                    │ - Tech     │  │
│  │ - Experience   │                    │ - IP       │  │
│  └────────────────┘                    └────────────┘  │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              EXTERNAL SERVICES                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   OpenAI     │  │   Anthropic  │  │    Tavily    │ │
│  │   GPT-4o     │  │    Claude    │  │  Web Search  │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐                    │
│  │  PostgreSQL  │  │  LangSmith   │                    │
│  │ (Optional)   │  │ Monitoring   │                    │
│  └──────────────┘  └──────────────┘                    │
└─────────────────────────────────────────────────────────┘
```

---

## Summary Stats

- **Total Files:** 47
- **Python Files:** 15
- **TypeScript/React Files:** 12
- **Configuration Files:** 10
- **Scripts:** 2
- **Documentation Files:** 3
- **Test Files:** 1 test suite (5 test cases)
- **Agents Implemented:** 2 (Supervisor, Market Analysis)
- **Agents Planned:** 4 (Financial, Team, Technical, Legal)
- **Modules Active:** 1 (VC Digital Twin)
- **Modules Planned:** 5 more
- **Lines of Code:** ~6,000+
- **External APIs:** 4 (OpenAI, Anthropic, Tavily, LangSmith)

---

**End of Repository Index**

*This index is accurate as of 2025-11-13. For the most up-to-date information, check the actual files or run `git log` to see recent changes.*
