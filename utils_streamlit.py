"""
Streamlit-specific utility functions for MCP agent
"""

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage


def astream_graph_streamlit(graph, inputs, config):
    """
    Stream graph execution with Streamlit UI rendering

    Args:
        graph: LangGraph graph to execute
        inputs: Input dictionary
        config: Graph configuration
    """

    # Create containers for different sections
    step_count = 0
    current_node = None
    agent_messages = []
    tool_calls = []

    for chunk in graph.stream(inputs, config, stream_mode="updates"):
        step_count += 1

        for node_name, chunk_data in chunk.items():
            current_node = node_name

            if node_name == "agent":
                # Agent node
                if "messages" in chunk_data:
                    for msg in chunk_data["messages"]:
                        if isinstance(msg, AIMessage):
                            # Agent response
                            if msg.content:
                                agent_messages.append(msg.content)

                            # Tool calls
                            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                                for tool_call in msg.tool_calls:
                                    tool_name = tool_call.get('name', 'Unknown')
                                    tool_args = tool_call.get('args', {})
                                    tool_calls.append({
                                        'name': tool_name,
                                        'args': tool_args,
                                        'result': None
                                    })

            elif node_name == "tools":
                # Tool execution results
                if "messages" in chunk_data:
                    for msg in chunk_data["messages"]:
                        if isinstance(msg, ToolMessage):
                            tool_name = msg.name if hasattr(msg, 'name') else 'Unknown'
                            tool_result = msg.content

                            # Update tool_calls with result
                            for tc in reversed(tool_calls):
                                if tc['name'] == tool_name and tc['result'] is None:
                                    tc['result'] = tool_result
                                    break

    return agent_messages, tool_calls


async def display_agent_response_streamlit(agent, config, query):
    """
    Display agent response in Streamlit with beautiful formatting

    Args:
        agent: LangGraph agent
        config: Agent configuration
        query: User query
    """

    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()

    step_count = 0
    total_steps = 10  # Estimate

    # Containers for output
    agent_thinking = st.container()
    tool_usage = st.container()
    final_response = st.container()

    agent_messages = []
    tool_executions = []

    try:
        status_text.text("🔄 Agent is thinking...")

        # Use async stream instead of sync stream
        async for chunk in agent.astream({"messages": query}, config, stream_mode="updates"):
            step_count += 1
            progress = min(step_count / total_steps, 0.9)
            progress_bar.progress(progress)

            for node_name, chunk_data in chunk.items():

                if node_name == "agent":
                    status_text.text(f"🤖 Agent: Processing...")

                    if "messages" in chunk_data:
                        for msg in chunk_data["messages"]:
                            if isinstance(msg, AIMessage):
                                # Agent thinking/response
                                if msg.content:
                                    agent_messages.append(msg.content)

                                # Tool calls
                                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                                    for tool_call in msg.tool_calls:
                                        tool_name = tool_call.get('name', 'Unknown')
                                        tool_args = tool_call.get('args', {})

                                        tool_executions.append({
                                            'name': tool_name,
                                            'args': tool_args,
                                            'result': None,
                                            'status': 'pending'
                                        })

                                        status_text.text(f"🔧 Calling tool: {tool_name}")

                elif node_name == "tools":
                    status_text.text(f"⚙️ Tools: Executing...")

                    if "messages" in chunk_data:
                        for msg in chunk_data["messages"]:
                            if isinstance(msg, ToolMessage):
                                tool_name = msg.name if hasattr(msg, 'name') else 'Unknown'
                                tool_result = msg.content

                                # Update tool execution result
                                for te in reversed(tool_executions):
                                    if te['name'] == tool_name and te['result'] is None:
                                        te['result'] = tool_result
                                        te['status'] = 'completed'
                                        break

                                status_text.text(f"✅ Tool completed: {tool_name}")

        progress_bar.progress(1.0)
        status_text.text("✅ Complete!")

        # Display results
        with final_response:
            st.markdown("### 💬 Agent Response")
            for msg in agent_messages:
                st.markdown(msg)

        # Display tool usage
        if tool_executions:
            with tool_usage:
                st.markdown("### 🔧 Tools Used")
                for i, te in enumerate(tool_executions, 1):
                    with st.expander(f"{i}. {get_tool_icon(te['name'])} {te['name']}", expanded=False):
                        if te['args']:
                            st.markdown("**Arguments:**")
                            st.json(te['args'])

                        if te['result']:
                            st.markdown("**Result:**")
                            # Truncate long results
                            result_text = str(te['result'])
                            if len(result_text) > 1000:
                                st.text_area("", result_text[:1000] + "\n\n... (truncated)", height=200, key=f"tool_result_{i}")
                            else:
                                st.code(result_text, language="")

        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()

        return True

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
        return False


def get_tool_icon(tool_name):
    """Get emoji icon for tool"""
    icons = {
        'retrieve': '📚',
        'calculate': '🧮',
        'percentage_change': '📊',
        'statistics_summary': '📈',
        'currency_convert': '💱',
        'compare_values': '⚖️',
        'execute_python': '🐍',
        'create_visualization': '📊',
        'analyze_data': '🔬',
        'read_csv': '📄',
        'save_to_csv': '💾',
        'tavily_search_results_json': '🔍'
    }
    return icons.get(tool_name, '🔧')


def format_tool_result(result, max_length=500):
    """Format tool result for display"""
    result_str = str(result)

    if len(result_str) <= max_length:
        return result_str

    return result_str[:max_length] + f"\n\n... (showing {max_length} of {len(result_str)} characters)"
