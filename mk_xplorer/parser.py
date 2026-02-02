#!/usr/bin/env python3
import re
import io


from typing import Self


from mk_xplorer.makefile import SpecialTargets, Makefile


class MakefileParser:
    BACKSLASH_NEWLINE_RGX = re.compile(r'([^\\\n]|\\u[A-Fa-f0-9]{4}|\\U[A-Fa-f0-9]{8}|\\.)*\\$')
    COMMENT_RGX = re.compile(r'^([^\\\n]*)(\#.*)$')


    def __init__(self, stream: io.TextIOBase):
        self._stream = stream
        self._targets = {}
        self._in_recipe = False


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


    def remove_comment(self, line: str) -> str:
        if self._in_recipe:
            return line

        _match = self.COMMENT_RGX.match(line)
        if _match is None:
            return line
        return _match.group(1)


    def parse(self) -> Makefile:
        while self._stream.readable():
            lline = self.remove_comment(self.read_full_logical_line())
            if not lline:
                continue


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
