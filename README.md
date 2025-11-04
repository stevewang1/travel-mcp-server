# Travel MCP Server

A comprehensive Model Context Protocol (MCP) server for travel aggregation, providing AI assistants with access to flight search, hotel booking, airport information, and real-time flight tracking.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-1.20.0-green.svg)](https://modelcontextprotocol.io/)

## Quick Links

- [Quick Start Guide](QUICKSTART.md) - Get started in 5 minutes
- [API Documentation](#available-tools) - See all available tools
- [Troubleshooting](#troubleshooting) - Common issues and solutions

## Features

### Flight Search & Booking
- **Search Flights**: Find flight offers between airports with prices, airlines, and schedules
- **Find Cheapest Dates**: Discover the most affordable travel dates for flexible planning
- **Flight Tracking**: Real-time flight status, location, altitude, and ETA

### Hotel Search
- **Search Hotels**: Find hotels with availability, pricing, amenities, and location
- **Multi-city Support**: Search hotels in any city worldwide

### Airport Information
- **Airport Search**: Find airports by city name or location
- **Airport Details**: Get comprehensive airport information including timezone and facilities
- **Route Information**: View all flights between two airports

## APIs Used

### Primary: Amadeus Self-Service API
- Flight Offers Search
- Hotel Search
- Airport & City Search
- Cheapest Date Search

[Get your Amadeus API keys](https://developers.amadeus.com/) (Free tier available with monthly quota)

### Secondary: AviationStack API
- Real-time Flight Tracking
- Flight Status Updates
- Route Information

[Get your AviationStack API key](https://aviationstack.com/) (100 free requests/month)

## Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Setup Steps

1. **Clone the repository**
```bash
cd travel-mcp-server
```

2. **Create a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -e .
```

4. **Set up environment variables**
```bash
cp .env.example .env
```

Edit the `.env` file with your API credentials:
```env
# Amadeus API Credentials (Required)
AMADEUS_CLIENT_ID=your_amadeus_api_key_here
AMADEUS_CLIENT_SECRET=your_amadeus_api_secret_here
AMADEUS_ENV=test  # Use 'production' when ready

# AviationStack API Key (Optional - for flight tracking)
AVIATIONSTACK_API_KEY=your_aviationstack_key_here
```

### Getting API Keys

#### Amadeus API
1. Go to [Amadeus for Developers](https://developers.amadeus.com/)
2. Click "Register" to create an account
3. Go to "My Self-Service Workspace"
4. Click "Create New App"
5. Copy your API Key and API Secret

#### AviationStack (Optional)
1. Go to [AviationStack](https://aviationstack.com/)
2. Sign up for a free account
3. Copy your API key from the dashboard

## Usage with Claude Desktop

### Configuration

Add this to your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "travel": {
      "command": "/path/to/travel-mcp-server/venv/bin/python",
      "args": [
        "-m",
        "travel_mcp.server"
      ],
      "env": {
        "AMADEUS_CLIENT_ID": "your_amadeus_api_key",
        "AMADEUS_CLIENT_SECRET": "your_amadeus_api_secret",
        "AMADEUS_ENV": "test",
        "AVIATIONSTACK_API_KEY": "your_aviationstack_key"
      }
    }
  }
}
```

### Restart Claude Desktop

After adding the configuration, restart Claude Desktop to load the MCP server.

## Available Tools

### 1. search_flights
Search for flight offers between two airports.

**Parameters:**
- `origin` (required): Origin airport IATA code (e.g., 'JFK')
- `destination` (required): Destination airport IATA code (e.g., 'LAX')
- `departure_date` (required): Departure date (YYYY-MM-DD)
- `return_date` (optional): Return date (YYYY-MM-DD)
- `adults` (optional): Number of passengers (default: 1)
- `max_results` (optional): Max results to return (default: 10)

**Example:**
```
Find me flights from New York (JFK) to London (LHR) on December 25, 2025, returning January 5, 2026
```

### 2. search_hotels
Search for hotels in a city with availability and pricing.

**Parameters:**
- `city_code` (required): City IATA code (e.g., 'NYC', 'PAR')
- `check_in_date` (required): Check-in date (YYYY-MM-DD)
- `check_out_date` (required): Check-out date (YYYY-MM-DD)
- `adults` (optional): Number of guests (default: 1)

**Example:**
```
Find hotels in Paris for December 20-25, 2025 for 2 adults
```

### 3. search_airports
Search for airports by city name.

**Parameters:**
- `city_name` (required): Name of the city

**Example:**
```
What airports are in Tokyo?
```

### 4. find_cheapest_dates
Find the cheapest dates to fly between two airports.

**Parameters:**
- `origin` (required): Origin airport IATA code
- `destination` (required): Destination airport IATA code

**Example:**
```
When is the cheapest time to fly from San Francisco to Sydney?
```

### 5. track_flight
Track a flight in real-time (requires AviationStack API key).

**Parameters:**
- `flight_iata` or `flight_icao` (one required): Flight code

**Example:**
```
Track flight AA100
```

### 6. get_flights_by_route
Get all flights on a specific route.

**Parameters:**
- `dep_iata` (optional): Departure airport IATA code
- `arr_iata` (optional): Arrival airport IATA code

**Example:**
```
What flights go from LAX to JFK?
```

### 7. get_airport_info
Get detailed information about an airport.

**Parameters:**
- `iata_code` (required): Airport IATA code

**Example:**
```
Tell me about Heathrow airport (LHR)
```

## Common Airport Codes

- **JFK** - New York John F. Kennedy
- **LAX** - Los Angeles International
- **LHR** - London Heathrow
- **CDG** - Paris Charles de Gaulle
- **NRT** - Tokyo Narita
- **DXB** - Dubai International
- **SYD** - Sydney Airport
- **SFO** - San Francisco International

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black src/
isort src/
```

### Type Checking
```bash
mypy src/
```

## API Rate Limits

### Amadeus Free Tier
- **Test Environment**: Fixed monthly quota
- **Production**: Free monthly quota + pay-as-you-go

### AviationStack Free Tier
- **100 API calls per month**
- 30-60 second data delay

## Troubleshooting

### "AMADEUS_CLIENT_ID and AMADEUS_CLIENT_SECRET must be set"
- Ensure you've created a `.env` file with your credentials
- Or set them in your Claude Desktop config

### "Unknown tool" error
- Check that your API keys are valid
- Ensure clients are initialized (check server logs)

### API Rate Limit Exceeded
- Amadeus: Wait for monthly quota reset or upgrade plan
- AviationStack: Wait for monthly reset or upgrade plan

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this in your projects!

## Support

For issues and questions:
- Open an issue on GitHub
- Check the [Amadeus API Documentation](https://developers.amadeus.com/)
- Check the [AviationStack Documentation](https://aviationstack.com/documentation)

## Roadmap

- [ ] Add price alerts and monitoring
- [ ] Add car rental search
- [ ] Add train/rail search (Eurail, Amtrak)
- [ ] Add activity/tour booking
- [ ] Add travel insurance options
- [ ] Add visa requirement checker
- [ ] Add currency converter
- [ ] Add weather forecasts for destinations
- [ ] Add caching for repeated queries
- [ ] Add more travel APIs (Booking.com, Expedia)

## Acknowledgments

Built with:
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Amadeus for Developers](https://developers.amadeus.com/)
- [AviationStack](https://aviationstack.com/)

---

**Happy Traveling!** ✈️ 🏨 🌍
