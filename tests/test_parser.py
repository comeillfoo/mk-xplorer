#!/usr/bin/env python3
import unittest


from mk_xplorer.splitting_lines import eliminate_splitting_lines
from mk_xplorer.comments import eliminate_comments
from mk_xplorer.parser import MakefileParser


class TestSplittingLines(unittest.TestCase):
    def test_empty(self):
        self.assertEqual('', eliminate_splitting_lines('').strip())


    def test_single_split(self):
        expected = 'obj += a.o b.o c.o'
        makefile = 'obj += a.o b.o\\\nc.o'
        self.assertEqual(expected, eliminate_splitting_lines(makefile).strip())


class TestCommentsIgnore(unittest.TestCase):
    def test_empty(self):
        self.assertEqual('', eliminate_comments(''))


    def test_comment_entire_line(self):
        self.assertEqual('', eliminate_comments('# lorem ipsum'))


    def test_comment_postfix(self):
        expected = 'CC ?= clang '
        makefile = expected + '# default c compiler'
        self.assertEqual(expected, eliminate_comments(makefile))


class TestMakefile(unittest.TestCase):
    def test_simplest_explicit_rule(self):
        mk = MakefileParser('all: help; @echo "Hello, World!"\n').accept()
        self.assertIsNotNone(mk)
        self.assertTrue(mk.rules[0].is_default)
        self.assertEqual(['all'], mk.rules[0].targets.filenames)
        self.assertEqual(['help'], mk.rules[0].prerequisites.filenames)
        self.assertFalse(mk.rules[0].is_grouped)
        self.assertEqual('@echo "Hello, World!"', mk.rules[0].recipe)
