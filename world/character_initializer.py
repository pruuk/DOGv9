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
