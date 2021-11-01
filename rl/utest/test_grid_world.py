"""Unit tests."""
import os
from os.path import join
import sys
import unittest
import logging
from pathlib import Path

utest_path = Path(__file__).resolve().parent
sys.path.append(str(utest_path / '../..'))

from rl import grid_world

class TestGridWorld(unittest.TestCase):
    """Unit tests."""

    def setUp(self):
        """Define data and setup environment."""
        logging.disable(logging.CRITICAL)  # disable logging at all levels

    def test_1(self):
        """Test."""
