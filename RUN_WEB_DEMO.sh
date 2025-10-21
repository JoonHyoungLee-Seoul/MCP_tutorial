#!/bin/bash

echo "🚀 Starting MCP Multi-Agent Web Demo..."
echo "============================================================"
echo ""
echo "📌 The web interface will open automatically in your browser"
echo "📌 URL: http://localhost:8501"
echo "📌 Press Ctrl+C to stop the server"
echo ""
echo "============================================================"
echo ""

# Activate virtual environment and run streamlit
cd "$(dirname "$0")"
source ../.venv/bin/activate
streamlit run web_demo.py
