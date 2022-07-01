"""
This file contains the suite of test for character creation, character
methods, character death, and character crafting."""

from evennia.utils.test_resources import LocalEvenniaTest
from typeclasses.characters import Character
from typeclasses.items import Item
from evennia.utils import create
from world.character_updater import update_encumberance

class TestCharacterCreation(LocalEvenniaTest):
    """ Instantiate a character and test to ensure the character has all
    required information attached to character at creation, such as ability
    scores, health, etc. """

    item_typeclass = Item

    def setUp(self):
        """ Sets up test environment. Inheriting the setup behavior
        from the parent class plus adding a few item types to attach
        traits to and test.
        """
        super().setUp()
        # create a few item objects to test traits on
        self.item1 = create.create_object(self.item_typeclass, key='Sword', \
                    location=self.room1, home=self.room1)
        self.item2 = create.create_object(self.item_typeclass, key='Stone', \
                    location=self.room2, home=self.room2)

    # tests for ability scores
    def test_if_character_has_dex_score(self):
        self.assertIsInstance(self.char1.ability_scores.Dex.actual, int)
        self.assertGreater(self.char1.ability_scores.Dex.actual, 0)

    def test_if_character_has_str_score(self):
        self.assertIsInstance(self.char1.ability_scores.Str.actual, int)
        self.assertGreater(self.char1.ability_scores.Str.actual, 0)

    def test_if_character_has_vit_score(self):
        self.assertIsInstance(self.char1.ability_scores.Vit.actual, int)
        self.assertGreater(self.char1.ability_scores.Vit.actual, 0)

    def test_if_character_has_per_score(self):
        self.assertIsInstance(self.char1.ability_scores.Per.actual, int)
        self.assertGreater(self.char1.ability_scores.Per.actual, 0)

    def test_if_character_has_cha_score(self):
        self.assertIsInstance(self.char1.ability_scores.Wil.actual, int)
        self.assertGreater(self.char1.ability_scores.Wil.actual, 0)

    # tests for status scores
    def test_if_character_hp_correct(self):
        self.assertIsInstance(self.char1.statuses.hp.actual, int)
        self.assertAlmostEqual(self.char1.statuses.hp.actual, \
            ((self.char1.ability_scores.Vit.current * 5) + \
            (self.char1.ability_scores.Wil.current * 2)))

    def test_if_character_sp_correct(self):
        self.assertIsInstance(self.char1.statuses.sp.actual, int)
        self.assertAlmostEqual(self.char1.statuses.sp.actual, \
            ((self.char1.ability_scores.Vit.current * 3) + \
            (self.char1.ability_scores.Str.current * 2) + \
            (self.char1.ability_scores.Dex.current)))
    
    def test_if_character_cp_correct(self):
        self.assertIsInstance(self.char1.statuses.cp.actual, int)
        self.assertAlmostEqual(self.char1.statuses.cp.actual, ((self.char1.ability_scores.Wil.current * 5) + \
            (self.char1.ability_scores.Vit)))

    def test_if_character_has_mass(self):
        self.assertIsInstance(self.char1.statuses.mass.actual, int)
        self.assertGreater(self.char1.statuses.mass.actual, 5)

    def test_if_character_has_height(self):
        self.assertIsInstance(self.char1.statuses.height.actual, int)
        self.assertGreater(self.char1.statuses.height.actual, 5)

    def test_if_character_has_encumberance(self):
        self.assertIsInstance(self.char1.statuses.enc.max, float)
        self.assertAlmostEqual(self.char1.statuses.enc.max, (self.char1.ability_scores.Str.current / 2.0))

    # tests for equipment slots
    def test_if_character_has_eq_slots(self):
        self.assertGreater(len(self.char1.db.eq_slots), 10)

    # test adding and removing a new skill to character
    def test_adding_and_removing_new_skill_to_character(self):
        self.char1.skills.add(key="ts", name="Test Skill", type="static", base=1)
        self.assertIsInstance(self.char1.skills.ts.current, int)
        self.char1.skills.remove('ts')
        self.assertEqual(self.char1.traits.__len__(), 0)

    # test if permanent info fields are present on character
    def test_if_info_contains_correct_fields(self):
        info_template = {'Target': None, 'Mercy': True, 'Default Attack': 'unarmed_strike', \
                        'In Combat': False, 'Position': 'standing', 'Sneaking' : False, \
                        'Wimpy': 100, 'Yield': 200, 'Title': None}
        self.assertEqual(self.char1.db.info.items(), info_template.items())

    def test_if_character_has_wallet(self):
        wallet_template = {'GC': 0, 'SC': 0, 'CC': 0}
        self.assertEqual(self.char1.db.wallet.items(), wallet_template.items())
        
    
    # test functions that recalculate status numbers important for interactions (ex. encumberance)
    def test_recalculating_encumberance(self):
        self.char1.execute_cmd("get Sword")
        update_encumberance(self.char1)
        self.assertAlmostEqual(self.char1.statuses.enc.current, self.item1.mass)
        self.assertAlmostEqual(self.char1.statuses.mass.mod, self.item1.mass)
