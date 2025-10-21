#!/usr/bin/env python
"""
Quick test script to verify agent initialization works
"""

import sys
import os

# Add project to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from agent import create_mcp_agent

def test_agent_creation():
    """Test that agent can be created without errors"""
    print("="*60)
    print("Testing Agent Initialization")
    print("="*60)

    try:
        agent, config, tools = create_mcp_agent()

        print("\n" + "="*60)
        print("✅ SUCCESS! Agent initialized successfully")
        print("="*60)
        print(f"\nAgent: {type(agent).__name__}")
        print(f"Config: {config}")
        print(f"Tools: {len(tools)} tools loaded")
        print("\nTool names:")
        for i, tool in enumerate(tools, 1):
            print(f"  {i}. {tool.name}")

        return True

    except Exception as e:
        print("\n" + "="*60)
        print(f"❌ FAILED: {str(e)}")
        print("="*60)
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_agent_creation()
    sys.exit(0 if success else 1)
