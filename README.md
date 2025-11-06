# Capital OS - Intelligence & Orchestration Platform

> **AI-native modular platform** for building self-evolving organizational intelligence

Capital OS transforms specifications, notes, and data into actionable intelligence through modular micro-UIs, multi-agent orchestration, and knowledge graph infrastructure. Built for rapid prototyping and production deployment.

![Capital OS Architecture](https://img.shields.io/badge/Status-Strawman%20Prototype-blue)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-green)

---

## 🎯 What is Capital OS?

Capital OS is a **modular Intelligence & Orchestration platform** where:

- **Knowledge evolves**: Notes → AI analysis → Deterministic code → Hardware optimization
- **Agents orchestrate**: Multi-agent systems (LangGraph) handle complex workflows
- **Modules compose**: Self-contained micro-UIs for each capability
- **Specifications drive**: GitOps-style company-as-code approach
- **Intelligence graduates**: Information gets smarter and more cost-effective over time

**Philosophy**: Build fast, learn faster. This is a functional strawman designed for rapid iteration.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│           Next.js Frontend (Vercel)                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ VC Twin  │  │  Notes   │  │  Specs   │  ...        │
│  │ Micro UI │  │ Micro UI │  │ Micro UI │             │
│  └──────────┘  └──────────┘  └──────────┘             │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP/WebSocket
┌─────────────────────▼───────────────────────────────────┐
│          MCP Server (Fast MCP - Python)                 │
│  Resources  │  Tools  │  Prompts  │  Workflows         │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│         LangGraph Multi-Agent System                    │
│  Supervisor → Market Analysis → Due Diligence → ...    │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│  Infrastructure: Supabase, Neo4j, Vercel, Vector DB    │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.10+
- **API Key**: OpenAI or Anthropic

### Get Started in 3 Commands

```bash
# 1. Setup everything
./scripts/setup.sh

# 2. Add your API key to .env
echo "OPENAI_API_KEY=sk-your-key-here" >> .env

# 3. Start the platform
npm run dev
```

**Access Points:**
- 🌐 **Platform Home**: http://localhost:3000
- 💼 **VC Digital Twin**: http://localhost:3000/modules/vc-digital-twin
- 🤖 **MCP Server**: http://localhost:8000

### First Test

1. Open http://localhost:3000/modules/vc-digital-twin
2. Enter a company name: "Stripe", "OpenAI", "Anthropic"
3. Watch the multi-agent system analyze it in real-time!

---

## 📦 Modules

### 1. VC Digital Twin ✅ **Active**

**Multi-agent investment evaluation system with LangGraph supervisor-worker pattern**

**Features:**
- 🔍 **Market Analysis Agent**: TAM, growth rate, competitive landscape
- 🏢 **Due Diligence Workflows**: Financial, technical, team, legal (Phase 2)
- 📊 **Portfolio Monitoring**: Performance tracking and insights (Phase 3)
- ⚙️ **Investment Thesis Customization**: YAML-based configuration
- 📈 **Real-time Agent Status**: Watch agents work through the UI

**Current Status:**
- ✅ Supervisor agent with intelligent routing
- ✅ Market analysis agent operational
- ✅ Web search & calculator tools integrated
- ✅ Investment thesis configuration system
- 🚧 Financial, technical, team, legal agents (Phase 2)

**Tech:** LangGraph, Claude/GPT-4, Tavily Search, COSTAR prompting

**Location:** `/modules/vc-digital-twin`

---

### 2. Note Intelligence 🚧 **Planned**

**Capture knowledge from notes and graduate it through intelligence tiers**

**Planned Features:**
- 📸 **Capture**: Camera + upload with OCR (Tesseract.js / Google Vision)
- 🧠 **Classification**: Tier intelligence (Foundation LLM → SLM → Deterministic → Hardware)
- 📊 **Significance Scoring**: Automatically prioritize important information
- 🎓 **Graduation Pipeline**: Move knowledge down the cost curve
- 🔗 **Knowledge Graph**: Connect insights in Neo4j

**Graduation Path:**
```
Foundation Model (Claude Opus) → Cost: $$$
    ↓ Extract patterns, create rules
Small Language Model (Llama 3) → Cost: $$
    ↓ Identify deterministic logic
Rule Engine (Python/TypeScript) → Cost: $
    ↓ Compile critical paths
FPGA/Hardware → Cost: ¢
```

**Location:** `/modules/note-intelligence`

---

### 3. Specification Orchestrator 📋 **Planned**

**Company-as-code: GitOps for organizational workflows**

**Planned Features:**
- 📝 Define company principles, workflows, agents in YAML/JSON
- 🔄 GitOps: Version control for organizational intelligence
- 🚀 Auto-execution: Specs trigger workflows and agent actions
- 🔍 Validation: Schema checking for specifications
- 📊 Impact tracking: See how specs affect operations

**Location:** `/modules/spec-orchestrator`

---

### 4. Agent Control Manager 📋 **Planned**

**Monitor, govern, and audit AI agent operations**

**Planned Features:**
- 📊 Agent registry and capability mapping
- 👁️ Real-time observability (OpenTelemetry)
- 💰 Cost tracking per agent/workflow
- 🔒 Policy engine and compliance tracking
- 📝 Complete audit logs

**Location:** `/modules/agent-control`

---

### 5. Intelligence Dashboard 📋 **Planned**

**Real-time metrics and optimization insights**

**Planned Features:**
- 💰 Cost savings from intelligence graduation
- 📊 Intelligence tier distribution
- ⚡ Processing queue metrics
- 🔍 Pattern detection and anomalies
- 💡 Optimization recommendations

**Location:** `/modules/intelligence-dashboard`

---

### 6. Knowledge Graph Builder 📋 **Planned**

**Self-evolving organizational knowledge graph with hybrid RAG**

**Planned Features:**
- 🗺️ Neo4j graph database
- 🔍 Hybrid vector + graph search
- 🤖 Auto-construction from notes and specs
- ⛏️ Pattern mining and optimization
- 🧠 RAG pipeline for context-aware answers

**Location:** `/modules/knowledge-graph`

---

## 📁 Project Structure

```
capos/
├── frontend/                 # Next.js 14 frontend
│   ├── app/
│   │   ├── modules/         # Module pages
│   │   │   └── vc-digital-twin/
│   │   ├── page.tsx         # Home with module gallery
│   │   └── layout.tsx
│   ├── components/ui/       # shadcn/ui components
│   └── lib/                 # Utilities
│
├── modules/                  # Self-contained module components
│   ├── vc-digital-twin/     # VC module UI
│   │   └── index.tsx
│   ├── note-intelligence/   # (Planned)
│   └── registry.ts          # Module definitions
│
├── backend/
│   └── mcp-server/          # Fast MCP server
│       ├── server.py        # Wraps LangGraph agents
│       └── requirements.txt
│
├── src/                      # LangGraph agents (existing)
│   ├── agents/
│   │   ├── supervisor.py
│   │   └── market_analysis.py
│   ├── graph.py             # StateGraph definition
│   ├── state/
│   │   └── schema.py
│   ├── config/
│   │   └── loader.py
│   └── tools/
│
├── config/
│   └── investment_thesis.yaml  # VC thesis configuration
│
├── scripts/
│   ├── setup.sh             # One-time setup
│   └── quick-start.sh       # Start servers
│
├── tests/                    # Test suite
│   ├── agents/
│   └── integration/
│
├── package.json              # Monorepo scripts
└── README.md                 # This file
```

---

## 🛠️ Development

### Available Commands

```bash
# Start everything (frontend + MCP server)
npm run dev

# Start individually
npm run dev:frontend         # Next.js on :3000
npm run dev:mcp              # MCP server on :8000
npm run dev:agents           # Original CLI interface

# Build & deploy
npm run build                # Build frontend
npm run start                # Production server

# Testing
npm run test:python          # Python tests (pytest)
npm run test:frontend        # Frontend tests

# Setup
npm run setup                # Run setup script
npm run install:all          # Install all dependencies
```

### Original CLI Still Works

```bash
# Use the original command-line interface
python cli.py evaluate --company "Acme Corp"
python cli.py evaluate --company "TechCo" --sector SaaS --stage seed
python cli.py config  # View investment thesis
```

---

## 🎨 Tech Stack

### Frontend
- **Framework**: Next.js 14 (App Router, React Server Components)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Components**: shadcn/ui (Radix UI primitives)
- **State**: Zustand, React Query
- **Deployment**: Vercel

### Backend
- **MCP Server**: Fast MCP (Python)
- **Agent Framework**: LangGraph + LangChain
- **Web API**: FastAPI
- **LLMs**: Anthropic Claude, OpenAI GPT-4o
- **Search**: Tavily API

### Infrastructure (Planned)
- **Authentication**: Supabase Auth
- **Database**: Supabase (PostgreSQL)
- **Knowledge Graph**: Neo4j Aura
- **Vector Store**: Supabase pgvector
- **Email**: Resend
- **Monitoring**: LangSmith, OpenTelemetry

---

## 📊 Development Roadmap

### ✅ Phase 1: Foundation (Complete)
- [x] Modular architecture setup
- [x] Next.js frontend with module system
- [x] MCP server wrapping LangGraph agents
- [x] VC Digital Twin UI (market analysis)
- [x] Setup and development scripts
- [x] Documentation

### 🚧 Phase 2: VC Digital Twin Complete (Current)
- [ ] Financial analysis agent
- [ ] Technical assessment agent
- [ ] Team evaluation agent
- [ ] Legal review agent
- [ ] Parallel agent execution
- [ ] Full report generation with exports
- [ ] Agent streaming updates

### 📋 Phase 3: Note Intelligence (Next)
- [ ] Note capture UI (camera + upload)
- [ ] OCR integration (Tesseract.js)
- [ ] Intelligence tier classification
- [ ] Neo4j connection and schema
- [ ] Graduation pipeline implementation
- [ ] Hybrid RAG setup

### 📋 Phase 4: Orchestration & Control (Future)
- [ ] Specification parser and executor
- [ ] GitOps integration
- [ ] Agent control manager
- [ ] Policy engine
- [ ] Cost tracking system
- [ ] Intelligence dashboard

### 📋 Phase 5: Production & Scale (Future)
- [ ] Supabase authentication
- [ ] Multi-tenancy support
- [ ] Security audit and hardening
- [ ] Performance optimization
- [ ] Load testing
- [ ] Complete deployment automation

---

## 🔌 Integration: MCP Server API

The MCP server exposes LangGraph agents via HTTP:

### Analyze Market

```typescript
const response = await fetch('http://localhost:8000/tools/analyze_market', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    company_name: 'Acme Corp',
    sector: 'SaaS',
    stage: 'seed',
  })
})
```

### Get Resources

```bash
# Investment thesis
GET http://localhost:8000/resources/vc://investment-thesis

# Portfolio overview
GET http://localhost:8000/resources/vc://portfolio

# Market reports
GET http://localhost:8000/resources/vc://market-reports
```

---

## 🧩 Adding a New Module

### 1. Create Module Component

```typescript
// modules/your-module/index.tsx
"use client"

export function YourModule() {
  return (
    <div>
      <h1>Your Module</h1>
      {/* Your module UI */}
    </div>
  )
}
```

### 2. Create Page Route

```typescript
// frontend/app/modules/your-module/page.tsx
import { YourModule } from '@/modules/your-module'

export default function Page() {
  return <YourModule />
}
```

### 3. Register Module

```typescript
// modules/registry.ts
{
  id: 'your-module',
  name: 'Your Module',
  version: '0.1.0',
  status: 'development',
  path: '/modules/your-module',
  dependencies: ['mcp-server'],
  permissions: ['read:data', 'write:data'],
}
```

### 4. Add MCP Tools (Optional)

```python
# backend/mcp-server/server.py
@mcp.tool()
async def your_module_action(request: YourRequest) -> Dict[str, Any]:
    """Your module's backend logic"""
    return {"result": "success"}
```

---

## 🔐 Environment Variables

### Required

```bash
# AI Models (at least one)
OPENAI_API_KEY=sk-...
# OR
ANTHROPIC_API_KEY=sk-ant-...
```

### Optional

```bash
# Search (recommended for VC module)
TAVILY_API_KEY=tvly-...

# Monitoring
LANGSMITH_API_KEY=...

# Database (Phase 3+)
DATABASE_URL=postgresql://...

# Neo4j (Phase 3+)
NEO4J_URI=neo4j+s://...
NEO4J_USER=neo4j
NEO4J_PASSWORD=...

# Supabase (Phase 2+)
NEXT_PUBLIC_SUPABASE_URL=...
NEXT_PUBLIC_SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_ROLE_KEY=...

# Feature Flags
NEXT_PUBLIC_ENABLE_VC_MODULE=true
NEXT_PUBLIC_ENABLE_NOTE_INTELLIGENCE=false
```

---

## 🧪 Testing

```bash
# Python tests
pytest tests/
pytest tests/ --cov=src  # With coverage

# Frontend tests
cd frontend && npm test

# Integration tests
pytest tests/integration/

# Type checking
mypy src/
cd frontend && npm run type-check
```

---

## 📚 Documentation

- **Architecture Overview**: This README
- **Module Development**: `docs/modules.md` (planned)
- **MCP Server API**: `docs/mcp-api.md` (planned)
- **Deployment Guide**: `docs/deployment.md` (planned)
- **Original VC Twin Docs**: See `src/` directory

---

## 🎯 Design Principles

1. **Modular by Design**: Each capability is a self-contained module
2. **Agent-First**: Multi-agent systems orchestrate complex workflows
3. **Knowledge Evolution**: Information graduates from expensive → cheap
4. **Company as Code**: Specifications drive everything
5. **Speed over Perfection**: Strawman for rapid learning and iteration

---

## 🤝 Contributing

This is a strawman prototype built for rapid iteration. Contributions welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

**Areas of Interest:**
- New modules (Spec Orchestrator, Note Intelligence, etc.)
- Additional VC due diligence agents
- UI/UX improvements
- Performance optimizations
- Documentation

---

## 📝 License

[Your License Here]

---

## 🙏 Acknowledgments

Built with:
- **LangGraph** - Multi-agent orchestration framework
- **Next.js** - React framework by Vercel
- **Fast MCP** - Model Context Protocol server
- **shadcn/ui** - Beautiful component library
- **Anthropic Claude** & **OpenAI GPT-4** - Foundation models

Inspired by:
- Anthropic's multi-agent system guidelines
- Company-as-code principles
- Intelligence graduation concepts
- Modern web development patterns

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/capos/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/capos/discussions)
- **Documentation**: See `/docs` (coming soon)

---

**Capital OS** - Building intelligence that evolves 🚀
