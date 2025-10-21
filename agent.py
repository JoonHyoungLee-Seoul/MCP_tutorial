"""
MCP Multi-Agent System - Standalone Python Implementation
===========================================================

This module provides a LangGraph agent with multiple MCP server integrations:
- Document Retrieval (RAG)
- Calculator
- Code Executor
- Web Search (Tavily)

Usage:
    python agent.py

    Or import in your own code:
    from agent import create_mcp_agent, chat_with_agent
"""

import sys
import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.runnables import RunnableConfig
from utils import astream_graph
import asyncio
import nest_asyncio


# Set project root
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Load environment variables
os.chdir(PROJECT_ROOT)
load_dotenv(override=True)


def create_mcp_agent(venv_path: str = None):
    """
    Create a MCP agent with all integrated tools.

    Args:
        venv_path: Path to virtual environment. Defaults to parent directory .venv

    Returns:
        tuple: (agent, config, all_tools)
    """
    # Default venv path
    if venv_path is None:
        venv_path = os.path.join(os.path.dirname(PROJECT_ROOT), '.venv', 'bin', 'python')

    print("🚀 Initializing MCP Multi-Agent System...")
    print("=" * 60)

    # Initialize model
    model = ChatAnthropic(
        model_name="claude-3-7-sonnet-latest",
        temperature=0,
        max_tokens=20000
    )

    print("✅ Model initialized: claude-3-7-sonnet-latest")

    # Configure MCP servers
    client = MultiServerMCPClient({
        "document-retriever": {
            "command": venv_path,
            "args": ["./mcp_server_rag.py"],
            "transport": "stdio",
        },
        "calculator": {
            "command": venv_path,
            "args": ["./mcp_server_calculator.py"],
            "transport": "stdio",
        },
        "code-executor": {
            "command": venv_path,
            "args": ["./mcp_server_code_executor.py"],
            "transport": "stdio",
        },
    })

    print("✅ MCP servers configured")

    # Get MCP tools (synchronous wrapper for async function)
    # Handle different event loop scenarios (CLI, Jupyter, Streamlit)
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            raise RuntimeError("Event loop is closed")
    except RuntimeError:
        # No event loop or closed loop - create new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Apply nest_asyncio to allow nested event loops (for Jupyter/Streamlit)
    nest_asyncio.apply()

    # Get tools
    mcp_tools = loop.run_until_complete(client.get_tools())

    print(f"✅ MCP tools loaded: {len(mcp_tools)} tools")

    # Add TavilySearch
    tavily = TavilySearchResults(max_results=2, topic="news", days=2)

    # Combine all tools
    all_tools = mcp_tools + [tavily]

    print(f"\n{'='*60}")
    print(f"🎉 Integration Complete! Available Tools: {len(all_tools)}")
    print(f"{'='*60}\n")

    # Print tool categories
    for i, tool in enumerate(all_tools, 1):
        category = ""
        if tool.name == "retrieve":
            category = "📚 Document"
        elif tool.name in ["calculate", "percentage_change", "statistics_summary", "currency_convert", "compare_values"]:
            category = "🧮 Calculator"
        elif tool.name in ["execute_python", "create_visualization", "analyze_data", "read_csv", "save_to_csv"]:
            category = "💻 Code Executor"
        elif tool.name == "tavily_search_results_json":
            category = "🔍 Web Search"

        print(f"{i:2d}. {category:20s} {tool.name}")

    print(f"\n{'='*60}\n")

    # Create agent
    agent = create_react_agent(
        model,
        all_tools,
        prompt="""You are a powerful AI agent with multiple capabilities:

    📚 Document Retrieval (retrieve):
       - Search information from iPhone technical documents

    🧮 Calculator (calculate, percentage_change, statistics_summary, currency_convert, compare_values):
       - Perform mathematical calculations and statistical analysis

    💻 Code Executor (execute_python, create_visualization, analyze_data, read_csv, save_to_csv):
       - Execute Python code for data analysis
       - Create visualizations (charts, graphs)
       - Process and save data files

    🔍 Web Search (tavily_search_results_json):
       - Search latest news and web information

    Choose the most appropriate tools based on the user's request.
    You can use multiple tools in sequence for complex tasks.
    Always explain which tools you're using and why.""",
        checkpointer=MemorySaver()
    )

    print("✅ Agent created successfully!\n")

    # Configuration
    config = RunnableConfig(recursion_limit=30, thread_id=1)

    return agent, config, all_tools


async def chat_with_agent(agent, config, message: str):
    """
    Send a message to the agent and get response.

    Args:
        agent: The LangGraph agent
        config: Agent configuration
        message: User message
    """
    await astream_graph(
        agent,
        {"messages": message},
        config=config
    )


def main():
    """Main CLI interface"""
    print("\n" + "="*60)
    print("🤖 MCP Multi-Agent System - Interactive CLI")
    print("="*60 + "\n")

    # Create agent
    agent, config, all_tools = create_mcp_agent()

    print("💡 Type your query (or 'quit' to exit)\n")

    # Get or create event loop
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    while True:
        try:
            user_input = input("\n👤 You: ")

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break

            if not user_input.strip():
                continue

            print("\n🤖 Agent:")
            loop.run_until_complete(chat_with_agent(agent, config, user_input))

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
