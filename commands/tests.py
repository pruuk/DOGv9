# test building tutorial using in-game testing mechanism

import unittest

class TestString(unittest.TestCase):
    """ Unit test for strings, basic example."""

    def test_upper(self):
        """Test the upper string method"""
        self.assertEqual('foo'.upper(), 'FOO')
