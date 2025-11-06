/**
 * Capital OS Module Registry
 *
 * Central registry for all Capital OS modules.
 * Each module is self-contained with its own UI, logic, and integration points.
 */

export interface ModuleDefinition {
  id: string
  name: string
  description: string
  version: string
  status: 'active' | 'development' | 'planned' | 'deprecated'
  path: string
  dependencies: string[]
  permissions: string[]
  routes?: {
    ui?: string
    api?: string
  }
}

export const moduleRegistry: ModuleDefinition[] = [
  {
    id: 'vc-digital-twin',
    name: 'VC Digital Twin',
    description: 'Multi-agent investment evaluation system using LangGraph',
    version: '1.0.0',
    status: 'active',
    path: '/modules/vc-digital-twin',
    dependencies: ['mcp-server', 'langgraph'],
    permissions: ['read:companies', 'write:analysis', 'execute:agents'],
    routes: {
      ui: '/modules/vc-digital-twin',
      api: '/api/modules/vc',
    },
  },
  {
    id: 'note-intelligence',
    name: 'Note Intelligence',
    description: 'Capture, process, and graduate knowledge from notes',
    version: '0.1.0',
    status: 'development',
    path: '/modules/note-intelligence',
    dependencies: ['neo4j', 'tesseract', 'supabase'],
    permissions: ['read:notes', 'write:knowledge-graph', 'execute:ocr'],
    routes: {
      ui: '/modules/note-intelligence',
      api: '/api/modules/notes',
    },
  },
  {
    id: 'spec-orchestrator',
    name: 'Specification Orchestrator',
    description: 'Company-as-code specification management and GitOps',
    version: '0.0.1',
    status: 'planned',
    path: '/modules/spec-orchestrator',
    dependencies: ['github', 'mcp-server'],
    permissions: ['read:specs', 'write:specs', 'execute:workflows'],
    routes: {
      ui: '/modules/spec-orchestrator',
      api: '/api/modules/specs',
    },
  },
  {
    id: 'agent-control',
    name: 'Agent Control Manager',
    description: 'Monitor, govern, and audit AI agent operations',
    version: '0.0.1',
    status: 'planned',
    path: '/modules/agent-control',
    dependencies: ['mcp-server', 'supabase'],
    permissions: ['read:agents', 'write:policies', 'execute:governance'],
    routes: {
      ui: '/modules/agent-control',
      api: '/api/modules/agents',
    },
  },
  {
    id: 'intelligence-dashboard',
    name: 'Intelligence Dashboard',
    description: 'Real-time metrics, cost tracking, and optimization insights',
    version: '0.0.1',
    status: 'planned',
    path: '/modules/intelligence-dashboard',
    dependencies: ['supabase', 'neo4j'],
    permissions: ['read:metrics', 'read:costs'],
    routes: {
      ui: '/modules/intelligence-dashboard',
      api: '/api/modules/dashboard',
    },
  },
  {
    id: 'knowledge-graph',
    name: 'Knowledge Graph Builder',
    description: 'Self-evolving organizational knowledge graph with hybrid RAG',
    version: '0.0.1',
    status: 'planned',
    path: '/modules/knowledge-graph',
    dependencies: ['neo4j', 'vector-db'],
    permissions: ['read:graph', 'write:graph', 'execute:queries'],
    routes: {
      api: '/api/modules/graph',
    },
  },
]

/**
 * Get module by ID
 */
export function getModule(id: string): ModuleDefinition | undefined {
  return moduleRegistry.find(m => m.id === id)
}

/**
 * Get active modules
 */
export function getActiveModules(): ModuleDefinition[] {
  return moduleRegistry.filter(m => m.status === 'active')
}

/**
 * Check if module has permission
 */
export function hasPermission(moduleId: string, permission: string): boolean {
  const module = getModule(moduleId)
  return module?.permissions.includes(permission) || false
}
