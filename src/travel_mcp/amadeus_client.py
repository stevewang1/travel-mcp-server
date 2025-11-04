"""Amadeus API client wrapper for flight and hotel search."""

import os
from typing import Any, Dict, List, Optional
from amadeus import Client, ResponseError
from dotenv import load_dotenv

load_dotenv()


class AmadeusClient:
    """Client for interacting with Amadeus Travel APIs."""

    def __init__(self) -> None:
        """Initialize the Amadeus client with credentials from environment variables."""
        self.client_id = os.getenv("AMADEUS_CLIENT_ID")
        self.client_secret = os.getenv("AMADEUS_CLIENT_SECRET")
        self.env = os.getenv("AMADEUS_ENV", "test")

        if not self.client_id or not self.client_secret:
            raise ValueError(
                "AMADEUS_CLIENT_ID and AMADEUS_CLIENT_SECRET must be set in environment"
            )

        self.client = Client(
            client_id=self.client_id,
            client_secret=self.client_secret,
            hostname="test" if self.env == "test" else "production",
        )

    def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        return_date: Optional[str] = None,
        adults: int = 1,
        max_results: int = 10,
    ) -> Dict[str, Any]:
        """
        Search for flight offers.

        Args:
            origin: Origin airport IATA code (e.g., 'JFK')
            destination: Destination airport IATA code (e.g., 'LAX')
            departure_date: Departure date in YYYY-MM-DD format
            return_date: Return date in YYYY-MM-DD format (optional for one-way)
            adults: Number of adult passengers
            max_results: Maximum number of results to return

        Returns:
            Dictionary containing flight offers

        Raises:
            ResponseError: If the API request fails
        """
        try:
            params = {
                "originLocationCode": origin.upper(),
                "destinationLocationCode": destination.upper(),
                "departureDate": departure_date,
                "adults": adults,
                "max": max_results,
            }

            if return_date:
                params["returnDate"] = return_date

            response = self.client.shopping.flight_offers_search.get(**params)

            return {
                "success": True,
                "data": response.data,
                "meta": getattr(response, "meta", {}),
            }
        except ResponseError as error:
            return {
                "success": False,
                "error": str(error),
                "details": getattr(error, "description", "Unknown error"),
            }

    def search_hotels(
        self,
        city_code: str,
        check_in_date: str,
        check_out_date: str,
        adults: int = 1,
        radius: int = 5,
        radius_unit: str = "KM",
    ) -> Dict[str, Any]:
        """
        Search for hotels by city.

        Args:
            city_code: City IATA code (e.g., 'NYC', 'PAR')
            check_in_date: Check-in date in YYYY-MM-DD format
            check_out_date: Check-out date in YYYY-MM-DD format
            adults: Number of adults
            radius: Search radius
            radius_unit: Unit for radius ('KM' or 'MILE')

        Returns:
            Dictionary containing hotel offers

        Raises:
            ResponseError: If the API request fails
        """
        try:
            response = self.client.reference_data.locations.hotels.by_city.get(
                cityCode=city_code.upper()
            )

            if not response.data:
                return {
                    "success": True,
                    "data": [],
                    "message": f"No hotels found in {city_code}",
                }

            # Get hotel IDs from the response
            hotel_ids = [hotel["hotelId"] for hotel in response.data[:20]]  # Limit to 20 hotels

            # Get hotel offers
            if hotel_ids:
                offers_response = self.client.shopping.hotel_offers_search.get(
                    hotelIds=",".join(hotel_ids),
                    checkInDate=check_in_date,
                    checkOutDate=check_out_date,
                    adults=adults,
                )

                return {
                    "success": True,
                    "data": offers_response.data,
                    "meta": getattr(offers_response, "meta", {}),
                }

            return {
                "success": True,
                "data": [],
                "message": "No hotel offers available",
            }

        except ResponseError as error:
            return {
                "success": False,
                "error": str(error),
                "details": getattr(error, "description", "Unknown error"),
            }

    def search_airport_by_city(self, city_name: str) -> Dict[str, Any]:
        """
        Search for airports by city name.

        Args:
            city_name: Name of the city

        Returns:
            Dictionary containing airport information

        Raises:
            ResponseError: If the API request fails
        """
        try:
            response = self.client.reference_data.locations.get(
                keyword=city_name,
                subType="AIRPORT,CITY",
            )

            return {
                "success": True,
                "data": response.data,
            }
        except ResponseError as error:
            return {
                "success": False,
                "error": str(error),
                "details": getattr(error, "description", "Unknown error"),
            }

    def get_cheapest_date_for_route(
        self,
        origin: str,
        destination: str,
    ) -> Dict[str, Any]:
        """
        Get the cheapest flight dates for a route.

        Args:
            origin: Origin airport IATA code
            destination: Destination airport IATA code

        Returns:
            Dictionary containing cheapest dates information

        Raises:
            ResponseError: If the API request fails
        """
        try:
            response = self.client.shopping.flight_dates.get(
                origin=origin.upper(),
                destination=destination.upper(),
            )

            return {
                "success": True,
                "data": response.data,
            }
        except ResponseError as error:
            return {
                "success": False,
                "error": str(error),
                "details": getattr(error, "description", "Unknown error"),
            }
