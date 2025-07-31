# Pokemon TCG MCP Server

A Model Context Protocol (MCP) server that provides access to Pokemon Trading Card Game data through the TCGdex API. This server enables AI assistants and other MCP clients to search for cards, sets, series, and other Pokemon TCG information.

## Overview

This MCP server integrates with the TCGdex API to provide comprehensive Pokemon TCG data access. It offers tools for searching cards with advanced filtering, retrieving detailed card information, browsing sets and series, and accessing card images and metadata.

## Features

- 🔍 **Card Search**: Advanced card searching with complex query support
- 📋 **Card Details**: Get comprehensive card information including stats, abilities, and attacks
- 📚 **Set & Series Management**: Browse and retrieve Pokemon TCG sets and series
- 🎨 **Image Access**: Access card images, set logos, and symbols
- 🏷️ **Metadata**: Access types, rarities, stages, regulation marks, and more
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
        "TCGDX_LANGUAGE": "en" 
      }
    }
  }
}
```

Replace `C:\\path\\to\\pokemon_tcg_mcp` with the actual path to your project directory.

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

### Metadata Exploration

**"What rarities are available for Pokemon cards?"**
The AI will call `get_available_rarities()` and list all possible card rarities.

**"Show me all available illustrators"**
The AI will use `get_available_illustrators()` to display a list of all card artists and illustrators.

## API Reference

This server uses the [TCGdex API](https://tcgdex.dev/) which provides comprehensive Pokemon TCG data in multiple languages. The API is free to use and doesn't require authentication.

## Dependencies

- **mcp[cli]** (>=1.12.2) - Model Context Protocol framework
- **httpx** (>=0.28.1) - HTTP client for API requests
- **tcgdex-sdk** (>=2.2.0) - TCGdex API SDK
- **pokemontcgsdk** (>=3.4.0) - Pokemon TCG API SDK

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

## Troubleshooting

### Common Issues

1. **UV not found**: Make sure UV is installed and in your PATH
2. **Python version error**: Ensure you have Python 3.12 or higher
3. **Import errors**: Run `uv sync` to install all dependencies
4. **Connection errors**: Check your internet connection for API access

## Disclaimer

This project is not affiliated with Nintendo or The Pokémon Company.
