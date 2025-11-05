#!/usr/bin/env python3
"""Quick verification for AviationStackClient using environment variables.

This script initializes AviationStackClient and performs a lightweight airport
info query to confirm the API key is loaded correctly.
"""

import sys
import os

ROOT = os.path.dirname(os.path.dirname(__file__))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

try:
    from travel_mcp.aviation_client import AviationStackClient
except Exception as e:
    print(f"[AviationStack] Import failed: {e}")
    sys.exit(1)

def main() -> None:
    try:
        client = AviationStackClient()
        print("[AviationStack] Client initialized.")
        # Try tracking a flight (endpoint usually available on free tier)
        result = client.track_flight(flight_iata="AA100")
        if result.get("success"):
            data = result.get("data", [])
            print(f"[AviationStack] Track OK. Records: {len(data)}")
            if data:
                sample = data[0]
                print(f"[AviationStack] Sample: {sample.get('flight', sample)}")
        else:
            print(f"[AviationStack] API error: {result}")
            sys.exit(2)
    except Exception as e:
        print(f"[AviationStack] Initialization/API call failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()