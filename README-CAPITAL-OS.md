# Capital OS - Intelligence & Orchestration Platform

> **Strawman Prototype**: A functional AI-native platform for rapid experimentation and iteration

Capital OS is a modular platform that creates self-evolving organizational intelligence through micro-UIs, agent orchestration, and knowledge graph infrastructure. Built for speed and flexibility, it combines Next.js frontend, Python MCP backend, and existing LangGraph agents.

## 🎯 Vision

Transform specifications, notes, and data into actionable intelligence through:
- **Modular Architecture**: Self-contained micro UIs for each capability
- **Agent Orchestration**: Multi-agent systems powered by LangGraph
- **Knowledge Evolution**: Information graduates from notes → AI → deterministic code
- **Company as Code**: GitOps-driven specifications and workflows

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
│  ┌────────────────────────────────────────────┐        │
│  │  Resources  │  Tools  │  Prompts           │        │
│  └────────────────────────────────────────────┘        │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│         Existing LangGraph Agents (Python)              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │Supervisor│  │  Market  │  │Financial │  ...        │
│  │  Agent   │  │ Analysis │  │ Analysis │             │
│  └──────────┘  └──────────┘  └──────────┘             │
└─────────────────────────────────────────────────────────┘
```

## 📦 Current Modules

### 1. VC Digital Twin (Active ✅)
**Status**: Phase 1 Complete
**Location**: `/modules/vc-digital-twin`

Multi-agent investment evaluation system using LangGraph supervisor-worker pattern.

**Features**:
- Market analysis agent (active)
- Investment thesis customization
- Real-time agent status updates
- Pipeline management UI

**Coming in Phase 2**:
- Financial analysis agent
- Technical assessment agent
- Team evaluation agent
- Legal review agent

### 2. Note Intelligence (Development 🚧)
**Status**: Planned
**Location**: `/modules/note-intelligence`

Capture and evolve knowledge from notes through intelligence graduation.

**Planned Features**:
- Camera + upload capture
- OCR (Tesseract.js or Google Vision)
- Intelligence tier classification
- Graduation pipeline (Foundation → SLM → Deterministic → Hardware)

### 3. Specification Orchestrator (Planned 📋)
**Status**: Planned
**Location**: `/modules/spec-orchestrator`

Company-as-code with GitOps workflow management.

### 4. Agent Control Manager (Planned 📋)
**Status**: Planned
**Location**: `/modules/agent-control`

Monitor, govern, and audit AI agent operations.

### 5. Intelligence Dashboard (Planned 📋)
**Status**: Planned
**Location**: `/modules/intelligence-dashboard`

Real-time metrics, cost tracking, and optimization insights.

### 6. Knowledge Graph Builder (Planned 📋)
**Status**: Planned
**Location**: `/modules/knowledge-graph`

Self-evolving knowledge graph with hybrid vector RAG (Neo4j + Vector DB).

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.10+
- **API Keys**: OpenAI or Anthropic (for agents)

### Installation

```bash
# 1. Clone and navigate to the repo
cd capos

# 2. Run the setup script
./scripts/setup.sh

# 3. Add your API keys to .env
# Edit .env and add:
# OPENAI_API_KEY=sk-...
# OR
# ANTHROPIC_API_KEY=sk-ant-...

# 4. Start everything
npm run dev
```

### Access the Platform

- **Frontend**: http://localhost:3000
- **VC Digital Twin**: http://localhost:3000/modules/vc-digital-twin
- **MCP Server**: http://localhost:8000

### Try It Out

1. Open http://localhost:3000/modules/vc-digital-twin
2. Enter a company name (e.g., "Stripe", "OpenAI", "Anthropic")
3. Select sector and stage
4. Click "Analyze"
5. Watch your existing LangGraph agents work through the new UI!

## 📁 Project Structure

```
capos/
├── frontend/                 # Next.js frontend
│   ├── app/                 # Next.js 14 app directory
│   │   ├── modules/        # Module pages
│   │   └── page.tsx        # Home page
│   ├── components/ui/      # shadcn/ui components
│   └── lib/                # Utilities
│
├── modules/                 # Self-contained modules
│   ├── vc-digital-twin/    # VC module UI
│   ├── note-intelligence/  # Note module (planned)
│   └── registry.ts         # Module registry
│
├── backend/                 # Backend services
│   └── mcp-server/         # Fast MCP server
│       ├── server.py       # MCP server wrapping agents
│       └── requirements.txt
│
├── src/                     # Existing VC Digital Twin agents
│   ├── agents/             # LangGraph agents
│   ├── graph.py            # StateGraph definition
│   └── ...
│
├── config/                  # Configuration
│   └── investment_thesis.yaml
│
├── scripts/                 # Setup and deployment scripts
│   ├── setup.sh           # Initial setup
│   └── quick-start.sh     # Start servers
│
└── package.json            # Monorepo scripts
```

## 🛠️ Development

### Available Commands

```bash
# Start both frontend and MCP server
npm run dev

