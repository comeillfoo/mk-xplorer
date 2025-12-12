#!/usr/bin/env python3
from abc import ABC
from enum import Flag, auto

class ParserContext(ABC):
    pass

class StrParserContext(ParserContext):
    def __init__(self, string: str):
        self.string = string

class IntParserContext(ParserContext):
    def __init__(self, integer: int):
        self.integer = integer


class BaseParserContext(ParserContext):
    pass

class RuleParserContext(IntParserContext):
    pass

class VariableParserContext(StrParserContext):
    pass


class ParserContexts(Flag):
    BASE_CTX = auto()
    RULE_CTX = auto()
    VARIABLE_CTX = auto()
