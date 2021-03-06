import unittest
from game.common.disasters import *


class TestDisasterObjects(unittest.TestCase):

    # General Disaster Testing

    # Lasting Disaster Testing

    # Earthquake Object Testing

    def test_init_earthquake(self):
        my_earthquake = Earthquake()
        self.assertIsInstance(my_earthquake, Earthquake)
        self.assertNotIsInstance(my_earthquake, LastingDisaster)
        self.assertIsInstance(my_earthquake, Disaster)

    # Fire Object Testing

    def test_init_fire(self):
        my_fire = Fire()
        self.assertIsInstance(my_fire, Fire)
        self.assertIsInstance(my_fire, LastingDisaster)
        self.assertIsInstance(my_fire, Disaster)

    # Blizzard Object Testing

    def test_init_blizzard(self):
        my_blizzard = Blizzard()
        self.assertIsInstance(my_blizzard, Blizzard)
        self.assertIsInstance(my_blizzard, LastingDisaster)
        self.assertIsInstance(my_blizzard, Disaster)

    # Monster Object Testing

    def test_init_monster(self):
        my_monster = Monster()
        self.assertIsInstance(my_monster, Monster)
        self.assertIsInstance(my_monster, LastingDisaster)
        self.assertIsInstance(my_monster, Disaster)

    #  Tornado Object Testing

    def test_init_tornado(self):
        my_tornado = Tornado()
        self.assertIsInstance(my_tornado, Tornado)
        self.assertNotIsInstance(my_tornado, LastingDisaster)
        self.assertIsInstance(my_tornado, Disaster)

    # UFO Object Testing

    def test_init_ufo(self):
        my_ufo = Ufo()
        self.assertIsInstance(my_ufo, Ufo)
        self.assertNotIsInstance(my_ufo, LastingDisaster)
        self.assertIsInstance(my_ufo, Disaster)

if __name__ == '__main__':
    unittest.main()
