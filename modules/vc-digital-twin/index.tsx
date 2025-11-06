"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import {
  TrendingUp,
  Search,
  FileText,
  BarChart3,
  AlertCircle,
  CheckCircle,
  Clock,
  Activity,
  Loader2,
  ExternalLink,
  DollarSign,
  Users,
  Target
} from "lucide-react"

interface Company {
  name: string
  sector: string
  stage: string
  status: "analyzing" | "complete" | "error" | "pending"
  analysis?: {
    status: string
    market_analysis?: {
      tam: string
      growth_rate: string
      competitive_landscape: any
      opportunities: string[]
      risks: string[]
    }
    agent_notes?: string[]
    recommendation?: string
  }
  error?: string
}

export function VCDigitalTwin() {
  const [activeTab, setActiveTab] = useState("pipeline")
  const [companies, setCompanies] = useState<Company[]>([])
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedSector, setSelectedSector] = useState("Technology")
  const [selectedStage, setSelectedStage] = useState("seed")
  const [analyzing, setAnalyzing] = useState(false)

  const analyzeCompany = async (companyName: string) => {
    setAnalyzing(true)

    // Add to pipeline
    const newCompany: Company = {
      name: companyName,
      sector: selectedSector,
      stage: selectedStage,
      status: "analyzing"
    }
    setCompanies(prev => [newCompany, ...prev])

    try {
      // Call MCP server
      const mcpServerUrl = process.env.NEXT_PUBLIC_MCP_SERVER_URL || 'http://localhost:8000'
      const response = await fetch(`${mcpServerUrl}/tools/analyze_market`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          company_name: companyName,
          sector: selectedSector,
          stage: selectedStage,
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const result = await response.json()

      // Update company with results
      setCompanies(prev => prev.map(c =>
        c.name === companyName && c.status === "analyzing"
          ? { ...c, status: "complete", analysis: result }
          : c
      ))
    } catch (error) {
      console.error("Analysis failed:", error)
      setCompanies(prev => prev.map(c =>
        c.name === companyName && c.status === "analyzing"
          ? { ...c, status: "error", error: error instanceof Error ? error.message : "Unknown error" }
          : c
      ))
    } finally {
      setAnalyzing(false)
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "analyzing": return <Loader2 className="h-4 w-4 animate-spin text-blue-500" />
      case "complete": return <CheckCircle className="h-4 w-4 text-green-500" />
      case "error": return <AlertCircle className="h-4 w-4 text-red-500" />
      default: return <Clock className="h-4 w-4 text-gray-400" />
    }
  }

  const handleSubmit = () => {
    if (searchQuery.trim()) {
      analyzeCompany(searchQuery.trim())
      setSearchQuery("")
    }
  }

  return (
    <div className="space-y-6">
      {/* Module Header */}
      <Card className="border-2">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-3xl">VC Digital Twin</CardTitle>
              <CardDescription className="mt-2 text-base">
                AI-powered investment analysis using LangGraph multi-agent system
              </CardDescription>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="outline" className="text-sm px-3 py-1">
                <Activity className="mr-2 h-4 w-4" />
                {companies.filter(c => c.status === "analyzing").length} Active
              </Badge>
              <Badge variant="secondary" className="text-sm px-3 py-1">
                {companies.filter(c => c.status === "complete").length} Analyzed
              </Badge>
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Main Interface */}
      <Card>
        <CardContent className="pt-6">
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="pipeline">
                <TrendingUp className="mr-2 h-4 w-4" />
                Pipeline
              </TabsTrigger>
              <TabsTrigger value="research">
                <Search className="mr-2 h-4 w-4" />
                Research
              </TabsTrigger>
              <TabsTrigger value="diligence">
                <FileText className="mr-2 h-4 w-4" />
                Due Diligence
              </TabsTrigger>
              <TabsTrigger value="portfolio">
                <BarChart3 className="mr-2 h-4 w-4" />
                Portfolio
              </TabsTrigger>
            </TabsList>

            {/* Pipeline Tab */}
            <TabsContent value="pipeline" className="space-y-4 mt-6">
              {/* Search Interface */}
              <Card>
                <CardContent className="pt-6">
                  <div className="space-y-4">
                    <div className="flex gap-2">
                      <Input
                        placeholder="Enter company name (e.g., Stripe, OpenAI, Anthropic)..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        onKeyPress={(e) => {
                          if (e.key === 'Enter') handleSubmit()
                        }}
                        className="text-base"
                      />
                      <Button
                        onClick={handleSubmit}
                        disabled={analyzing || !searchQuery.trim()}
                        size="lg"
                      >
                        {analyzing ? (
                          <>
                            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                            Analyzing...
                          </>
                        ) : (
                          <>
                            <Search className="mr-2 h-4 w-4" />
                            Analyze
                          </>
                        )}
                      </Button>
                    </div>

                    <div className="flex gap-2">
                      <select
                        value={selectedSector}
                        onChange={(e) => setSelectedSector(e.target.value)}
                        className="px-3 py-2 border rounded-md text-sm"
                      >
                        <option>Technology</option>
                        <option>SaaS</option>
                        <option>Fintech</option>
                        <option>Healthcare</option>
                        <option>AI/ML</option>
                      </select>
                      <select
                        value={selectedStage}
                        onChange={(e) => setSelectedStage(e.target.value)}
                        className="px-3 py-2 border rounded-md text-sm"
                      >
                        <option value="pre-seed">Pre-Seed</option>
                        <option value="seed">Seed</option>
                        <option value="series-a">Series A</option>
                        <option value="series-b">Series B</option>
                      </select>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Company Pipeline */}
              <div className="space-y-3">
                {companies.length === 0 ? (
                  <Card className="border-dashed">
                    <CardContent className="text-center py-12">
                      <TrendingUp className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
                      <p className="text-lg font-medium text-muted-foreground mb-2">
                        No companies in pipeline
                      </p>
                      <p className="text-sm text-muted-foreground">
                        Enter a company name above to start your first analysis
                      </p>
                    </CardContent>
                  </Card>
                ) : (
                  companies.map((company, idx) => (
                    <Card key={idx} className="hover:shadow-md transition-shadow">
                      <CardContent className="p-6">
                        <div className="flex items-start justify-between">
                          <div className="flex items-start gap-4 flex-1">
                            {getStatusIcon(company.status)}

                            <div className="flex-1">
                              <div className="flex items-center gap-2 mb-1">
                                <h3 className="font-semibold text-lg">{company.name}</h3>
                                <Badge variant="outline">{company.sector}</Badge>
                                <Badge variant="secondary">{company.stage}</Badge>
                              </div>

                              {company.status === "analyzing" && (
                                <div className="mt-3">
                                  <p className="text-sm text-muted-foreground mb-2">
                                    Running analysis through agent network...
                                  </p>
                                  <Progress value={33} className="h-2" />
                                </div>
                              )}

                              {company.status === "complete" && company.analysis && (
                                <div className="mt-4 space-y-3">
                                  {company.analysis.market_analysis && (
                                    <>
                                      <div className="grid grid-cols-3 gap-3">
                                        <div className="p-3 bg-blue-50 dark:bg-blue-950 rounded-lg">
                                          <p className="text-xs text-muted-foreground">TAM</p>
                                          <p className="font-semibold">
                                            {company.analysis.market_analysis.tam}
                                          </p>
                                        </div>
                                        <div className="p-3 bg-green-50 dark:bg-green-950 rounded-lg">
                                          <p className="text-xs text-muted-foreground">Growth Rate</p>
                                          <p className="font-semibold">
                                            {company.analysis.market_analysis.growth_rate}
                                          </p>
                                        </div>
                                        <div className="p-3 bg-purple-50 dark:bg-purple-950 rounded-lg">
                                          <p className="text-xs text-muted-foreground">Status</p>
                                          <p className="font-semibold capitalize">
                                            {company.analysis.status}
                                          </p>
                                        </div>
                                      </div>

                                      {company.analysis.market_analysis.opportunities && company.analysis.market_analysis.opportunities.length > 0 && (
                                        <div className="p-3 border rounded-lg">
                                          <p className="text-sm font-medium mb-2">Key Opportunities</p>
                                          <ul className="text-sm space-y-1">
                                            {company.analysis.market_analysis.opportunities.slice(0, 3).map((opp, i) => (
                                              <li key={i} className="text-muted-foreground">• {opp}</li>
                                            ))}
                                          </ul>
                                        </div>
                                      )}
                                    </>
                                  )}

                                  <div className="flex gap-2">
                                    <Button variant="outline" size="sm">
                                      <FileText className="mr-2 h-4 w-4" />
                                      Full Report
                                    </Button>
                                    <Button variant="outline" size="sm">
                                      <Target className="mr-2 h-4 w-4" />
                                      Due Diligence
                                    </Button>
                                  </div>
                                </div>
                              )}

                              {company.status === "error" && (
                                <div className="mt-3 p-3 bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-800 rounded-lg">
                                  <p className="text-sm text-red-600 dark:text-red-400">
                                    {company.error || "Analysis failed. Please try again."}
                                  </p>
                                </div>
                              )}
                            </div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))
                )}
              </div>
            </TabsContent>

            {/* Research Tab */}
            <TabsContent value="research" className="space-y-4 mt-6">
              <Card>
                <CardHeader>
                  <CardTitle>Market Research Tools</CardTitle>
                  <CardDescription>
                    Deep dive into market dynamics and competitive landscape
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 gap-4">
                    <Button variant="outline" className="h-32 flex-col">
                      <Search className="h-8 w-8 mb-2" />
                      <span className="font-medium">Industry Analysis</span>
                      <span className="text-xs text-muted-foreground mt-1">
                        Coming in Phase 2
                      </span>
                    </Button>
                    <Button variant="outline" className="h-32 flex-col">
                      <Target className="h-8 w-8 mb-2" />
                      <span className="font-medium">Competitor Research</span>
                      <span className="text-xs text-muted-foreground mt-1">
                        Coming in Phase 2
                      </span>
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Due Diligence Tab */}
            <TabsContent value="diligence" className="space-y-4 mt-6">
              <Card>
                <CardHeader>
                  <CardTitle>Due Diligence Workflows</CardTitle>
                  <CardDescription>
                    Comprehensive analysis across multiple domains
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {[
                      { name: "Financial Analysis", desc: "Revenue, burn rate, unit economics" },
                      { name: "Technical Assessment", desc: "Architecture, scalability, tech debt" },
                      { name: "Team Evaluation", desc: "Founders, key hires, culture" },
                      { name: "Legal Review", desc: "Cap table, contracts, IP" }
                    ].map((item, idx) => (
                      <div key={idx} className="flex items-center justify-between p-4 border rounded-lg hover:bg-accent transition-colors">
                        <div>
                          <p className="font-medium">{item.name}</p>
                          <p className="text-sm text-muted-foreground">{item.desc}</p>
                        </div>
                        <Button size="sm" variant="outline" disabled>
                          Coming in Phase 2
                        </Button>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Portfolio Tab */}
            <TabsContent value="portfolio" className="space-y-4 mt-6">
              <div className="grid grid-cols-4 gap-4 mb-6">
                {[
                  { label: "Total AUM", value: "$50M", icon: DollarSign, color: "blue" },
                  { label: "Portfolio Cos", value: "12", icon: Users, color: "green" },
                  { label: "Avg Multiple", value: "3.2x", icon: TrendingUp, color: "purple" },
                  { label: "Exits", value: "2", icon: CheckCircle, color: "orange" }
                ].map((metric, idx) => {
                  const Icon = metric.icon
                  return (
                    <Card key={idx}>
                      <CardContent className="pt-6">
                        <div className="flex items-center justify-between mb-2">
                          <Icon className={`h-5 w-5 text-${metric.color}-500`} />
                        </div>
                        <div className="text-3xl font-bold">{metric.value}</div>
                        <p className="text-xs text-muted-foreground mt-1">{metric.label}</p>
                      </CardContent>
                    </Card>
                  )
                })}
              </div>

              <Card>
                <CardHeader>
                  <CardTitle>Portfolio Companies</CardTitle>
                  <CardDescription>Monitor and support existing investments</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="text-center py-12 text-muted-foreground">
                    <Users className="h-12 w-12 mx-auto mb-4" />
                    <p className="font-medium mb-2">Portfolio monitoring coming in Phase 3</p>
                    <p className="text-sm">
                      Track KPIs, milestones, and provide AI-powered insights
                    </p>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>

      {/* Agent Status Footer */}
      <Card>
        <CardContent className="flex items-center justify-between py-4">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="h-2 w-2 bg-green-500 rounded-full animate-pulse" />
              <span className="text-sm font-medium">Supervisor</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="h-2 w-2 bg-green-500 rounded-full animate-pulse" />
              <span className="text-sm font-medium">Market Analysis</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="h-2 w-2 bg-gray-300 rounded-full" />
              <span className="text-sm font-medium text-muted-foreground">Financial Analysis (Phase 2)</span>
            </div>
          </div>
          <Badge variant="outline">
            <Activity className="mr-1 h-3 w-3" />
            All systems operational
          </Badge>
        </CardContent>
      </Card>
    </div>
  )
}
