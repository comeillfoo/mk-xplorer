#!/usr/bin/env python3
import unittest


from mk_xplorer.parser import MakefileParser


class TestSplittingLines(unittest.TestCase):
    def test_empty(self):
        parser = MakefileParser.from_makefile('')


    def test_single_split(self):
        pass
