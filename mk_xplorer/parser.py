#!/usr/bin/env python3
import re
import io


from typing import Self


from mk_xplorer.lexer import MakefileLexer
from mk_xplorer.makefile import SpecialTargets, Makefile


class MakefileParser:
    def __init__(self, stream: io.TextIOBase):
        self._stream = stream
        self._targets = {}
        self._in_recipe = False
        self._recipeprefix = '\t'


    @staticmethod
    def condense(line: str, conform_posix_2: bool = False) -> str:
        condensed = line.rstrip().removesuffix('\\')
        return (condensed if conform_posix_2 else condensed.rstrip()) + ' '


    def read_full_logical_line(self) -> str:
        conform_posix_2 = SpecialTargets.POSIX in self._targets
        is_previous_splitted = False
        lline = io.StringIO(newline=None)

        while True:
            line = self._stream.readline()
            if is_previous_splitted and not conform_posix_2:
                line = line.lstrip()

            is_splitted = self.BACKSLASH_NEWLINE_RGX.match(line) is not None
            if not is_splitted:
                lline.write(line)
                break
            lline.write(self.condense(line, conform_posix_2))
            is_previous_splitted = is_splitted
        return lline.getvalue()


    def parse(self) -> Makefile:
        while True:
            lline = self._stream.readline()
            if not lline:
                break
            lexer = MakefileLexer()
            lexer.build()
            tokens = lexer.tokenize(lline)


    @classmethod
    def from_makefile(cls, makefile: str) -> Self:
        return cls(io.StringIO(makefile, None))


    @classmethod
    def load(cls, stream: io.TextIOBase) -> Makefile:
        parser = cls(stream)
        return parser.parse()


    @classmethod
    def loads(cls, makefile: str) -> Makefile:
        parser = cls.from_makefile(makefile)
        return parser.parse()
