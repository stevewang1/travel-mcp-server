"""AviationStack API client for real-time flight tracking."""

import os
from pathlib import Path
from typing import Any, Dict, Optional
import requests
from dotenv import load_dotenv

# Always load .env from project root regardless of current working directory
_ROOT_DIR = Path(__file__).resolve().parents[2]
_DOTENV_PATH = _ROOT_DIR / ".env"
load_dotenv(dotenv_path=_DOTENV_PATH, override=False)


class AviationStackClient:
    """Client for interacting with AviationStack API for flight tracking."""

    BASE_URL = "https://api.aviationstack.com/v1"

    def __init__(self) -> None:
        """Initialize the AviationStack client with API key from environment."""
        self.api_key = os.getenv("AVIATIONSTACK_API_KEY")

        if not self.api_key:
            raise ValueError("AVIATIONSTACK_API_KEY must be set in environment")

    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a request to the AviationStack API.

        Args:
            endpoint: API endpoint path
            params: Query parameters

        Returns:
            API response as dictionary
        """
        params["access_key"] = self.api_key
        url = f"{self.BASE_URL}/{endpoint}"

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "success": False}

    def track_flight(
        self,
        flight_iata: Optional[str] = None,
        flight_icao: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Track a specific flight in real-time.

        Args:
            flight_iata: IATA flight code (e.g., 'AA100')
            flight_icao: ICAO flight code (e.g., 'AAL100')

        Returns:
            Dictionary containing flight tracking information
        """
        if not flight_iata and not flight_icao:
            return {
                "success": False,
                "error": "Either flight_iata or flight_icao must be provided",
            }

        params: Dict[str, Any] = {}
        if flight_iata:
            params["flight_iata"] = flight_iata
        if flight_icao:
            params["flight_icao"] = flight_icao

        result = self._make_request("flights", params)

        if "error" in result:
            return result

        return {
            "success": True,
            "data": result.get("data", []),
            "pagination": result.get("pagination", {}),
        }

    def get_flights_by_route(
        self,
        dep_iata: Optional[str] = None,
        arr_iata: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get flights by departure and arrival airports.

        Args:
            dep_iata: Departure airport IATA code
            arr_iata: Arrival airport IATA code

        Returns:
            Dictionary containing flight information
        """
        params: Dict[str, Any] = {}
        if dep_iata:
            params["dep_iata"] = dep_iata
        if arr_iata:
            params["arr_iata"] = arr_iata

        result = self._make_request("flights", params)

        if "error" in result:
            return result

        return {
            "success": True,
            "data": result.get("data", []),
            "pagination": result.get("pagination", {}),
        }

    def get_airport_info(self, iata_code: str) -> Dict[str, Any]:
        """
        Get information about an airport.

        Args:
            iata_code: Airport IATA code

        Returns:
            Dictionary containing airport information
        """
        params = {"search": iata_code}
        result = self._make_request("airports", params)

        if "error" in result:
            return result

        return {
            "success": True,
            "data": result.get("data", []),
        }
