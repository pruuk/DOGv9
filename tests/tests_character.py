"""
This file contains the suite of test for character creation, character
methods, character death, and character crafting."""

from evennia.utils.test_resources import LocalEvenniaTest
from typeclasses.characters import Character
import unittest

class TestCharacterCreation(LocalEvenniaTest):
    """ Instantiate a character and test to ensure the character has all
    required information attached to character at creation, such as ability
    scores, health, etc. """

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