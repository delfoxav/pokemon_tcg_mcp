"""MCP Server implementation for Pokemon TCG API"""

import logging
from typing import Any, Union

import urllib
import httpx
from mcp.server.fastmcp import FastMCP

from tcgdexsdk import TCGdex
from tcgdexsdk import Card, Set, Serie, SerieResume, SetResume, CardResume
import time
import asyncio

import tools
from tcgdexsdk import Query


sdk = TCGdex("en")

# initialize FastMCP server
mcp = FastMCP("Pokemon TCG MCP Server")


@mcp.tool()
def get_available_types() -> list[str]:
    """ Returns a list of all available Pokémon types. """
    return sdk.type.listSync()

@mcp.tool()
def get_available_rarities() -> list[str]:
    """ Returns a list of all available Cards rarities. """
    return sdk.rarity.listSync()

@mcp.tool()
async def get_available_series() -> list[dict[str, Any]]:
    """ Returns a list of all available Cards series. """

    return [tools.SerieResume_to_dict(serie) for serie in await sdk.serie.list()]

@mcp.tool()
def get_available_sets() -> list[dict[str, Any]]:
    """ Returns a list of all available Cards sets. """

    return [tools.SetResume_to_dict(set) for set in sdk.set.listSync()]


@mcp.tool()
def get_available_trainerTypes() -> list[str]:
    """ Returns a list of all available Trainer types. """
    return sdk.trainerType.listSync()

@mcp.tool()
def get_available_energyTypes() -> list[str]:
    """ Returns a list of all available Energy types. """
    return sdk.energyType.listSync()

@mcp.tool()
def get_available_stages() -> list[str]:
    """ Returns a list of all available Pokémon stages. """
    return sdk.stage.listSync()

@mcp.tool()
def get_available_regulationMarks() -> list[str]:
    """ Returns a list of all available Regulation Marks. """
    return sdk.regulationMark.listSync()

@mcp.tool()
def get_available_categories() -> list[str]:
    """ Returns a list of all available Card categories. """
    return sdk.category.listSync()

@mcp.tool()
def get_available_illustrators() -> list[str]:
    """ Returns a list of all available Card illustrators. """
    return sdk.illustrator.listSync()

@mcp.tool()
def get_card_by_id(card_id: str) -> dict:
    """
    Returns a card or list of cards from their id.
    
    Args:
        card_id (str): The ID of the card to fetch. 
    Returns:
        Card: The card object retrieved from the API.
    """
    # Check if card_id is a list, if so prepare all the fetches
    try:
        card = sdk.card.getSync(card_id)
        logging.info(f"Fetched card with ID {card_id}")
        if not card:
            logging.warning(f"No card found with ID {card_id}")
            return None
        return tools.Card_to_dict(card)
    except Exception as e:
        logging.error(f"Error fetching card with ID {card_id}: {e}")
        return None

@mcp.tool()
def get_set_by_id(set_id: str) -> dict:
    """
    Returns a set from its id.
    
    Args:
        set_id (str): The ID of the set to fetch.
    Returns:
        Set: The set object retrieved from the API.
    """
    try:
        set = sdk.set.getSync(set_id)
        logging.info(f"Fetched set with ID {set_id}")
        if not set:
            logging.warning(f"No set found with ID {set_id}")
            return None
        return tools.SetResume_to_dict(set)
    except Exception as e:
        logging.error(f"Error fetching set with ID {set_id}: {e}")
     
        return None

@mcp.tool()
def get_serie_by_id(serie_id: str) -> dict:
    """
    Returns a serie from its id.
    
    Args:
        serie_id (str): The ID of the serie to fetch.
    Returns:
        Serie: The serie object retrieved from the API.
    """
    try:
        serie = sdk.serie.getSync(serie_id)
        logging.info(f"Fetched serie with ID {serie_id}")
        if not serie:
            logging.warning(f"No serie found with ID {serie_id}")
            return None
        return tools.Serie_to_dict(serie)
    except Exception as e:
        logging.error(f"Error fetching serie with ID {serie_id}: {e}")
        return None


@mcp.tool()
def get_card_by_query(query:str) -> list[dict]:
    """
    Returns a list of cards based on a query.
    
    The query should be defined using the TCGdex Query syntax.
    
    it starts with the Query class, followed by the search parameters.

    The query class has several methods to filter the results, such as:
    - 'equal': to match exact values takes two parameters: the field to check and the value to compare
    - 'contains': to match values that contain a substring takes two parameters: the field to check and the value to compare
    - 'sort': to sort the results by a specific field takes two parameters the field to sort by and the order ('asc' or 'desc')
    - 'greaterOrEqualThan': to filter results greater than or equal to a value takes two parameters: the field to check and the value to compare
    - 'lessOrEqualThan': to filter results less than or equal to a value takes two parameters: the field to check and the value to compare
    - 'greaterThan': to filter results greater than a value takes two parameters: the field to check and the value to compare
    - 'lessThan': to filter results less than a value takes two parameters: the field to check and the value to compare
    - 'isNull': to filter results where a field is null takes one parameter: the field to check
    - 'paginate': to limit the number of results returned takes two parameters: 'page' and 'itemsPerPage'    
    - 'notEqual': to match values that are not equal to a specific value takes two parameters: the field to check and the value to compare
    - 'notContains': to match values that do not contain a substring takes two parameters: the field to check and the value to compare
    - 'notNull': to filter results where a field is not null takes one parameter: the field to check
    
    Following the Query class, you can chain these methods to build your query.
    
    example:
    - To get all cards from the "Base Set" series that are of the "Fire" type and have a rarity of "Rare":
      ```python
      query = Query().equal("series.name", "Base Set").equal("type", "Fire").equal("rarity", "Rare")
      ```
    - To get all the pokemon from the regulation mark "D" that have an ability:
    ```python
    query = Query().equal("category", "Pokemon").equal("regulationMark", "D").notNull("ability")
    ```
    
    Args:
        query (str): The query to search for cards.
    Returns:
        list[Card]: A list of card objects matching the query.
    """
    
    results = sdk.card.listSync(eval(query))
    if not results:
        logging.warning("No cards found for the given query.")
        return []
    else:
        return [tools.Card_to_dict(sdk.card.getSync(card.id)) for card in results]


if __name__ == "__main__":
    
    mcp.run(transport='stdio')
    
    