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
import justTCG
from tcgdexsdk import Query

import os
language = os.getenv("TCGDEX_LANGUAGE", "en")

sdk = TCGdex(language)

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


if os.getenv("JUSTTCG_API_KEY"):

    @mcp.tool()
    def get_games_JustTCG() -> list[dict]:
        """
        
        JustTCG is an api that provides access to trading card stores for various games.
        Using this tool, you can access the list of games available in JustTCG.
        
        Returns a list of games available in JustTCG. With general information such as:
        - id: The unique identifier for the game.
        - name: The name of the game.
        - card_count: The total number of cards available in the game.
        - sets_count: The total number of sets available in the game.
        - game_id: The unique identifier for the game in the JustTCG API.
        
        Returns:
            list[dict]: A list of games with their details.
        """
        return justTCG.get_list_of_games()

    @mcp.tool()
    def get_sets_JustTCG(game: str) -> list[dict]:
        """
        JustTCG is an api that provides access to trading card stores for various games.
        Using this tool, you can access the list of sets available in JustTCG for a specific game.

        Returns a list of sets for a specific game. With general information such as:
        - id: The unique identifier for the set.
        - name: The name of the set.
        - game_id: The unique identifier for the game in the JustTCG API.
        - game: The name of the game.
        - card_count: The total number of cards available in the set.
        
        Args:
            game (str): The game id to fetch sets for.
            
        Returns:
            list[dict]: A list of sets with their details.
        """
        return justTCG.get_list_of_sets(game)

    @mcp.tool()
    def get_cards_by_query_JustTCG(
        tcgplayerId: str = None,
        cardId: str = None,
        variantId: str = None,
        condition: str = None,
        game: str = None,
        set: str = None,
        order_by: str = None,
        order_direction: str = None,
        limit: int = 20,
        offset: int = 0,
        search_query: str = None
    ) -> list[dict]:
        """
        JustTCG is an api that provides access to trading card stores for various games.
        Using this tool, you can find specific cards based on various parameters.
        
        
        Returns a list of cards based on a query.
        Note: The tcgplayerId, cardId or variantId will take precedence over any search query if any of those are provided.
        
        Avoid using multiple identifiers in the same object.
        variantId will take precedence over tcgplayerId and tcgplayerId will take precedence over cardId.

        Args:
            tcgplayerId (str, optional): The TCGPlayer ID of the card.
            cardId (str, optional): The ID of the card.
            variantId (str, optional): The variant ID of the card.
            condition (str, optional): valid conditions are [Sealed, Near Mint, Lightly Played, Moderately Played, Heavily Played, Damaged] or abreviations [S, NM, LP, MP, HP, D].
            game (str, optional): The name of the game to filter cards by.
            set (str, optional): The name of the set to filter cards by.
            order_by (str, optional): The field to order the results by.
            order_direction (str, optional): The direction to order the results (asc or desc).
            limit (int, optional): The number of results to return per page. Default is 20.
            offset (int, optional): Number of results to skip. Default is 0.
            search_query (str, optional): A search query string to filter cards by name or other attributes. A search query looks like this:
            
        Returns:
            list[dict]: A list of cards matching the query.
            
            A card object will contain the following fields:
            - id: The unique identifier for the card.
            - name: The name of the card.
            - game: The name of the game the card belongs to.
            - set: The name of the set the card belongs to.
            - number: The card number in the set.
            - tcgplayerId: The TCGPlayer ID of the card.
            - rarity: The rarity of the card.
            - details: additional card specific details.
            - variants: an array of variants objects.
            
            A variant object will contain the following fields:
            - id: The unique identifier for the variant.
            - condition: The condition of the variant (e.g., Near Mint, Lightly Played).
            - printing: The printing type (e.g, "Normal", "Foil")
            - price: the current price of the variant in USD.
            - lastUpdated: The date and time when the variant was last updated Unix timestamp in seconds.
            - priceChange24hr: The percentage change in price over the last 24 hours.
            - priceChange7d: The percentage change in price over the last 7 days.
            - avgPrice: The average price over the default time period.
            - priceHistory (list[dict]): A list of price history objects, each containing:
                - t: The date of the price record in Unix timestamp format.
                - p: The price of the card at the given date.
            - minPrice7d: The minimum price of the variant over the last 7 days.
            - maxPrice7d: The maximum price of the variant over the last 7 days.
            - stddevPopPrice7d: The population standard deviation of the price over the last 7 days.
            - covPrice7d: The coefficient of variation of the price over the last 7 days.
            - iqrPrice7d: The interquartile range of the price over the last 7 days.
            - trendSlope7d: The slope of the price trend over the last 7 days.
            - priceChangesCount7d: The number of price changes over the last 7 days.
            - priceChange30d: The percentage change in price over the last 30 days.
            - avgPrice30d: The average price over the last 30 days.
            - minPrice30d: The minimum price of the variant over the last 30 days.
            - maxPrice30d: The maximum price of the variant over the last 30 days.
            - priceHistory30d (list[dict]): A list of price history objects for the last 30 days, each containing:
                - t: The date of the price record in Unix timestamp format.
                - p: The price of the card at the given date.
            - stddevPopPrice30d: The population standard deviation of the price over the last 30 days.
            - covPrice30d: The coefficient of variation of the price over the last 30 days.
            - iqrPrice30d: The interquartile range of the price over the last 30 days.
            - trendSlope30d: The slope of the price trend over the last 30 days
            - priceChangesCount30d: The number of price changes over the last 30 days.
            - priceRelativeTo30dRange: The current price relative to the 30-day range,(0 to 1).
            - minPrice90d: The minimum price of the variant over the last 90 days.
            - maxPrice90d: The maximum price of the variant over the last 90 days.
            - minPrice1y: The minimum price of the variant over the last year.
            - maxPrice1y: The maximum price of the variant over the last year.
            - minPriceAllTime: The minimum price of the variant since it was added to the database.
            - maxPriceAllTime: The maximum price of the variant since it was added to the database.
            - minPriceAllTimeDate: The date of the minimum price of the variant since it was added to the database in ISO 8601 date.
            - maxPriceAllTimeDate: The date of the maximum price of the variant since it was added to the database in ISO 8601 date.
        """
        results = justTCG.get_cards_by_query(
            tcgplayerId=tcgplayerId,
            cardId=cardId,
            variantId=variantId,
            condition=condition,
            game=game,
            set=set,
            order_by=order_by,
            order_direction=order_direction,
            limit=limit,
            offset=offset,
            search_query=search_query
        )
        
        if not results:
            logging.warning("No cards found for the given query.")
            return []
        else:
            return results
        
if __name__ == "__main__":
    
    mcp.run(transport='stdio')
    
    