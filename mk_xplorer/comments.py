#!/usr/bin/env python3
import re


comment_recipe = re.compile(r'(.*)(\#.*)$')

def eliminate_single_comment(mk_line: str) -> str:
    return re.sub(comment_recipe, r'\1', mk_line)


def eliminate_comments(makefile: str) -> str:
    return '\n'.join(map(eliminate_single_comment, makefile.split('\n')))