# Start only frontend
npm run dev:frontend

# Start only MCP server
npm run dev:mcp

# Use original CLI (still works!)
npm run dev:agents
# or
python cli.py evaluate --company "Acme Corp"

# Build for production
npm run build

# Run tests
npm run test:python      # Python tests
npm run test:frontend    # Frontend tests
```

### Adding a New Module

1. **Create module folder**:
   ```bash
   mkdir -p modules/your-module
   ```

2. **Create the module component**:
   ```typescript
   // modules/your-module/index.tsx
   "use client"

   export function YourModule() {
     return <div>Your Module UI</div>
   }
   ```

3. **Create the page**:
   ```typescript
   // frontend/app/modules/your-module/page.tsx
   import { YourModule } from '@/modules/your-module'

   export default function Page() {
     return <YourModule />
   }
   ```

4. **Register the module**:
   ```typescript
   // modules/registry.ts
   {
     id: 'your-module',
     name: 'Your Module',
     version: '0.1.0',
     status: 'development',
     // ...
   }
   ```

### Module Development Guidelines

- **Self-contained**: Each module is independent
- **Consistent UI**: Use shadcn/ui components
- **MCP Integration**: Call MCP server for backend logic
- **State Management**: Use Zustand or React Query
- **TypeScript**: Fully typed

## 🔌 Integration Points

### MCP Server API

The MCP server exposes your LangGraph agents via HTTP:

```typescript
// Call market analysis
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

### Resources

```typescript
// Get investment thesis
GET http://localhost:8000/resources/vc://investment-thesis

// Get portfolio
GET http://localhost:8000/resources/vc://portfolio
```

## 🎨 Tech Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS
- **Components**: shadcn/ui (Radix)
- **State**: Zustand, React Query
- **Deployment**: Vercel

### Backend
- **MCP Server**: Fast MCP (Python)
- **Agents**: LangGraph + LangChain
- **API**: FastAPI
- **LLMs**: OpenAI GPT-4o, Anthropic Claude

### Infrastructure (Planned)
- **Auth**: Supabase
- **Database**: Supabase (PostgreSQL)
- **Knowledge Graph**: Neo4j Aura
- **Vector Store**: Supabase pgvector
- **Email**: Resend

## 📊 Development Phases

### ✅ Phase 1: Foundation (Complete)
- [x] Directory structure
- [x] MCP server wrapper
- [x] Next.js frontend
- [x] VC Digital Twin UI
- [x] Module registry
- [x] Setup scripts

### 🚧 Phase 2: VC Digital Twin Complete (In Progress)
- [ ] All due diligence agents
- [ ] Parallel agent execution
- [ ] Full report generation
- [ ] PDF exports

### 📋 Phase 3: Note Intelligence (Planned)
- [ ] Note capture UI
- [ ] OCR integration
- [ ] Intelligence classification
- [ ] Neo4j connection
- [ ] Graduation pipeline

### 📋 Phase 4: Orchestration (Planned)
- [ ] Spec parser
- [ ] GitOps integration
- [ ] Agent control manager
- [ ] Policy engine

### 📋 Phase 5: Production (Planned)
- [ ] Supabase auth
- [ ] Multi-tenancy
- [ ] Security audit
- [ ] Performance optimization
- [ ] Full deployment

## 🧪 Testing

```bash
# Python tests
pytest tests/

# Frontend tests
cd frontend && npm test

# E2E tests (planned)
npm run test:e2e
```

## 📚 Documentation

- [Original VC Digital Twin README](./README.md)
- [Module Development Guide](./docs/modules.md) (planned)
- [MCP Server API](./docs/mcp-api.md) (planned)
- [Deployment Guide](./docs/deployment.md) (planned)

## 🤝 Contributing

This is a strawman prototype designed for rapid iteration. Feel free to:
- Add new modules
- Improve existing UIs
- Extend agent capabilities
- Optimize performance

## 🔐 Environment Variables

### Required

```bash
# AI Models (at least one)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

### Optional

```bash
# Search
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
```

## 🎯 Next Steps

1. **Immediate**
   - Complete Phase 2 VC agents
   - Add agent streaming updates
   - Improve error handling

2. **This Week**
   - Build Note Intelligence UI
   - Integrate OCR
   - Set up Neo4j connection

3. **This Month**
   - Deploy to Vercel
   - Add Supabase auth
   - Build Spec Orchestrator

## 💡 Philosophy

**Speed over perfection**: This is a strawman to learn fast and iterate
**Modular by design**: Each piece works independently
**AI-native**: Agents and intelligence at the core
**Company as code**: Specifications drive everything
**Knowledge evolution**: Information gets smarter over time

## 📝 License

[Your License Here]

---

**Built with**: Next.js, Fast MCP, LangGraph, Anthropic Claude, OpenAI GPT-4
**Deployed on**: Vercel, Supabase, Neo4j Aura
**For**: Rapid prototyping and organizational intelligence
