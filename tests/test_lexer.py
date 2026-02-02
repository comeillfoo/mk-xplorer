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
