# File contains the functions necessary to update info about the character such as encumberance,
# combat modifiers, etc

from evennia.utils.logger import log_file

def update_encumberance(character):
    """
    This function will calculate how encumbered the object is based upon
    carried weight and their strength. Encumberance will affect how much
    stamina it costs to move, fight, etc...
    Equipped items will not count against encumberance as much as 'loose'
    items in inventory. Certain containers and bags will also reduce
    encmberance.
    """
    log_file(f"Updating encumberance for {character}", filename='char_updates.log')
    character.statuses.enc.current = 0
    for item in character.contents:
        log_file(f"Updating {character} enc for {item}, mass: {item.mass}", filename='char_updates.log')
        if item in character.db.eq_slots.values():
            character.statuses.enc.current += item.mass * .5
        else:
            character.statuses.enc.current += item.mass
    # add modifier to base character mass to reflect character carried items
    character.statuses.mass.mod = 0
    for item in character.contents:
        character.statuses.mass.mod += item.mass
