# tests for functions & classes built in world directory

import unittest
from world.roller import BaseRoller, BonusRoller, RollerController

class TestBaseRoller(unittest.TestCase):
    """ Unit test for base rolling class that produces output that roughly
        follows a bell curve with a median at the integer passed into the
        class. """

    @classmethod
    def setUp(self):
        """ Set up the curve tests. Instantiate a BaseRoller obj."""
        # create roller object
        self.roll_curve = BaseRoller()
        self.roll_curve.roll(100)

    def test_roll_normal_distribution(self):
        """ test the base roller with input of 100. Ensure output is an
        integer between 0 & 1000."""
        self.assertIsInstance(self.roll_curve.total, int)
        self.assertLess(self.roll_curve.total, 1000)
        self.assertGreater(self.roll_curve.total, 0)

    @classmethod
    def tearDownClass(self):
        """ Remove object. Clean up."""
        del self.roll_curve

class TestBonusRoller(unittest.TestCase):
    """ Unit test for bonus roller. Bonus rolls are usually added to the base
    roll to produce the final roll. A character/item/place's mystique determines
    the strength of the bonus roll. """

    @classmethod
    def setUp(self):
        """ Set up the curve tests. Instantiate a BonusRoller obj."""
        # create roller object
        self.roll_bonus = BonusRoller()
        self.roll_bonus.roll({6 : 2, 8 : 3})

    def test_roll_bonus(self):
        """ test the bonus roller with input of 2d6. Ensure output is an
        integer between 2 & 100."""
        self.assertIsInstance(self.roll_bonus.total, int)
        self.assertLess(self.roll_bonus.total, 300)
        self.assertGreater(self.roll_bonus.total, 5)

    @classmethod
    def tearDownClass(self):
        """ Remove object. Clean up."""
        del self.roll_bonus


class TestInteractionRoll(unittest.TestCase):
    """ Unit test for testing a normal interaction roll (for example: a
    a character tries to hit an NPC with a strike). This interaction roll would
    include a combined base & bonus roll by the attacker and the defender using
    numbers derived from the skill and natural abilities of each for attack &
    defense. """

    @classmethod
    def setUp(self):
        """ Set up test rolls for attacker and defender. """
        # we'll fudge in skills & abilities for now.
        # TODO: Replace fudged in numbers w/ actual character & NPC objects
        attacker_attack_base = 105
        attacker_bonus_dict = {6 : 3, 10 : 1}
        defender_defend_base = 100
        defender_bonus_dict = {4: 2, 6 : 4}
        # set up rolls
        self.att_roll = RollerController()
        self.att_roll.add_base(attacker_attack_base)
        self.att_roll.add_bonus(attacker_bonus_dict)
        self.def_roll = RollerController()
        self.def_roll.add_base(defender_defend_base)
        self.def_roll.add_bonus(defender_bonus_dict)

    def test_att_roll(self):
        """ Checks to make sure attack roll properly formed. """
        self.assertIsInstance(self.att_roll.total, int)
        self.assertGreater(self.att_roll.total, 5)

    def test_def_roll(self):
        """ Checks to make sure defense roll properly formed. """
        self.assertIsInstance(self.def_roll.total, int)
        self.assertGreater(self.def_roll.total, 5)

    def test_modify_att_roll_below_zero(self):
        """ Ensure we never return below zero after direct modification of
        total. """
        self.att_roll.modify_total(-10000)
        self.assertEqual(self.att_roll.total, 0)

    def test_reset_of_att_roll(self):
        """ Check that reset sets total to zero. """
        self.att_roll.reset_total()
        self.assertEqual(self.att_roll.total, 0)
