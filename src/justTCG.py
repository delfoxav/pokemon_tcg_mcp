# Handling of price queries through JustTCG api.
import requests
import os
from typing import Union
import logging

API_KEY = os.getenv('JUSTTCG_API_KEY')

BASE_URL = 'https://api.justtcg.com/v1'


# API request helper with error handling
# copied from JustTCG documentation
def api_request(endpoint, method="GET", params=None, json_data=None):
    headers = {"X-API-Key": API_KEY}
    url = f"{BASE_URL}/{endpoint}"

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        else:  # POST
            response = requests.post(url, headers=headers, json=json_data)

        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        if hasattr(e, "response") and e.response:
            try:
                error_data = e.response.json()
                print(f"Error details: {error_data}")
            except:
                print(f"Error status code: {e.response.status_code}")
                print(f"Error text: {e.response.text}")
        return None
 
def get_list_of_games() -> list[dict]:
    """
    Returns a list of games available in JustTCG.

    Returns:
        list[dict]: A list of games with their details.
    """
    endpoint = "games"
    
    result = api_request(endpoint)
    
    if "data" in result:
        return result["data"]
    else:
        logging.error("Error fetching games: %s", result)
        return []
    


def get_list_of_sets(game: str) -> list[dict]:
    """
    Returns a list of sets for a specific game.
    Args:
        game (str): The name of the game to fetch sets for.
    Returns:
        list[dict]: A list of sets with their details.
    """
    endpoint = f"sets?game={game}"
    result = api_request(endpoint)
    if "data" in result:
        return result["data"]
    else:
        logging.error("Error fetching sets for game '%s': %s", game, result)
        return []


def get_cards_by_query(
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
                        search_query: str = None) -> list[dict]:
    """
    Returns a list of cards based on a query.
    Note: The tcgplayerId, cardId or variantId will take precedence over any search query if any of those are provided.
    
    Avoid using multiple identifiers in the same object.
    variantId will take precedence over tcgplayerId and tcgplayerId will take precedence over cardId.
    
    Args:
        tcgplayerId (str, optional): The TCGPlayer ID of the card.
        cardId (str, optional): The ID of the card.
        variantId (str, optional): The variant ID of the card.
        condition (str, optional): valid conditions are [Sealed, Near Mint, Lightly Played, Moderately Played, Heavily Played, Damaged] or abreviations [S, NM, LP, MP, HP, D].
        game (str, optional): The game ID to filter cards by (e.g., mtg, pokemon).
        set (str, optional): The set ID to filter cards by (e.g., Battle Pack: Epic Dawn).
        order_by (str, optional): The field to order the results by (e.g., name, price).
        order_direction (str, optional): The direction to order the results (asc or desc).
        limit (int, optional): The number of results to return per page. Default is 20.
        offset (int, optional): Number of results to skip. Default is 0.
        search_query (str, optional): A search query string to filter cards by name or other attributes.
    Returns:
        list[dict]: A list of cards matching the query.
    """
    
    # Build params dict using only non-None values
    params = { 
        k: v for k, v in [
            ("tcgplayerId", tcgplayerId),
            ("cardId", cardId),
            ("variantId", variantId),
            ("condition", condition),
            ("game", game),
            ("set", set),
            ("order_by", order_by),
            ("order_direction", order_direction),
            ("limit", limit),
            ("offset", offset),
            ("q", search_query)
        ] if v is not None
    }
    
    endpoint = "cards"
    result = api_request(endpoint, params=params)
    if "data" in result:
        return result["data"]
    else:
        logging.error("Error fetching cards: %s", result)
        return []

def build_card_query(tcgplayerId:str = None,
                     cardId:str = None,
                     variantId:str = None,
                     printingId:str = None,
                     condition:str = None) -> dict:
    """
    Builds a query dictionary for fetching cards from JustTCG.
    Only includes parameters that are not None.
    
    Args:
        tcgplayerId (str, optional): The TCGPlayer ID of the card priority over cardId.
        cardId (str, optional): The ID of the card.
        variantId (str, optional): The variant ID of the card priority over TCGPlayer ID.
        printingId (str, optional): The printing ID of the card.
        condition (str, optional): The condition of the card (e.g., NM for Near Mint).
        
    Returns:
        dict: A dictionary representing the card query.
    """
    
    return {k: v for k, v in [
        ("tcgplayerId", tcgplayerId),
        ("cardId", cardId),
        ("variantId", variantId),
        ("printingId", printingId),
        ("condition", condition)
    ] if v is not None}

def get_cards_by_batch_query(batch_query: list[dict]) -> list[dict]:
    """
    Fetches multiple cards based on a batch query.
    
    Args:
        batch_query (list[dict]): A list of dictionaries, each representing a card query.
        
    Returns:
        list[dict]: A list of cards matching the batch queries.
    """
    endpoint = "cards"

    result = api_request(endpoint, method="POST", json_data=batch_query)
    if "data" in result:
        return result["data"]
    else:
        logging.error("Error fetching cards: %s", result)
        return []

