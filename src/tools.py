from tcgdexsdk import TCGdex
from tcgdexsdk import Card, Set, Serie, SerieResume, SetResume, CardResume

from tcgdexsdk.models.subs import CardAttack, CardAbility, Legal




def Serie_to_dict(serie: Serie, image_quality: str = "low", image_type: str = "png") -> dict:
    """ Converts a Serie object to a dictionary. """
    return {
        'id': serie.id,
        'name': serie.name,
        'logo': serie.logo + "/" + image_quality + "." + image_type if serie.logo else None,
        'sets': [SetResume_to_dict(s, image_quality, image_type) for s in serie.sets] if serie.sets else None,
    }

def Set_to_dict(set: Set, image_quality: str = "low", image_type: str = "png") -> dict:
    """ Converts a Set object to a dictionary. """
    
    return {
        'id': set.id,
        'name': set.name,
        'logo': set.logo + "/" + image_quality + "." + image_type if set.logo else None,
        'symbol': set.symbol +"/" + image_quality + "." + image_type if set.symbol else None,
        'cardCount': {"total":set.cardCount.total, "official":set.cardCount.official},
        'tcgOnline': set.tcgOnline,
        'releaseDate': set.releaseDate,
        'legalities': Legal_to_str(set.legalities),
        'cards': [CardResume_to_dict(card) for card in set.cards] if set.cards else None,
    }

def CardResume_to_dict(card_resume: CardResume, image_quality: str = "low", image_type: str = "png") -> dict:
    """ Converts a CardResume object to a dictionary. """
    return {
        'id': card_resume.id,
        'localId': card_resume.localId,
        'name': card_resume.name,
        'image': card_resume.image +"/" + image_quality + "." + image_type if card_resume.image else None,
    }

def SetResume_to_dict(set_resume: SetResume, image_quality: str = "low", image_type: str = "png") -> dict:
    """ Converts a SetResume object to a dictionary. """
    return {
        'id': set_resume.id,
        'name': set_resume.name,
        'logo': set_resume.logo + "/" + image_quality + "." + image_type if set_resume.logo else None,
        'symbol': set_resume.symbol +"/" + image_quality + "." + image_type if set_resume.symbol else None,
        'cardCount': {"total":set_resume.cardCount.total, "official":set_resume.cardCount.official},
    }

def SerieResume_to_dict(serie_resume: SerieResume) -> dict:
    """ Converts a SerieResume object to a dictionary. """
    
    return {
        'id': serie_resume.id,
        'name': serie_resume.name,
        'logo': serie_resume.logo,
    }

def CardAttack_to_dict(attack: CardAttack) -> dict:
    """ Converts an Attack object to a dictionary. """
    return {
        'cost': attack.cost,
        'name': attack.name,
        'damage': attack.damage if attack.damage else None,
        'effect': attack.effect if attack.effect else None,
    }

def CardAbility_to_dict(ability: CardAbility) -> dict:
    """ Converts an Ability object to a dictionary. """
    return {
        'type': ability.type,
        'name': ability.name,
        'effect': ability.effect,
    }

def Legal_to_str(legal: Legal) -> str:
    """ Converts a Legal object to a string. """
    potential_legal = legal.__dict__
    # filter out the False values
    legal_list = [k for k, v in potential_legal.items() if v is not False]
    return ", ".join(legal_list) if legal_list else None

def Card_to_dict(card: Card, image_quality: str = "low", image_type: str = "png") -> dict:
    """ Converts a Card object to a dictionary. """
    potential_variants = card.variants.__dict__
    # filter out the False values
    variants = [k for k, v in potential_variants.items() if v is not False]
    
    
    
    output = {
        'illustrator': card.illustrator,
        'rarity': card.rarity,
        'category': card.category,
        "variants" : variants,
        "set": SetResume_to_dict(card.set),
        "hp": card.hp,
        "types":", ".join(card.types) if card.types else None,
        "evolvesFrom": card.evolvesFrom if card.evolvesFrom else None,
        "description": card.description if card.description else None,
        "level": card.level if card.level else None,
        "stage": card.stage if card.stage else None,
        "suffix": card.suffix if card.suffix else None,
        "item": card.item if card.item else None,
        "abilities": [CardAbility_to_dict(ability) for ability in card.abilities] if card.abilities else None,
        "attacks" : [CardAttack_to_dict(attack) for attack in card.attacks] if card.attacks else None,
        "resistances":  card.resistances if card.resistances else None,
        "retreat": card.retreat,
        "effect": card.effect if card.effect else None,
        "trainerType": card.trainerType if card.trainerType else None,
        "energyType": card.energyType if card.energyType else None,
        "regulationMark": card.regulationMark,
        "legal": Legal_to_str(card.legal),
        "id": card.id,
        "localId": card.localId,
        "name": card.name,
        "image": card.image +"/" + image_quality + "." + image_type if card.image else None,
        "boosters": card.boosters if card.boosters else None}
    
    # return only the fields that are not None
    return {k: v for k, v in output.items() if v is not None}