#!/bin/bash
# Quick start script for Capital OS
# Assumes setup.sh has already been run

echo "🚀 Starting Capital OS Platform..."
echo ""

# Check if setup has been run
if [ ! -f "frontend/node_modules/.package-lock.json" ]; then
    echo "⚠️  Looks like setup hasn't been run yet."
    echo "   Running setup first..."
    ./scripts/setup.sh
    echo ""
fi

# Check if API keys are configured
if ! grep -q "^OPENAI_API_KEY=sk-" .env && ! grep -q "^ANTHROPIC_API_KEY=sk-ant-" .env; then
    echo "⚠️  Warning: No AI API keys found in .env"
    echo "   The VC Digital Twin won't work without OPENAI_API_KEY or ANTHROPIC_API_KEY"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled. Please add API keys to .env first."
        exit 1
    fi
fi

echo "Starting servers..."
echo ""
echo "📡 Frontend will be available at: http://localhost:3000"
echo "🤖 MCP Server will be available at: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Start both servers using concurrently
npm run dev
