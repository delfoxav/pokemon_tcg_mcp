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
- `get_card_by_id(card_id)` - Retrieve a specific card by its ID
- `get_card_by_query(query)` - Search cards using advanced TCGdx Query syntax

### Set & Series Operations
- `get_set_by_id(set_id)` - Get detailed set information
- `get_serie_by_id(serie_id)` - Get detailed series information
- `get_available_sets()` - List all available sets
- `get_available_series()` - List all available series

### Metadata Operations
- `get_available_types()` - Get all Pokemon types
- `get_available_rarities()` - Get all card rarities
- `get_available_stages()` - Get all Pokemon stages
- `get_available_trainerTypes()` - Get all trainer types
- `get_available_energyTypes()` - Get all energy types
- `get_available_regulationMarks()` - Get all regulation marks
- `get_available_categories()` - Get all card categories
- `get_available_illustrators()` - Get all card illustrators

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
   git clone <repository-url>
   cd pokemon_tcg_mcp
   ```

3. **Install dependencies**:
   ```powershell
   uv sync
   ```

### Method 2: Using pip

1. **Clone the repository**:
   ```powershell
   git clone <repository-url>
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
      "args": [
        "--directory",
        "C:\\path\\to\\pokemon_tcg_mcp\\src",
        "run",
        "server.py"
      ]
    }
  }
}
```

Replace `C:\\path\\to\\pokemon_tcg_mcp` with the actual path to your project directory.

## Query Syntax

The `get_card_by_query` tool uses TCGdx Query syntax for advanced card searching:

### Basic Query Methods
- `equal(field, value)` - Exact match
- `contains(field, value)` - Substring match
- `sort(field, order)` - Sort results ('asc' or 'desc')
- `paginate(page, itemsPerPage)` - Limit results
- `notEqual(field, value)` - Not equal to value
- `greaterThan(field, value)` - Greater than value
- `lessThan(field, value)` - Less than value
- `isNull(field)` - Field is null
- `notNull(field)` - Field is not null

### Example Queries

**Find all Fire-type Rare cards from Base Set:**
```python
Query().equal("series.name", "Base Set").equal("type", "Fire").equal("rarity", "Rare")
```

**Find Pokemon with abilities from regulation mark D:**
```python
Query().equal("category", "Pokemon").equal("regulationMark", "D").notNull("ability")
```

**Find cards containing "Pikachu" sorted by name:**
```python
Query().contains("name", "Pikachu").sort("name", "asc")
```

## API Reference

This server uses the [TCGdx API](https://www.tcgdx.net/) which provides comprehensive Pokemon TCG data in multiple languages. The API is free to use and doesn't require authentication.

## Dependencies

- **mcp[cli]** (>=1.12.2) - Model Context Protocol framework
- **httpx** (>=0.28.1) - HTTP client for API requests
- **tcgdx-sdk** (>=2.2.0) - TCGdx API SDK
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

- [TCGdx API Documentation](https://www.tcgdx.net/docs)
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
