"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter
from world.traits import TraitHandler
from world.character_initializer import initialize_character
from world.character_updater import update_encumberance
from evennia.utils import lazy_property
from evennia.utils.logger import log_file


class Character(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """

    # pull in handlers for traits, equipment, mutations, talents
    @lazy_property
    def traits(self):
        """TraitHandler that manages character traits."""
        return TraitHandler(self)

    @lazy_property
    def ability_scores(self):
        """TraitHandler that manages character ability scores."""
        return TraitHandler(self, db_attribute='ability_scores')

    @lazy_property
    def statuses(self):
        """TraitHandler that manages character statuses."""
        return TraitHandler(self, db_attribute='statuses')

    @lazy_property
    def skills(self):
        """TraitHandler that manages character skills."""
        return TraitHandler(self, db_attribute='skills')

    def at_object_creation(self):
        "Called only at object creation and with update command."
        # call initialize_character
        initialize_character(self)

    def at_get(self):
        "Called when this object gets another object"
        log_file(f"{self.name} picked up something.", filename="item_moves.log")
        update_encumberance(self)

    def at_drop(self):
        "Called when this object drops an object"
        log_file(f"{self.name} dropped something.", filename="item_moves.log")
        update_encumberance(self)
