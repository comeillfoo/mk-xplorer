#!/usr/bin/env python3
import re
from typing import Optional, TypeVar, Callable

ListElement = TypeVar('ListElement')

split_start_recipe = re.compile(r'^(?!(\t+))(.*)(?<!\\)\\\n')


def make_get_or_default(lst: list[ListElement]) -> Callable[[int, Optional[ListElement]], Optional[ListElement]]:
    def get_or_default(i: int, default: Optional[ListElement]) -> Optional[ListElement]:
        try:
            return lst[i]
        except IndexError:
            return default
    return get_or_default



def eliminate_splitting_lines(makefile: str) -> str:
    makefile = list(map(lambda s: s + '\n', makefile.split('\n')))
    mk_getter = make_get_or_default(makefile)
    # work with lines separately is easier
    i = 0
    while i < len(makefile):
        m = split_start_recipe.match(makefile[i])
        if not m:
            i += 1
            continue
        next_line = mk_getter(i + 1, '').lstrip()
        makefile[i] = re.sub(split_start_recipe, r'\2 ', makefile[i]) + next_line
        makefile.pop(i + 1)

    return ''.join(makefile)


