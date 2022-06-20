"""
File for testing all functions of the traits module and Trailhandler
"""

from evennia.utils.test_resources import LocalEvenniaTest
from typeclasses.items import Item
from evennia.utils import create


class TestTraitFunctions(LocalEvenniaTest):
    """ test each of the functions of the trait module.  We're using
    LocalEvenniaTest because it uses the local version of typeclass objects
    and commands plus it's default setUp function creates a small test
    environment with objects we can attach traits to.
    """
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
        # add traits to objects to test methods on
        self.char1.traits.add(key='TT', name='Test Trait', type='static', \
                            base=100, extra={'learn' : 0})
        self.item2.traits.add(key='TT2', name= 'Test Trait 2', type= 'counter', \
                            min=0, max=100, extra={'learn' : 0})
        self.char1.traits.add(key="hp", name="Health Points", type="gauge", \
                        base=100, extra={'learn' : 0})

    def test_static_trait_creation_on_character(self):
        """Check to make sure we can initialize a trait on char1."""
        self.assertEqual(self.char1.traits.TT.actual, 100)

    def test_counter_trait_creation_on_stone(self):
        """ Check to make sure counter type trait initializes. """
        self.assertEqual(self.item2.traits.TT2.current, 0)

    def test_gauge_trait_creation_on_character(self):
        """ Check to initialize a gauge trait. """
        self.assertEqual(self.char1.traits.hp.max, 100)

    def test_len_method_of_traithandler(self):
        """ Check how many traits are on char2."""
        self.assertEqual(self.char1.traits.__len__(), 2)

    def test_remove_trait(self):
        """ Test removal of trait. Note: this affects the parent of the Traits
        object rather than being called on an individual trait"""
        self.char1.traits.remove('TT')
        self.assertEqual(self.char1.traits.__len__(), 1)
        self.char1.traits.add(key='TT', name='Test Trait', type='static', \
                            base=100, extra={'learn' : 0})
        self.assertEqual(self.char1.traits.__len__(), 2)

    def test_clear(self):
        """ Test removal of all traits from a parent object. """
        self.char2.traits.add(key='TT3', name='Test trait 3', type='static', \
                            base=100)
        self.assertEqual(self.char2.traits.__len__(), 1)
        self.char2.traits.clear()
        self.assertEqual(self.char2.traits.__len__(), 0)

    def test_all(self):
        """ Test all function for traits. Should return list of traits on
        parent. Not that all is not a callable function/method. You do not use ()
        with the all method here."""
        self.assertIsInstance(self.item2.traits.all, list)
        self.assertIn('TT2', self.item2.traits.all)


    def test_all_dict(self):
        """ Test the all_dict method in TraitHandler. """
        self.assertIsInstance(self.char1.traits.all_dict, dict)
        self.assertIn('hp', self.char1.traits.all_dict.keys())


    def test_mod(self):
        """ Tests modification of an individual trait. """
        self.item2.traits.TT2.mod += 5
        self.assertEqual(self.item2.traits.TT2.actual, 5)

    def test_reset_mod(self):
        """ Tests resetting modifier on a trait."""
        self.item2.traits.TT2.mod += 5
        self.assertEqual(self.item2.traits.TT2.actual, 5)
        self.item2.traits.TT2.reset_mod()
        self.assertEqual(self.item2.traits.TT2.actual, 0)

    def test_reset_counter(self):
        """ Test the reset counter method on Traithandler."""
        self.item2.traits.TT2.current += 5
        self.assertEqual(self.item2.traits.TT2.actual, 5)
        self.item2.traits.TT2.reset_counter()
        self.assertEqual(self.item2.traits.TT2.actual, 0)

    def test_fill_gauge(self):
        """ Test fill gauge method on gauge type trait."""
        self.char1.traits.hp.current -= 50
        self.assertEqual(self.char1.traits.hp.current, 50)
        self.char1.traits.hp.fill_gauge()
        self.assertEqual(self.char1.traits.hp.current, 100)

    def test_percent(self):
        """ Test percent method on gauge trait. """
        self.assertEqual(self.char1.traits.hp.percent(), '100.0%')

    def test_percent_bar(self):
        """ Test the percent bar method for a gauge trait. """
        self.assertEqual(self.char1.traits.hp.percent_bar(), '[|g░░░░░▒▒▒▒▒▓▓▓▓▓▓▓|n]')
        self.char1.traits.hp.current -= 100
        self.assertEqual(self.char1.traits.hp.percent_bar(), '[|R                 |n]')
        self.char1.traits.hp.fill_gauge()
