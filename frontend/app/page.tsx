import Link from 'next/link'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import {
  TrendingUp,
  FileText,
  Sparkles,
  Users,
  BarChart3,
  Database,
  ArrowRight
} from 'lucide-react'

export default function Home() {
  const modules = [
    {
      id: 'vc-digital-twin',
      name: 'VC Digital Twin',
      description: 'AI-powered investment analysis and portfolio management',
      icon: TrendingUp,
      status: 'active',
      href: '/modules/vc-digital-twin',
    },
    {
      id: 'note-intelligence',
      name: 'Note Intelligence',
      description: 'Capture, process, and evolve knowledge from notes',
      icon: FileText,
      status: 'development',
      href: '/modules/note-intelligence',
    },
    {
      id: 'spec-orchestrator',
      name: 'Specification Orchestrator',
      description: 'Company-as-code specification management',
      icon: Sparkles,
      status: 'planned',
      href: '#',
    },
    {
      id: 'agent-control',
      name: 'Agent Control Manager',
      description: 'Monitor and govern AI agent operations',
      icon: Users,
      status: 'planned',
      href: '#',
    },
    {
      id: 'intelligence-dashboard',
      name: 'Intelligence Dashboard',
      description: 'Real-time metrics and optimization insights',
      icon: BarChart3,
      status: 'planned',
      href: '#',
    },
    {
      id: 'knowledge-graph',
      name: 'Knowledge Graph Builder',
      description: 'Self-evolving organizational knowledge graph',
      icon: Database,
      status: 'infrastructure',
      href: '#',
    },
  ]

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-500'
      case 'development': return 'bg-blue-500'
      case 'infrastructure': return 'bg-purple-500'
      case 'planned': return 'bg-gray-400'
      default: return 'bg-gray-400'
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-950 dark:to-slate-900">
      {/* Header */}
      <header className="border-b bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Capital OS
              </h1>
              <p className="text-sm text-muted-foreground mt-1">
                Intelligence & Orchestration Platform
              </p>
            </div>
            <Badge variant="outline" className="text-sm">
              Strawman Prototype v0.1
            </Badge>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-12">
        {/* Hero Section */}
        <div className="mb-12 text-center">
          <h2 className="text-4xl font-bold mb-4">
            Modular AI-Native Platform
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Build self-evolving organizational intelligence through micro-UIs,
            agent orchestration, and knowledge graph infrastructure
          </p>
        </div>

        {/* Modules Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {modules.map((module) => {
            const Icon = module.icon
            return (
              <Card
                key={module.id}
                className="hover:shadow-lg transition-shadow relative overflow-hidden group"
              >
                <div className={`absolute top-0 right-0 w-24 h-24 ${getStatusColor(module.status)} opacity-10 rounded-bl-full`} />

                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="p-2 bg-primary/10 rounded-lg">
                      <Icon className="h-6 w-6 text-primary" />
                    </div>
                    <Badge variant="secondary" className="text-xs">
                      {module.status}
                    </Badge>
                  </div>
                  <CardTitle className="mt-4">{module.name}</CardTitle>
                  <CardDescription>{module.description}</CardDescription>
                </CardHeader>

                <CardContent>
                  {module.status === 'active' ? (
                    <Link href={module.href}>
                      <Button className="w-full group">
                        Open Module
                        <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                      </Button>
                    </Link>
                  ) : (
                    <Button className="w-full" variant="outline" disabled>
                      Coming Soon
                    </Button>
                  )}
                </CardContent>
              </Card>
            )
          })}
        </div>

        {/* System Status */}
        <Card>
          <CardHeader>
            <CardTitle>System Status</CardTitle>
            <CardDescription>Backend services and infrastructure</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="flex items-center gap-3 p-3 border rounded-lg">
                <div className="h-2 w-2 bg-green-500 rounded-full animate-pulse" />
                <div>
                  <p className="text-sm font-medium">MCP Server</p>
                  <p className="text-xs text-muted-foreground">Connected</p>
                </div>
              </div>
              <div className="flex items-center gap-3 p-3 border rounded-lg">
                <div className="h-2 w-2 bg-yellow-500 rounded-full" />
                <div>
                  <p className="text-sm font-medium">Supabase</p>
                  <p className="text-xs text-muted-foreground">Pending Setup</p>
                </div>
              </div>
              <div className="flex items-center gap-3 p-3 border rounded-lg">
                <div className="h-2 w-2 bg-yellow-500 rounded-full" />
                <div>
                  <p className="text-sm font-medium">Neo4j</p>
                  <p className="text-xs text-muted-foreground">Pending Setup</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </main>

      {/* Footer */}
      <footer className="border-t mt-12 py-6">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          <p>Capital OS - Built on Vercel, Powered by AI</p>
        </div>
      </footer>
    </div>
  )
}
