/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    MCP_SERVER_URL: process.env.MCP_SERVER_URL || 'http://localhost:8000',
  },
}

module.exports = nextConfig
