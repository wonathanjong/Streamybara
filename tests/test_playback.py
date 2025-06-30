import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "resources", "lib"))

from modules import playback


class TestSelectPreferredSource(unittest.TestCase):
    def setUp(self):
        self.sources = [
            {"quality": 720, "size": 2},
            {"quality": 720, "size": 1},
            {"quality": 1080, "size": 3},
            {"quality": 1080, "size": 1},
            {"quality": 2160, "size": 5},
            {"quality": 2160, "size": 4},
        ]

    def test_highest_quality(self):
        chosen = playback.select_preferred_source(self.sources, 0)
        self.assertEqual(chosen["quality"], 2160)

    def test_high_quality_lowest_size(self):
        chosen = playback.select_preferred_source(self.sources, 1)
        self.assertEqual(chosen["quality"], 2160)
        self.assertEqual(chosen["size"], 4)

    def test_medium_quality_largest_size(self):
        chosen = playback.select_preferred_source(self.sources, 2)
        self.assertEqual(chosen["quality"], 1080)
        self.assertEqual(chosen["size"], 3)

    def test_low_quality_smallest_size(self):
        chosen = playback.select_preferred_source(self.sources, 3)
        self.assertEqual(chosen["quality"], 720)
        self.assertEqual(chosen["size"], 1)


if __name__ == "__main__":
    unittest.main()
