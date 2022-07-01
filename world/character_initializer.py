"""
This file contains the functions to initialize a new character or reset
a character to the base attributes. This has been moved off of the character
class in order to reduce the clutter on the character class.
"""

from world.traits import TraitHandler
from world.roller import BaseRoller, BonusRoller, RollerController


def initialize_character(character):
    """ Pass in a character. Character will be populated with the initial set
    of ability scores, attributes, talents, & skills. """
    # set up RollerController
    ability_roller = RollerController()

    # initialze ability scores
    character.ability_scores.clear()
    ability_scores = {'Dex': 'Dexterity', 'Str': 'Strength', 'Per': 'Perception', \
                        'Vit': 'Vitality', 'Wil': "Willpower"}
    # character.ability_scores.clear()
    for abbrev, full_name in ability_scores.items():
        ability_roller.reset_total()
        ability_roller.add_base(100)
        character.ability_scores.add(key=abbrev, name=full_name, type='static', \
                            base=ability_roller.total, extra={'learn' : 0})

    # Set status gauges for health, stamina, conviction
    character.statuses.clear()
    character.statuses.add(key="hp", name="Health Points", type="gauge", \
                        base=((character.ability_scores.Vit.current * 5) + \
                        (character.ability_scores.Wil.current * 2)), extra={'learn' : 0})
    character.statuses.add(key="sp", name="Stamina Points", type="gauge", \
                    base=((character.ability_scores.Vit.current * 3) + \
                    (character.ability_scores.Str.current * 2)+ \
                    (character.ability_scores.Dex.current)), extra={'learn' : 0})
    character.statuses.add(key="cp", name="Conviction Points", type="gauge", \
                        base=((character.ability_scores.Wil.current * 5) + \
                        (character.ability_scores.Vit.current)), extra={'learn' : 0})

    # Set status for height, mass, encumberance
    ability_roller.reset_total()
    ability_roller.add_base(75) # average mass in kilograms
    character.statuses.add(key="mass", name="Mass", type="static", \
                        base=ability_roller.total)
    ability_roller.reset_total()
    ability_roller.add_base(175) # average height in centimeters
    character.statuses.add(key="height", name="Height", type="static", \
                        base=ability_roller.total)
    # Encumberance measures a character's carrying capacity. Some items
    # may be lighter or heavier in emcumberance than their mass would suggest
    # because they are easier to carry or are inside a container
    character.statuses.add(key="enc", name="Encumberance", type="counter", \
                        max=character.ability_scores.Str.current / 2.0)

    # Initialize character equipment slots
    character.db.eq_slots = {
        'head': None,
        'face': None,
        'ears': None,
        'neck': None,
        'chest': None,
        'back': None,
        'waist': None,
        'quiver': None,
        'shoulders': None,
        'arms': None,
        'hands': None,
        'legs': None,
        'feet': None,
        'primary hand': None,
        'secondary hand': None
    }

    # Add in info fields needed to track changeable info about character like who they are targeting
    character.db.info = {'Target': None, 'Mercy': True, 'Default Attack': 'unarmed_strike', \
                        'In Combat': False, 'Position': 'standing', 'Sneaking' : False, \
                        'Wimpy': 100, 'Yield': 200, 'Title': None}

    # Add in a character wallet for storing coins
    character.db.wallet = {'GC': 0, 'SC': 0, 'CC': 0}
