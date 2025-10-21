"""
MCP Multi-Agent System - Streamlit Web Demo
============================================

A web-based demo interface for the MCP multi-agent system.

Usage:
    streamlit run web_demo.py
"""

import streamlit as st
import sys
import os
from pathlib import Path
import asyncio
import time
from io import StringIO
from contextlib import redirect_stdout
from PIL import Image

# Add project to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from agent import create_mcp_agent, chat_with_agent
from utils_streamlit import display_agent_response_streamlit


# Page configuration
st.set_page_config(
    page_title="MCP Multi-Agent System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .tool-category {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .example-query {
        background-color: #e8f4f8;
        padding: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
        cursor: pointer;
    }
    .stTextArea textarea {
        font-size: 1.1rem;
    }
    /* Improve expander styling */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 0.5rem;
        font-weight: 500;
    }
    /* Better code block styling */
    .stCodeBlock {
        background-color: #f6f8fa;
        border-left: 3px solid #1f77b4;
    }
    /* Progress bar styling */
    .stProgress > div > div > div {
        background-color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_agent():
    """Initialize agent (cached to avoid re-initialization)"""
    with st.spinner("🚀 Initializing MCP Multi-Agent System..."):
        agent, config, tools = create_mcp_agent()
    return agent, config, tools


def display_tool_categories(tools):
    """Display available tools by category"""
    categories = {
        "📚 Document Retrieval": [],
        "🧮 Calculator": [],
        "💻 Code Executor": [],
        "🔍 Web Search": []
    }

    for tool in tools:
        if tool.name == "retrieve":
            categories["📚 Document Retrieval"].append(tool.name)
        elif tool.name in ["calculate", "percentage_change", "statistics_summary", "currency_convert", "compare_values"]:
            categories["🧮 Calculator"].append(tool.name)
        elif tool.name in ["execute_python", "create_visualization", "analyze_data", "read_csv", "save_to_csv"]:
            categories["💻 Code Executor"].append(tool.name)
        elif tool.name == "tavily_search_results_json":
            categories["🔍 Web Search"].append(tool.name)

    for category, tool_list in categories.items():
        if tool_list:
            with st.expander(f"{category} ({len(tool_list)} tools)", expanded=False):
                for tool in tool_list:
                    st.code(f"• {tool}", language="")


def display_example_queries():
    """Display example queries"""
    examples = {
        "📊 Visualization": "Create a bar chart showing iPhone sales: iPhone 17 Pro (2.8M), iPhone 17 (3.5M), iPhone 16 Pro (2.5M), iPhone 16 (3.2M). Title: 'Q3 2025 Sales'",
        "📚 Document + Calculator": "Retrieve iPhone 17 Pro price in euros and convert to USD using exchange rate 1.08",
        "🔍 Web + Analysis": "Search for iPhone 17 sales data and create a statistical summary",
        "💻 Python Code": "Execute Python code to analyze this data: sales = [1000, 1200, 1500, 1800]. Calculate mean, std dev, and growth rate.",
        "🔄 Multi-Step": "1. Retrieve iPhone 17 battery capacity\n2. Compare with iPhone 16\n3. Calculate percentage difference\n4. Create a bar chart"
    }

    st.sidebar.markdown("### 💡 Example Queries")
    for title, query in examples.items():
        if st.sidebar.button(title, key=f"example_{title}", use_container_width=True):
            st.session_state.example_query = query


async def run_agent_query(agent, config, query):
    """Run agent query and capture output"""
    # Capture stdout
    output_buffer = StringIO()

    # Create a placeholder for streaming output
    output_placeholder = st.empty()

    # Run the agent
    with redirect_stdout(output_buffer):
        await chat_with_agent(agent, config, query)

    # Get the output
    output = output_buffer.getvalue()

    return output


def main():
    """Main application"""

    # Header
    st.markdown('<div class="main-header">🤖 MCP Multi-Agent System</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Initialize agent
    try:
        agent, config, tools = initialize_agent()
        st.success(f"✅ Agent initialized with {len(tools)} tools!")
    except Exception as e:
        st.error(f"❌ Failed to initialize agent: {str(e)}")
        st.stop()

    # Sidebar
    with st.sidebar:
        st.markdown("## 🛠️ Available Tools")
        display_tool_categories(tools)

        st.markdown("---")

        display_example_queries()

        st.markdown("---")

        # Output directory info
        output_dir = os.path.join(PROJECT_ROOT, "output")
        if os.path.exists(output_dir):
            files = [f for f in os.listdir(output_dir) if f.endswith(('.png', '.csv', '.jpg'))]
            st.markdown(f"### 📁 Generated Files ({len(files)})")
            for file in sorted(files)[:10]:  # Show max 10 files
                st.text(f"• {file}")

    # Main content area
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("### 💬 Ask the Agent")

        # Check if example query was clicked
        if 'example_query' in st.session_state:
            default_value = st.session_state.example_query
            del st.session_state.example_query
        else:
            default_value = ""

        # Query input
        user_query = st.text_area(
            "Enter your query:",
            height=150,
            placeholder="Example: Create a bar chart showing iPhone sales data...",
            value=default_value,
            key="query_input"
        )

        col_submit, col_clear = st.columns([1, 4])
        with col_submit:
            submit_button = st.button("🚀 Run", type="primary", use_container_width=True)
        with col_clear:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.query_input = ""
                st.rerun()

    with col2:
        st.markdown("### 📊 Stats")
        st.metric("Total Tools", len(tools))
        st.metric("Thread ID", config.get("thread_id", 1))

        if os.path.exists(os.path.join(PROJECT_ROOT, "output")):
            file_count = len([f for f in os.listdir(os.path.join(PROJECT_ROOT, "output"))])
            st.metric("Files Generated", file_count)

    # Execute query
    if submit_button and user_query.strip():
        st.markdown("---")

        try:
            # Capture existing files BEFORE execution
            output_dir = os.path.join(PROJECT_ROOT, "output")
            existing_files = set()
            if os.path.exists(output_dir):
                existing_files = set(os.listdir(output_dir))

            # Record start time
            start_time = time.time()

            # Run async function with beautiful UI
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            success = loop.run_until_complete(display_agent_response_streamlit(agent, config, user_query))
            loop.close()

            if success:
                # Find NEW files generated during this query
                if os.path.exists(output_dir):
                    current_files = set(os.listdir(output_dir))
                    new_files = current_files - existing_files

                    # Filter for image files created after start_time
                    new_images = []
                    for f in new_files:
                        if f.endswith(('.png', '.jpg', '.jpeg')):
                            filepath = os.path.join(output_dir, f)
                            if os.path.getmtime(filepath) >= start_time:
                                new_images.append(f)

                    # Also check existing files that were modified after start_time
                    for f in existing_files:
                        if f.endswith(('.png', '.jpg', '.jpeg')):
                            filepath = os.path.join(output_dir, f)
                            if os.path.exists(filepath) and os.path.getmtime(filepath) >= start_time:
                                if f not in new_images:
                                    new_images.append(f)

                    if new_images:
                        st.markdown("---")
                        st.markdown("### 📊 Generated Visualizations")
                        st.info(f"🎨 {len(new_images)} image(s) created during this query")

                        # Sort by creation time (newest first)
                        sorted_images = sorted(
                            new_images,
                            key=lambda f: os.path.getmtime(os.path.join(output_dir, f)),
                            reverse=True
                        )

                        # Display all new images (with cache busting)
                        for img_file in sorted_images:
                            img_path = os.path.join(output_dir, img_file)

                            # Add timestamp to bust cache
                            mtime = os.path.getmtime(img_path)

                            # Read image file and display
                            # This prevents browser caching issues
                            img = Image.open(img_path)
                            st.image(img, caption=f"📊 {img_file} (created: {time.strftime('%H:%M:%S', time.localtime(mtime))})", use_container_width=True)
                    else:
                        # No new images, but show info
                        st.info("ℹ️ No new visualizations were created during this query.")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.exception(e)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>🤖 MCP Multi-Agent System | Powered by LangGraph, Claude, and MCP Servers</p>
        <p><small>Tools: Document Retrieval • Calculator • Code Executor • Web Search</small></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
