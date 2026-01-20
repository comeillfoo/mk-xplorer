#!/usr/bin/env python3
import re


from abc import ABC
from typing import Optional
from dataclasses import dataclass


from mk_xplorer.makefile import (
    Filenames, Variable, Rule, Makefile, RECIPE_PREFIX
)


FILENAME_RGX = '[a-zA-Z0-9](?:[a-zA-Z0-9 ._-]*[a-zA-Z0-9])?\.[a-zA-Z0-9_-]+'
TARGETS_PREREQS_RGX = f'({FILENAME_RGX} )*({FILENAME_RGX})'
RECIPE_RGX = re.compile(f'(?P<targets>{TARGETS_PREREQS_RGX})(?P<grouped>\&)?: *(?P<prereqs>{TARGETS_PREREQS_RGX}) *(?P<recipe>;.*)?')
INLINE_VAR_RGX = re.compile(r'(?P<varname>\w+) *(?P<op>(\?|:{1,3}|\+|\!)?=) *(?P<varvalue>.*)')
DIRECTIVE_VAR_RGX = re.compile(r'define +(?P<varname>\w+) *(?P<op>(\?|:{1,3}|\+|\!)?=)?')
SPLITTING_LONG_LINE_RGX = r'([^\\\n]|\\[$#%\\tr])*\\$'


class ParsingContext(ABC):
    pass


@dataclass
class StrParsingContext(ParsingContext):
    string: str


@dataclass
class IntParsingContext(ParsingContext):
    integer: str


class BaseParsingContext(ParsingContext):
    pass


class RuleParsingContext(IntParsingContext):
    pass


class VariableParsingContext(StrParsingContext):
    pass


class MakefileParser:
    def __init__(self, stream: str):
        self._ctx = BaseParsingContext()
        self._stream: list[str] = stream.split('\n')
        self._makefile = Makefile()


    def accept_directive(self) -> bool:
        # BUG: skips empty lines
        self._stream.pop(0)
        return True


    def accept_directive_var(self) -> bool:
        line = self._stream[0].strip()
        _match = DIRECTIVE_VAR_RGX.match(line)
        if _match is None:
            return False

        varname = _match.group('varname')
        assert varname is not None
        operator = _match.group('op') or '='
        self._makefile.variables[varname] = Variable(varname, operator)
        self._ctx = VariableParsingContext(varname)
        self._stream.pop(0)
        return True


    def accept_inline_var(self) -> bool:
        line = self._stream[0].strip()
        _match = INLINE_VAR_RGX.match(line)
        if _match is None:
            return False

        varname = _match.group('varname')
        operator = _match.group('op')
        value = _match.group('varvalue')
        assert varname is not None 
        assert operator is not None
        assert value is not None

        # TODO: distinguish between different operators
        self._makefile.variables[varname] = Variable(varname, operator, value)
        self._stream.pop(0)
        return True


    def enter_variable(self) -> bool:
        return self.accept_directive_var() or self.accept_inline_var()


    def enter_rule(self) -> bool:
        line = self._stream[0]
        print(f'RULE0:: [{line}]')
        _match = RECIPE_RGX.match(line)
        print('RULE1::', _match)
        if _match is None: # has no match
            return False

        recipe = _match.group('recipe')
        self._makefile.rules.append(Rule(
            Filenames.from_filenames(_match.group('targets').strip()),
            Filenames.from_filenames(_match.group('prereqs').strip()),
            not self._makefile.rules, _match.group('grouped') is not None,
            [] if not recipe else [ recipe.lstrip(';').strip() ]
        ))
        
        last_rule_idx = len(self._makefile.rules) - 1
        # switch to parse recipe in rule context
        self._ctx = RuleParsingContext(last_rule_idx)
        self._stream.pop(0)
        return True


    def exit_base(self) -> bool:
        return (
            self.enter_rule() or self.enter_variable()
            or self.accept_directive()
        )


    def exit_rule(self) -> bool:
        line = self._stream[0]
        if not line.startswith(RECIPE_PREFIX):
            self._ctx = BaseParsingContext()
            return self.exit_base()

        self._makefile.rules[self._ctx.integer].recipe.append(
            line.lstrip(RECIPE_PREFIX).strip()
        )
        self._stream.pop(0)
        return True


    def exit_variable(self) -> bool:
        line = self._stream[0].strip()
        if line == 'endef':
            self._ctx = BaseParsingContext()
            self._stream.pop(0)
            return True

        self._makefile.variables[self._ctx.string] += line
        self._stream.pop(0)
        return True


    def accept_single(self) -> bool:
        if isinstance(self._ctx, BaseParsingContext):
            return self.exit_base()
        elif isinstance(self._ctx, RuleParsingContext):
            return self.exit_rule()
        elif isinstance(self._ctx, VariableParsingContext):
            return self.exit_variable()
        else:
            print('Parse error')
            return False


    def accept(self) -> Optional[Makefile]:
        result = True
        while len(self._stream) > 0:
            result = result and self.accept_single()
            if not result:
                return None
        return self._makefile
