# Pokemon TCG MCP Server
This MCP server integrates with both the TCGdx API and JustTCG API to provide comprehensive Pokemon TCG data access. It offers tools for searching cards with advanced filtering, retrieving detai## API R## Dependencies

- **## Support

- [TCGdx API Documentation](https://tcgdx.dev/)
- [JustTCG API Documentation](https://justtcg.com/)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/docs)
- [UV Documentation](https://docs.astral.sh/uv/)** (>=1.12.2) - Model Context Protocol framework
- **httpx** (>=0.28.1) - HTTP client for API requests
- **tcgdx-sdk** (>=2.2.0) - TCGdx API SDK
- **requests** - HTTP library for JustTCG API integration

This server uses two APIs:
- **[TCGdx API](https://tcgdx.dev/)** - Provides comprehensive Pokemon TCG card data, sets, and metadata. Free to use without authentication.
- **[JustTCG API](https://justtcg.com/)** - Provides real-time pricing data and market trends. Requires API key for access. card information, browsing sets and series, accessing card images and metadata, and getting real-time pricing information from trading card stores. TCG MCP Server

A Model Context Protocol (MCP) server that provides access to Pokemon Trading Card Game data through the TCGdex API and real-time pricing data through JustTCG API. This server enables AI assistants and other MCP clients to search for cards, sets, series, pricing information, and other Pokemon TCG information.

A Model Context Protocol (MCP) server that provides access to Pokemon Trading Card Game data through the TCGdex API. This server enables AI assistants and other MCP clients to search for cards, sets, series, and other Pokemon TCG information.

## Overview

This MCP server integrates with the TCGdex API to provide comprehensive Pokemon TCG data access. It offers tools for searching cards with advanced filtering, retrieving detailed card information, browsing sets and series, and accessing card images and metadata.

## Features

- 🔍 **Card Search**: Advanced card searching with complex query support
- 📋 **Card Details**: Get comprehensive card information including stats, abilities, and attacks
- 📚 **Set & Series Management**: Browse and retrieve Pokemon TCG sets and series
- 🎨 **Image Access**: Access card images, set logos, and symbols
- 🏷️ **Metadata**: Access types, rarities, stages, regulation marks, and more
- 💰 **Real-time Pricing**: Get current market prices, price history, and trends from JustTCG
- 📊 **Price Analytics**: Access price statistics including 7-day, 30-day trends and historical data
- ⚡ **Fast Performance**: Built with FastMCP for optimal performance

## Available Tools

### Card Operations
- `get_card_by_id(card_id)` - Get detailed information about a specific card
- `get_card_by_query(query)` - Search for cards using natural language or specific criteria

### Set & Series Operations
- `get_set_by_id(set_id)` - Get complete information about a card set
- `get_serie_by_id(serie_id)` - Get details about a card series
- `get_available_sets()` - Browse all available Pokemon TCG sets
- `get_available_series()` - View all Pokemon TCG series

### Pricing & Market Data (JustTCG)
- `get_list_of_games_JustTCG()` - Get all available games with pricing data in JustTCG
- `get_sets_JustTCG(game)` - Get sets available for a specific game in the pricing database of JustTCG
- `get_cards_by_query_JustTCG(...)` - Search cards with comprehensive pricing information from JusTCG including:
  - Current market prices by condition (Near Mint, Lightly Played, etc.)
  - Price history and trends (7-day, 30-day, 90-day, 1-year)
  - Price analytics (min/max prices, standard deviation, trend slopes)
  - Multiple card variants and conditions

### Metadata Operations
- `get_available_types()` - List all Pokemon types (Fire, Water, etc.)
- `get_available_rarities()` - Show all card rarities (Common, Rare, etc.)
- `get_available_stages()` - Display Pokemon evolution stages
- `get_available_trainerTypes()` - List trainer card categories
- `get_available_energyTypes()` - Show energy card types
- `get_available_regulationMarks()` - View tournament regulation marks
- `get_available_categories()` - List card categories (Pokemon, Trainer, Energy)
- `get_available_illustrators()` - Browse card artists and illustrators

## Project Structure

```
pokemon_tcg_mcp/
├── src/
│   ├── server.py          # Main MCP server implementation
│   ├── tools.py           # Helper functions for data conversion
│   ├── justTCG.py         # JustTCG API integration for pricing data
│   └── __pycache__/
├── pyproject.toml         # Project configuration
├── requirements.txt       # Python dependencies
├── uv.lock               # UV lock file
└── README.md             # This file
```

## Installation

### Prerequisites
- Python 3.12 or higher
- [UV](https://docs.astral.sh/uv/) package manager (recommended)

### Method 1: Using UV (Recommended)

1. **Install UV** (if not already installed):
   ```powershell
   # On Windows (PowerShell)
   irm https://astral.sh/uv/install.ps1 | iex
   ```

2. **Clone the repository**:
   ```powershell
   git clone https://github.com/delfoxav/pokemon_tcg_mcp
   cd pokemon_tcg_mcp
   ```

3. **Install dependencies**:
   ```powershell
   uv sync
   ```

### Method 2: Using pip

1. **Clone the repository**:
   ```powershell
   git clone https://github.com/delfoxav/pokemon_tcg_mcp
   cd pokemon_tcg_mcp
   ```

2. **Create virtual environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

## Usage

### Running the Server

#### With UV:
```powershell
uv run --directory src server.py
```

#### With Python:
```powershell
cd src
python server.py
```

### MCP Client Configuration

Add the following configuration to your MCP client settings (e.g., `mcp.json`):

```json
{
  "servers": {
    "pokemontcg": {
      "command": "uv",
      "args": ["--directory", "C:\\path\\to\\pokemon_tcg_mcp\\src", "run", "server.py"],
      "env": {
        "TCGDX_LANGUAGE": "en",
        "TCGDX_IMAGE_QUALITY": "low",
        "TCGDX_IMAGE_FORMAT": "png",
        "JUSTTCG_API_KEY": "your_justtcg_api_key_here"// This is optional, can be left empty if not using JustTCG
      }
    }
  }
}
```

Replace `C:\\path\\to\\pokemon_tcg_mcp` with the actual path to your project directory.

### JustTCG API Key Setup

To access pricing data, you'll need a JustTCG API key:

1. **Get an API Key**: Visit [JustTCG](https://justtcg.com/) to obtain an API key
2. **Set Environment Variable**: Add your API key to the environment configuration above
3. **Without API Key**: The server will still work for TCGdex data, but pricing features will be unavailable

## Usage Examples with LLMs

Once the MCP server is configured with your AI assistant, you can ask natural language questions about Pokemon TCG cards:

### Card Search Examples

**"Find all Charizard cards"**
The AI will use the `get_card_by_query` tool to search for cards containing "Charizard" in the name and return detailed information about each card including stats, abilities, and images.

**"Show me rare Fire-type Pokemon from the Base Set"**
The AI will search for cards matching these criteria and display comprehensive details about each card.

**"What are all the available Pokemon types?"**
The AI will call `get_available_types()` and list all Pokemon types like Fire, Water, Grass, etc.

### Set and Series Information

**"Tell me about the Base Set"**
The AI will use `get_set_by_id()` to retrieve detailed information about the Base Set including release date, card count, and all cards in the set.

**"What Pokemon sets are available?"**
The AI will call `get_available_sets()` and provide a comprehensive list of all available sets with their logos and basic information.

### Card Details

**"Get details for card swsh1-25"**
The AI will use `get_card_by_id()` to fetch complete information about the specific card including:
- Card image
- Stats (HP, attacks, abilities)
- Rarity and set information
- Artist and illustrator details

### Advanced Queries

**"Find all Pokemon with abilities from the latest regulation"**
The AI will construct appropriate queries to find Pokemon cards that have abilities from recent regulation marks.

**"Show me all trainer cards from Team Rocket series"**
The AI will search for trainer-type cards from the specified series and display their effects and artwork.

### Pricing Queries

**"What's the current price of Charizard Base Set in Near Mint condition?"**
The AI will use `get_cards_by_query_JustTCG()` to find the specific card and return current market pricing with condition-based variants.

**"Show me price trends for Pikachu cards over the last 30 days"**
The AI will retrieve pricing data including price history, trends, and analytics for Pikachu cards.

**"Find the cheapest Base Set booster box available"**
The AI will search for sealed products and return pricing information sorted by current market value.

**"What Pokemon TCG sets have pricing data available?"**
The AI will use `get_sets_JustTCG()` to show all sets with available pricing information.

### Metadata Exploration

**"What rarities are available for Pokemon cards?"**
The AI will call `get_available_rarities()` and list all possible card rarities.

**"Show me all available illustrators"**
The AI will use `get_available_illustrators()` to display a list of all card artists and illustrators.

## API Reference

This server uses the [TCGdex API](https://tcgdex.dev/) which provides comprehensive Pokemon TCG data in multiple languages. The API is free to use and doesn't require authentication.

The prices information is provided by the [JustTCG API](https://justtcg.com/), which requires an API key for access. The JustTCG API provides real-time pricing data, market trends, and detailed card information. All the prices are based on TCGPlayer prices.

## Dependencies

- **mcp[cli]** (>=1.12.2) - Model Context Protocol framework
- **httpx** (>=0.28.1) - HTTP client for API requests
- **tcgdex-sdk** (>=2.2.0) - TCGdex API SDK

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

- [TCGdx API Documentation](https://tcgdex.dev/)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/docs)
- [UV Documentation](https://docs.astral.sh/uv/)
- [JustTCG API Documentation](https://justtcg.com/)
- [TCGPlayer prices](https://www.tcgplayer.com/)
## Troubleshooting

### Common Issues

1. **UV not found**: Make sure UV is installed and in your PATH
2. **Python version error**: Ensure you have Python 3.12 or higher
3. **Import errors**: Run `uv sync` to install all dependencies
4. **Connection errors**: Check your internet connection for API access
5. **JustTCG pricing unavailable**: Verify your API key is set correctly in the environment variables

## Disclaimer

This project is not affiliated with Nintendo or The Pokémon Company.
