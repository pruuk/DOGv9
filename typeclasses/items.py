"""
Generic items, item subclasses, & base functions for items.
"""

from typeclasses.objects import Object
from world.traits import TraitHandler
from evennia.utils.logger import log_file
from evennia.utils import lazy_property

class Item(Object):
    """
    Typeclass for Items.
    Attributes:
        value (int): monetary value of the item in CC
        weight (float): weight of the item
    """
    value = 1 # default value in copper coins
    mass = 0.5 # default mass in kilograms

    @lazy_property
    def traits(self):
        """TraitHandler that manages room traits."""
        return TraitHandler(self)

    def at_object_creation(self):
        "Only called at creation and forced update"
        super(Item, self).at_object_creation()
        self.locks.add(";".join(("puppet:perm(Builder)",
                                 "equip:false()",
                                 "get:all()"
                                 )))
