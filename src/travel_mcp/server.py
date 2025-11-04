"""Travel MCP Server - Main server implementation."""

import asyncio
import json
from typing import Any, Optional
from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from mcp.server.stdio import stdio_server

from .amadeus_client import AmadeusClient
from .aviation_client import AviationStackClient


# Initialize clients
try:
    amadeus_client = AmadeusClient()
except ValueError as e:
    print(f"Warning: Amadeus client not initialized: {e}")
    amadeus_client = None  # type: ignore

try:
    aviation_client = AviationStackClient()
except ValueError as e:
    print(f"Warning: AviationStack client not initialized: {e}")
    aviation_client = None  # type: ignore


# Initialize MCP server
app = Server("travel-mcp-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    tools = []

    # Amadeus tools
    if amadeus_client:
        tools.extend([
            Tool(
                name="search_flights",
                description="Search for flight offers between two airports. Returns flight options with prices, airlines, and schedules.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "origin": {
                            "type": "string",
                            "description": "Origin airport IATA code (e.g., 'JFK', 'LAX')",
                        },
                        "destination": {
                            "type": "string",
                            "description": "Destination airport IATA code (e.g., 'LHR', 'CDG')",
                        },
                        "departure_date": {
                            "type": "string",
                            "description": "Departure date in YYYY-MM-DD format",
                        },
                        "return_date": {
                            "type": "string",
                            "description": "Return date in YYYY-MM-DD format (optional for one-way flights)",
                        },
                        "adults": {
                            "type": "integer",
                            "description": "Number of adult passengers (default: 1)",
                            "default": 1,
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of results to return (default: 10)",
                            "default": 10,
                        },
                    },
                    "required": ["origin", "destination", "departure_date"],
                },
            ),
            Tool(
                name="search_hotels",
                description="Search for hotels in a city with availability and pricing. Returns hotel options with rates, amenities, and location.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "city_code": {
                            "type": "string",
                            "description": "City IATA code (e.g., 'NYC', 'PAR', 'LON')",
                        },
                        "check_in_date": {
                            "type": "string",
                            "description": "Check-in date in YYYY-MM-DD format",
                        },
                        "check_out_date": {
                            "type": "string",
                            "description": "Check-out date in YYYY-MM-DD format",
                        },
                        "adults": {
                            "type": "integer",
                            "description": "Number of adults (default: 1)",
                            "default": 1,
                        },
                    },
                    "required": ["city_code", "check_in_date", "check_out_date"],
                },
            ),
            Tool(
                name="search_airports",
                description="Search for airports by city name or location. Returns airport codes, names, and locations.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "city_name": {
                            "type": "string",
                            "description": "Name of the city to search for airports",
                        },
                    },
                    "required": ["city_name"],
                },
            ),
            Tool(
                name="find_cheapest_dates",
                description="Find the cheapest dates to fly between two airports. Useful for flexible travel planning.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "origin": {
                            "type": "string",
                            "description": "Origin airport IATA code",
                        },
                        "destination": {
                            "type": "string",
                            "description": "Destination airport IATA code",
                        },
                    },
                    "required": ["origin", "destination"],
                },
            ),
        ])

    # AviationStack tools
    if aviation_client:
        tools.extend([
            Tool(
                name="track_flight",
                description="Track a flight in real-time. Get current status, location, altitude, and estimated arrival.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "flight_iata": {
                            "type": "string",
                            "description": "IATA flight code (e.g., 'AA100')",
                        },
                        "flight_icao": {
                            "type": "string",
                            "description": "ICAO flight code (e.g., 'AAL100')",
                        },
                    },
                },
            ),
            Tool(
                name="get_flights_by_route",
                description="Get all flights on a specific route. Shows all airlines flying between two airports.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "dep_iata": {
                            "type": "string",
                            "description": "Departure airport IATA code",
                        },
                        "arr_iata": {
                            "type": "string",
                            "description": "Arrival airport IATA code",
                        },
                    },
                },
            ),
            Tool(
                name="get_airport_info",
                description="Get detailed information about an airport including location, timezone, and facilities.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "iata_code": {
                            "type": "string",
                            "description": "Airport IATA code (e.g., 'JFK')",
                        },
                    },
                    "required": ["iata_code"],
                },
            ),
        ])

    return tools


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""

    try:
        # Amadeus tools
        if name == "search_flights" and amadeus_client:
            result = amadeus_client.search_flights(
                origin=arguments["origin"],
                destination=arguments["destination"],
                departure_date=arguments["departure_date"],
                return_date=arguments.get("return_date"),
                adults=arguments.get("adults", 1),
                max_results=arguments.get("max_results", 10),
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "search_hotels" and amadeus_client:
            result = amadeus_client.search_hotels(
                city_code=arguments["city_code"],
                check_in_date=arguments["check_in_date"],
                check_out_date=arguments["check_out_date"],
                adults=arguments.get("adults", 1),
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "search_airports" and amadeus_client:
            result = amadeus_client.search_airport_by_city(
                city_name=arguments["city_name"]
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "find_cheapest_dates" and amadeus_client:
            result = amadeus_client.get_cheapest_date_for_route(
                origin=arguments["origin"],
                destination=arguments["destination"],
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        # AviationStack tools
        elif name == "track_flight" and aviation_client:
            result = aviation_client.track_flight(
                flight_iata=arguments.get("flight_iata"),
                flight_icao=arguments.get("flight_icao"),
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "get_flights_by_route" and aviation_client:
            result = aviation_client.get_flights_by_route(
                dep_iata=arguments.get("dep_iata"),
                arr_iata=arguments.get("arr_iata"),
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "get_airport_info" and aviation_client:
            result = aviation_client.get_airport_info(
                iata_code=arguments["iata_code"]
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        else:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "error": f"Unknown tool: {name} or client not initialized"
                })
            )]

    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({
                "error": str(e),
                "tool": name,
            })
        )]


async def main() -> None:
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
