# Quick Start Guide - Travel MCP Server

Get your Travel MCP Server up and running in 5 minutes!

## Step 1: Get Your API Keys (5 minutes)

### Amadeus API (Required)
1. Visit [https://developers.amadeus.com/](https://developers.amadeus.com/)
2. Click **"Register"** in the top right
3. Fill out the registration form
4. Check your email and click the activation link
5. Login and go to **"My Self-Service Workspace"**
6. Click **"Create New App"**
7. Give it a name (e.g., "Travel MCP")
8. Copy your **API Key** and **API Secret**

### AviationStack API (Optional - for flight tracking)
1. Visit [https://aviationstack.com/](https://aviationstack.com/)
2. Click **"Get Free API Key"**
3. Sign up with your email
4. Copy your API key from the dashboard

## Step 2: Configure Environment Variables (1 minute)

Create a `.env` file in the project root:

```bash
cd /Users/levtheswag/VSCodestuff/travel-mcp-server
cp .env.example .env
```

Edit `.env` and add your keys:

```env
AMADEUS_CLIENT_ID=your_amadeus_api_key_here
AMADEUS_CLIENT_SECRET=your_amadeus_api_secret_here
AMADEUS_ENV=test

# Optional
AVIATIONSTACK_API_KEY=your_aviationstack_key_here
```

## Step 3: Configure Claude Desktop (2 minutes)

### Find Your Config File

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### Edit the Config

Add this to the config file (create it if it doesn't exist):

```json
{
  "mcpServers": {
    "travel": {
      "command": "/Users/levtheswag/VSCodestuff/travel-mcp-server/venv/bin/python",
      "args": [
        "-m",
        "travel_mcp.server"
      ],
      "env": {
        "AMADEUS_CLIENT_ID": "YOUR_AMADEUS_KEY_HERE",
        "AMADEUS_CLIENT_SECRET": "YOUR_AMADEUS_SECRET_HERE",
        "AMADEUS_ENV": "test",
        "AVIATIONSTACK_API_KEY": "YOUR_AVIATIONSTACK_KEY_HERE"
      }
    }
  }
}
```

**Important**: Replace the API keys in the `env` section with your actual keys!

## Step 4: Restart Claude Desktop

1. Quit Claude Desktop completely (Cmd+Q on Mac)
2. Reopen Claude Desktop
3. Look for the 🔌 icon in the bottom right - it should show "travel" as connected

## Step 5: Test It Out!

Try these prompts in Claude:

### Test Flight Search
```
Find me flights from New York (JFK) to London (LHR) on January 15, 2026
```

### Test Hotel Search
```
Find hotels in Paris (PAR) for February 10-15, 2026
```

### Test Airport Search
```
What airports are in Tokyo?
```

### Test Flight Tracking (if you have AviationStack key)
```
Track flight AA100
```

## Troubleshooting

### "Tool not found" error
- Make sure you restarted Claude Desktop after editing the config
- Check that the path to the Python executable is correct
- Verify your virtual environment is activated

### "API authentication failed"
- Double-check your API keys in the config
- Make sure you copied both the API Key AND API Secret for Amadeus
- For Amadeus, make sure you're using `test` environment first

### "No results found"
- Airport codes must be valid IATA codes (3 letters)
- Dates must be in YYYY-MM-DD format
- For hotels, use city codes not airport codes (e.g., PAR for Paris, not CDG)

### Check Server Logs
If Claude Desktop isn't connecting:
1. Open Claude Desktop
2. Click the 🔌 icon
3. Look for error messages next to "travel"

## Common Airport Codes Reference

| City | Code | Airport |
|------|------|---------|
| New York | JFK | John F. Kennedy |
| Los Angeles | LAX | Los Angeles Intl |
| London | LHR | Heathrow |
| Paris | CDG | Charles de Gaulle |
| Tokyo | NRT | Narita |
| Dubai | DXB | Dubai Intl |
| Sydney | SYD | Sydney Airport |
| San Francisco | SFO | San Francisco Intl |
| Chicago | ORD | O'Hare |
| Miami | MIA | Miami Intl |

## API Limits

### Amadeus Free Tier
- **Test Environment**: Monthly quota for testing
- **Production**: Free monthly quota + pay-as-you-go
- Check your usage at [developers.amadeus.com](https://developers.amadeus.com/)

### AviationStack Free Tier
- **100 API calls per month**
- Resets on the 1st of each month
- Data has 30-60 second delay

## Next Steps

- Read the full [README.md](README.md) for all features
- Try different search parameters
- Explore hotel amenities and filters
- Use cheapest date search for flexible travel planning

## Support

Having issues?
1. Check the [README.md](README.md) for detailed documentation
2. Verify your API keys are valid
3. Make sure dates are in the future
4. Ensure airport codes are valid IATA codes

---

Happy traveling! ✈️
