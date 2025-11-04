#!/usr/bin/env python3
"""Basic test script to verify the MCP server structure."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")

    try:
        from travel_mcp import __version__
        print(f"✓ travel_mcp package imported (version {__version__})")
    except ImportError as e:
        print(f"✗ Failed to import travel_mcp: {e}")
        return False

    try:
        from travel_mcp.server import app, list_tools, call_tool
        print("✓ Server module imported")
    except ImportError as e:
        print(f"✗ Failed to import server: {e}")
        return False

    # Test clients (they might fail without env vars, which is OK)
    try:
        from travel_mcp.amadeus_client import AmadeusClient
        print("✓ AmadeusClient imported")
    except ImportError as e:
        print(f"✗ Failed to import AmadeusClient: {e}")
        return False

    try:
        from travel_mcp.aviation_client import AviationStackClient
        print("✓ AviationStackClient imported")
    except ImportError as e:
        print(f"✗ Failed to import AviationStackClient: {e}")
        return False

    return True

def test_mcp_structure():
    """Test that MCP server structure is correct."""
    print("\nTesting MCP server structure...")

    try:
        from travel_mcp.server import app
        print(f"✓ MCP server app created: {app.name}")
        return True
    except Exception as e:
        print(f"✗ Failed to create MCP server: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Travel MCP Server - Basic Tests")
    print("=" * 60)

    all_passed = True

    if not test_imports():
        all_passed = False

    if not test_mcp_structure():
        all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All basic tests passed!")
        print("\nNote: Client initialization will fail without API keys in .env")
        print("This is expected and doesn't affect the MCP server structure.")
    else:
        print("✗ Some tests failed!")
        sys.exit(1)
    print("=" * 60)

if __name__ == "__main__":
    main()
