"""
UnitTests for Bloglang.Helpers.Utils
"""

import unittest
import Helpers.Utils as Utils

class UtilsTests(unittest.TestCase):
    """
    tests for Helpers.Utils
    """

    def runTest(self):
        """
        tests for Utils.joinit
        """
        self.assertEqual(list(Utils.joinit([], 3)), [])
        self.assertEqual(list(Utils.joinit([1], 3)), [1])
        self.assertEqual(list(Utils.joinit(['a', 'b', 'c', 'd'], 3)), ['a', 3, 'b', 3, 'c', 3, 'd'])
