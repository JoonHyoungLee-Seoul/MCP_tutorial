#!/usr/bin/env python
"""
Test calculator tools directly
"""

import asyncio
from agent import create_mcp_agent

async def test_calculator():
    """Test calculator tools"""
    print("="*60)
    print("Testing Calculator Tools")
    print("="*60)

    # Create agent
    agent, config, tools = create_mcp_agent()

    # Find calculator tools
    calc_tools = [t for t in tools if 'calculate' in t.name or 'currency' in t.name]

    print(f"\nFound {len(calc_tools)} calculator tools:")
    for tool in calc_tools:
        print(f"  - {tool.name}")

    # Test query
    test_query = "Calculate 1299 multiplied by 8.27"

    print(f"\n{'='*60}")
    print(f"Test Query: {test_query}")
    print(f"{'='*60}\n")

    try:
        # Use async stream
        async for chunk in agent.astream({"messages": test_query}, config, stream_mode="updates"):
            for node_name, chunk_data in chunk.items():
                if node_name == "agent":
                    if "messages" in chunk_data:
                        for msg in chunk_data["messages"]:
                            if hasattr(msg, 'content') and msg.content:
                                print(f"Agent: {msg.content}")

                elif node_name == "tools":
                    if "messages" in chunk_data:
                        for msg in chunk_data["messages"]:
                            if hasattr(msg, 'content'):
                                print(f"Tool Result: {msg.content}")

        print(f"\n{'='*60}")
        print("✅ Test completed successfully!")
        print(f"{'='*60}")
        return True

    except Exception as e:
        print(f"\n{'='*60}")
        print(f"❌ Test failed: {str(e)}")
        print(f"{'='*60}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_calculator())
    import sys
    sys.exit(0 if success else 1)
