#!/usr/bin/env python3
import unittest


from typing import Generator, Any


from mk_xplorer.lexer import lexer


class TestTokenizer(unittest.TestCase):
    def _tokenize(self, stream: str) -> Generator[Any, None, None]:
        lexer.input(stream)
        while True:
            tok = lexer.token()
            if not tok:
                break
            yield tok


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
            self.assertEqual('NEWLINE', actual[0].type)
            self.assertEqual('DEFINE', actual[1].type)

        with self.subTest('other tokens prepended comment'):
            actual = list(self._tokenize('include # lorem ipsum'))
            self.assertEqual(2, len(actual))
            self.assertEqual('INCLUDE', actual[0].type)
            self.assertEqual('SPACE', actual[1].type)
