#!/usr/bin/env python
"""
Test create_visualization tool to debug empty chart issue
"""

import asyncio
from agent import create_mcp_agent

async def test_visualization():
    """Test create_visualization with debug output"""
    print("="*60)
    print("Testing create_visualization Tool")
    print("="*60)

    # Create agent
    agent, config, tools = create_mcp_agent()

    # Test query with explicit data
    test_query = """
    Create a bar chart with the following data:
    - iPhone 17 Pro: 2.8 million units
    - iPhone 17: 3.5 million units
    - iPhone 16 Pro: 2.5 million units
    - iPhone 16: 3.2 million units

    Title: "iPhone Sales Comparison Q3 2025"
    X-axis label: "Model"
    Y-axis label: "Sales (Millions)"
    Save as: "test_sales.png"
    """

    print(f"\n{'='*60}")
    print(f"Test Query:\n{test_query}")
    print(f"{'='*60}\n")

    try:
        step_count = 0
        # Use async stream
        async for chunk in agent.astream({"messages": test_query}, config, stream_mode="updates"):
            step_count += 1
            print(f"\n--- Step {step_count} ---")

            for node_name, chunk_data in chunk.items():
                print(f"Node: {node_name}")

                if node_name == "agent":
                    if "messages" in chunk_data:
                        for msg in chunk_data["messages"]:
                            if hasattr(msg, 'content') and msg.content:
                                print(f"Agent says: {msg.content[:200]}...")

                            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                                for tc in msg.tool_calls:
                                    print(f"\n🔧 Tool Call: {tc.get('name')}")
                                    print(f"   Args: {tc.get('args')}")

                elif node_name == "tools":
                    if "messages" in chunk_data:
                        for msg in chunk_data["messages"]:
                            if hasattr(msg, 'content'):
                                print(f"\n✅ Tool Result:")
                                print(f"{msg.content[:500]}...")

        print(f"\n{'='*60}")
        print("✅ Test completed!")
        print(f"{'='*60}")

        # Check if file was created
        import os
        output_file = "output/test_sales.png"
        if os.path.exists(output_file):
            size = os.path.getsize(output_file)
            print(f"\n📊 File created: {output_file} ({size:,} bytes)")

            # Check if it's actually a valid PNG
            if size < 1000:
                print("⚠️  WARNING: File is very small, might be empty or corrupted")
            else:
                print("✅ File size looks good")
        else:
            print(f"\n❌ File not found: {output_file}")

        return True

    except Exception as e:
        print(f"\n{'='*60}")
        print(f"❌ Test failed: {str(e)}")
        print(f"{'='*60}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_visualization())
    import sys
    sys.exit(0 if success else 1)
