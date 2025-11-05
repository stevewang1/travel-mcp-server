#!/usr/bin/env python3
"""Quick verification for AmadeusClient using environment variables.

This script initializes AmadeusClient and performs a lightweight airport/city
search to confirm credentials are loaded correctly.
"""

import sys
import os

# Ensure src is in path
ROOT = os.path.dirname(os.path.dirname(__file__))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

try:
    from travel_mcp.amadeus_client import AmadeusClient
except Exception as e:
    print(f"[Amadeus] Import failed: {e}")
    sys.exit(1)

def main() -> None:
    try:
        client = AmadeusClient()
        print("[Amadeus] Client initialized.")
        # Lightweight query that should work in test environment
        result = client.search_airport_by_city("Paris")
        if result.get("success"):
            data = result.get("data", [])
            print(f"[Amadeus] Search OK. Records: {len(data)}")
            # Print a small sample
            if data:
                sample = data[0]
                print(f"[Amadeus] Sample: {sample.get('name', sample)}")
        else:
            print(f"[Amadeus] API error: {result}")
            sys.exit(2)
    except Exception as e:
        print(f"[Amadeus] Initialization/API call failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()