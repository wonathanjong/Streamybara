import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "resources", "lib"))

from modules import validation


class TestValidation(unittest.TestCase):
    def test_verify_provider(self):
        self.assertTrue(validation.verify_provider("abcdEFGH12345678"))
        self.assertFalse(validation.verify_provider("bad"))
        self.assertFalse(validation.verify_provider(""))

    def test_verify_trakt(self):
        self.assertTrue(validation.verify_trakt("deadBEEF00"))
        self.assertFalse(validation.verify_trakt("123"))
        self.assertFalse(validation.verify_trakt(""))


if __name__ == "__main__":
    unittest.main()
