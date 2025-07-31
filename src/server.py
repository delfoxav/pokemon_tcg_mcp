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
async def get_available_types() -> list[str]:
    """ Returns a list of all available Pokémon types. """
    types = await sdk.type.list()
    if not types:
        logging.warning("No types found.")
        return []
    else:
        return types

@mcp.tool()
async def get_available_rarities() -> list[str]:
    """ Returns a list of all available Cards rarities. """
    rarities = await sdk.rarity.list()
    if not rarities:
        logging.warning("No rarities found.")
        return []
    else:
        return rarities

@mcp.tool()
async def get_available_series() -> list[dict[str, Any]]:
    """ Returns a list of all available Cards series. """

    return [tools.SerieResume_to_dict(serie) for serie in await sdk.serie.list()]

@mcp.tool()
async def get_available_sets() -> list[dict[str, Any]]:
    """ Returns a list of all available Cards sets. """
    sets = await sdk.set.list()
    if not sets:
        logging.warning("No sets found.")
        return []
    else:
        return [tools.SetResume_to_dict(set) for set in sets]

@mcp.tool()
async def get_available_trainerTypes() -> list[str]:
    """ Returns a list of all available Trainer types. """
    trainer_types = await sdk.trainerType.list()
    if not trainer_types:
        logging.warning("No trainer types found.")
        return []
    else:
        return trainer_types

@mcp.tool()
async def get_available_energyTypes() -> list[str]:
    """ Returns a list of all available Energy types. """
    energy_types = await sdk.energyType.list()
    if not energy_types:
        logging.warning("No energy types found.")
        return []
    else:
        return energy_types

@mcp.tool()
async def get_available_stages() -> list[str]:
    """ Returns a list of all available Pokémon stages. """
    stages = await sdk.stage.list()
    if not stages:
        logging.warning("No stages found.")
        return []
    else:
        return stages

@mcp.tool()
async def get_available_regulationMarks() -> list[str]:
    """ Returns a list of all available Regulation Marks. """

    regulation_marks = await sdk.regulationMark.list()
    if not regulation_marks:
        logging.warning("No regulation marks found.")
        return []
    else:
        return regulation_marks

@mcp.tool()
async def get_available_categories() -> list[str]:
    """ Returns a list of all available Card categories. """
    
    categories = await sdk.category.list()
    if not categories:
        logging.warning("No categories found.")
        return []
    else:
        return categories
    
@mcp.tool()
async def get_available_illustrators() -> list[str]:
    """ Returns a list of all available Card illustrators. """
    
    illustrators = await sdk.illustrator.list()
    if not illustrators:
        logging.warning("No illustrators found.")
        return []
    else:
        return illustrators
    

@mcp.tool()
async def get_card_by_id(card_ids: list[str]) -> list[dict]:
    """
    Returns a card or list of cards from their id.
    
    Args:
        card_ids (list[str]): The ID of the card to fetch.
    Returns:
        list[Card]: The card object(s) retrieved from the API.
    """
    try:
        cards = await asyncio.gather(*(sdk.card.get(cid) for cid in card_ids), return_exceptions=True)
        return [tools.Card_to_dict(card) for card in cards if card]
    except Exception as e:
        logging.error(f"Error fetching cards with IDs {card_ids}: {e}")
        return []
@mcp.tool()
async def get_set_by_id(set_ids: list[str]) -> list[dict]:
    """
    Returns a list of sets from their id.
    
    Args:
        set_ids (list[str]): The IDs of the sets to fetch.
    Returns:
        list[Set]: The set objects retrieved from the API.
    """
    try:
        sets = await asyncio.gather(*(sdk.set.getSync(set_id) for set_id in set_ids), return_exceptions=True)
        logging.info(f"Fetched sets with IDs {set_ids}")
        return [tools.SetResume_to_dict(set) for set in sets if set]
    except Exception as e:
        logging.error(f"Error fetching sets with IDs {set_ids}: {e}")
        return []
    

@mcp.tool()
async def get_serie_by_id(serie_ids: list[str]) -> list[dict]:
    """
    Returns a list of series from their id.
    Args:
        serie_ids (list[str]): The IDs of the series to fetch.
    Returns:
        list[Serie]: The serie objects retrieved from the API.
    """
    try:
        series = await asyncio.gather(*(sdk.serie.getSync(serie_id) for serie_id in serie_ids), return_exceptions=True)
        logging.info(f"Fetched series with IDs {serie_ids}")
        return [tools.Serie_to_dict(serie) for serie in series if serie]
    except Exception as e:
        logging.error(f"Error fetching series with IDs {serie_ids}: {e}")
        return []   


@mcp.tool()
async def get_card_by_query(query:str) -> list[dict]:
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

    cards = await sdk.card.list(eval(query))
    if not cards:
        logging.warning("No cards found for the given query.")
        return []
    
    # collect the ids of the cards
    cards_ids = [tools.CardResume_to_dict(card).get("id") for card in cards]
    
    # get the corresponding card objects
    cards = await asyncio.gather(*(sdk.card.get(card_id) for card_id in cards_ids), return_exceptions=True)

    return [tools.Card_to_dict(card) for card in cards if card]



if __name__ == "__main__":
    
    mcp.run(transport='stdio')
    
    