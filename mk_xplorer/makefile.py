#!/usr/bin/env python3
from dataclasses import dataclass, field


RECIPE_PREFIX = '\t'


@dataclass
class Variable:
    name: str
    operator: str
    value: str = ''


@dataclass
class Filenames:
    filenames: list[str]


    @classmethod
    def from_filenames(cls, filenames: str):
        return cls(filenames.strip().split(' '))


    def __str__(self) -> str:
        return ' '.join(self.filenames)


@dataclass
class Rule:
    targets: Filenames
    prerequisites: Filenames
    is_default: bool = False
    is_grouped: bool = False # targets grouped or independent
    recipe: list[str] = field(default_factory=list)


    def __str__(self) -> str:
        return str(self.targets) \
            + ' ' + ('&:' if self.is_grouped else ':') \
            + ' ' + str(self.prerequisites) + '\n' \
            + '\n'.join(map(lambda s: RECIPE_PREFIX + s, self.recipe))


class Makefile:
    def __init__(self):
        self.rules: list[Rule] = []
        self.variables = {}
