#!/bin/bash
# Capital OS Platform Setup Script

set -e

echo "🚀 Setting up Capital OS Platform..."
echo ""

# Check if we're in the correct directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this script from the capos directory"
    exit 1
fi

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Found Python $python_version"

# Check Node version
echo "📋 Checking Node.js version..."
node_version=$(node --version)
echo "   Found Node $node_version"

echo ""
echo "📦 Installing dependencies..."

# Install Python dependencies for existing VC agents
echo "   Installing Python dependencies..."
pip install -r requirements.txt --quiet

# Install MCP server dependencies
echo "   Installing MCP server dependencies..."
pip install fastmcp fastapi uvicorn websockets --quiet

# Install root npm dependencies (for concurrently)
echo "   Installing root npm dependencies..."
npm install --silent

# Install frontend dependencies
echo "   Installing frontend dependencies..."
cd frontend
npm install --silent
cd ..

echo ""
echo "🔐 Setting up environment files..."

# Copy environment examples if they don't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "   Created .env from .env.example"
    echo "   ⚠️  Please edit .env and add your API keys"
else
    echo "   .env already exists, skipping..."
fi

if [ ! -f "frontend/.env.local" ]; then
    cp frontend/.env.example frontend/.env.local
    echo "   Created frontend/.env.local"
else
    echo "   frontend/.env.local already exists, skipping..."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📚 Next steps:"
echo ""
echo "1. Add your API keys to .env:"
echo "   - OPENAI_API_KEY or ANTHROPIC_API_KEY"
echo "   - TAVILY_API_KEY (optional, for web search)"
echo ""
echo "2. Start the development servers:"
echo "   npm run dev"
echo ""
echo "3. Open your browser:"
echo "   Frontend: http://localhost:3000"
echo "   MCP Server: http://localhost:8000"
echo ""
echo "4. Test the VC Digital Twin module:"
echo "   - Navigate to http://localhost:3000/modules/vc-digital-twin"
echo "   - Enter a company name (e.g., 'Stripe', 'OpenAI')"
echo "   - Watch your existing agents analyze it!"
echo ""
echo "💡 Tips:"
echo "   - Use 'npm run dev:frontend' to run just the frontend"
echo "   - Use 'npm run dev:mcp' to run just the MCP server"
echo "   - Use 'python cli.py' to test agents via CLI (original interface)"
echo ""
echo "🎉 Happy building with Capital OS!"
