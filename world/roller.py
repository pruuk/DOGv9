# Module for rolling. Used to resolve any random action
import numpy as np
import random
from evennia import logger
from evennia.utils.logger import log_file

class BaseRoller:
    """ Object used to output random numbers that roughly follow the shape
    of a normal distribution aka bell curve. This is intended to be the base
    roll for most ability score rolls and interactions in the game, usually
    with an input of 100."""

    def __init__(self):
        self.total = 0

    def roll(self, number):
        """ Return a number from a normal distribution."""
        self.total = int(np.random.default_rng().normal(loc=number, scale=number/10))

class BonusRoller:
    """ Object used to output random numbers that are less regular that the
    normal distribution. Used for bonus rolls to be added to a base roll or
    used to resolve actions for very random events. """

    def __init__(self):
        self.total = 0

    def roll_one_die(self, number):
        """ Rolls a die with a number of sides equal to the input number. In the
        event of a maximum roll, the die is rerolled and added to the totel.
        Rerolls can only happen up to 5 times for a given die. """
        roll_count = 5
        while roll_count > 0:
            roll = random.randint(1, number)
            self.total += roll
            if roll == number:
                roll_count -= 1
            else:
                roll_count = 0


    def roll(self, dice_dictionary):
        """ rolls bonus by calling roll_one_die a given number of times.
        Dice list must be formatted as a dictionay of values where the key
        is the sides of the dice and the value is number of dice of that
        size to roll."""

        for number_of_sides, number_of_dice in dice_dictionary.items():
            for i in range(number_of_dice):
                self.roll_one_die(number_of_sides)


class RollerController:
    """ Object used to roll for most interactions. Can include a base roll and
    a bonus roll. """

    def __init__(self):
        self.total = 0

    def add_base(self, base_number):
        """ Adds a base roll to the total for the controller. """
        base = BaseRoller()
        base.roll(base_number)
        self.total += base.total

    def add_bonus(self, bonus_dict):
        """ Adds bonus dice to RollerController total. """
        bonus = BonusRoller()
        bonus.roll(bonus_dict)
        self.total += bonus.total

    def modify_total(self, number):
        """ Modifies the total directly by a given amount. A negaitive number
        can be passed in. """
        self.total += number
        if self.total < 0:
            self.total = 0

    def reset_total(self):
        """ Resets total to zero. """
        self.total = 0
