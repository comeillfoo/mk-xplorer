#!/usr/bin/env python3
import unittest


from typing import Generator, Any


from mk_xplorer.lexer import MakefileLexer


class TestTokenizer(unittest.TestCase):
    def _tokenize(self, stream: str) -> Generator[Any, None, None]:
        lexer = MakefileLexer()
        lexer.build()
        yield from lexer.tokenize(stream)


    def test_empty(self):
        actual = list(self._tokenize(''))
        self.assertFalse(actual)


    def test_skip_comments(self):
        with self.subTest('no other tokens at all'):
            actual = list(self._tokenize('# lorem ipsum'))
            self.assertFalse(actual)

        with self.subTest('no other tokens at the same line'):
            actual = list(self._tokenize('# lorem ipsum\ndefine'))
            self.assertEqual(2, len(actual))
            self.assertEqual('NEWLINES', actual[0].type)
            self.assertEqual('DEFINE', actual[1].type)

        with self.subTest('other tokens prepended comment'):
            actual = list(self._tokenize('include # lorem ipsum'))
            self.assertEqual(2, len(actual))
            self.assertEqual('INCLUDE', actual[0].type)
            self.assertEqual('SPACES', actual[1].type)


    def test_tokenizing_splitted_long_lines(self):
        with self.subTest('just split'):
            actual = list(self._tokenize('\\\n'))
            self.assertEqual(1, len(actual))
            self.assertEqual('ESCSEQ', actual[0].type)
            self.assertEqual('\\\n', actual[0].value)

        with self.subTest('extra backslash'):
            actual = list(self._tokenize('\\\\\n'))
            self.assertEqual(2, len(actual))
            self.assertEqual('ESCSEQ', actual[0].type)
            self.assertEqual('\\\\', actual[0].value)
            self.assertEqual('NEWLINES', actual[1].type)
