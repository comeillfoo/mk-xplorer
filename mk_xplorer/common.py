#!/usr/bin/env python3
import re
from dataclasses import dataclass
from context import *

@dataclass
class Filenames:
    def __init__(self, filenames: str):
        self.filenames = filenames.strip().split(' ')

    def __str__(self) -> str:
        return ' '.join(self.filenames)


FILENAME_STX = '[a-zA-Z0-9](?:[a-zA-Z0-9 ._-]*[a-zA-Z0-9])?\.[a-zA-Z0-9_-]+'

@dataclass
class Rule:
    RECIPE_PREFIX='\t'
    TARGETS_PREREQS_STX = f'({FILENAME_STX} )*({FILENAME_STX})'
    RECIPE_STX = re.compile(f'(?P<targets>{TARGETS_PREREQS_STX})(?P<grouped>\&)?: *(?P<prereqs>{TARGETS_PREREQS_STX}) *(?P<recipe>;.*)?')

    def __init__(self, targets: Filenames, prerequisittes: Filenames,
                 is_default: bool = False, is_grouped: bool = False,
                 recipe: list[str] = []):
        self.is_default = is_default
        self.targets = targets
        self.is_grouped_or_independent = is_grouped # targets grouped or independent
        self.prerequisites = prerequisittes
        self.recipe: list[str] = recipe


    def __str__(self) -> str:
        return str(self.targets) \
            + ' ' + ('&:' if self.is_grouped_or_independent else ':') \
            + ' ' + str(self.prerequisites) + '\n' \
            + '\n'.join(map(lambda s: Rule.RECIPE_PREFIX + s, self.recipe))


INLINE_VARIABLE_STX = re.compile(r'(?P<varname>\w+) *(?P<op>(\?|:{1,3}|\+|\!)?=) *(?P<varvalue>.*)')
DIRECTIVE_VARIABLE_STX = re.compile(r'define +(?P<varname>\w+) *(?P<op>(\?|:{1,3}|\+|\!)?=)?')

class MakefileParser():

    def __init__(self):
        self.parser_ctx: ParserContext = BaseParserContext()
        self.rules: list[Rule] = []
        self.variables = {}


    def _accept_rule(self, mk_line: str) -> bool:
        match_rule = Rule.RECIPE_STX.match(mk_line)
        if not match_rule: # has no match
            return False

        recipe = match_rule.group('recipe')
        self.rules.append(Rule(
            Filenames(match_rule.group('targets').strip()),
            Filenames(match_rule.group('prereqs').strip()),
            not self.rules, match_rule.group('grouped') is not None,
            [] if not recipe else [ recipe.lstrip(';').strip() ]))

        # switch to parse recipe in rule context
        self.parser_ctx = RuleParserContext(len(self.rules) - 1)
        return True


    def _accept_variable(self, mk_line: str) -> bool:
        mk_line = mk_line.strip()
        match_directive_var = DIRECTIVE_VARIABLE_STX.match(mk_line)
        if match_directive_var:
            varname = match_directive_var.group('varname')
            operator = match_directive_var.group('op') or '='
            self.variables[varname] = {
                'operator': operator,
                'value': ''
            }
            self.parser_ctx = VariableParserContext(varname)
            return True

        match_inline_var = INLINE_VARIABLE_STX.match(mk_line)
        if not match_inline_var:
            return False

        # TODO: distinguish between different operators

        self.variables[match_inline_var.group('varname')] = {
            'operator': match_inline_var.group('op'),
            'value': match_inline_var.group('varvalue')
        }

        return True


    def _accept_directive(self, mk_line: str) -> bool:
        return True


    def _parse_base_ctx(self, mk_line: str) -> bool:
        return self._accept_rule(mk_line) \
            or self._accept_variable(mk_line) \
            or self._accept_directive(mk_line)


    def _parse_rule_ctx(self, mk_line: str) -> bool:
        if not mk_line.startswith(Rule.RECIPE_PREFIX):
            self.parser_ctx = BaseParserContext()
            return self._parse_base_ctx(mk_line)

        self.rules[self.parser_ctx.integer].recipe \
            .append(mk_line.lstrip(Rule.RECIPE_PREFIX).strip())
        return True


    def _parse_variable_ctx(self, mk_line: str) -> bool:
        if mk_line.strip() == 'endef':
            self.parser_ctx = BaseParserContext()
            return True

        self.variables[self.parser_ctx.string] += mk_line.strip()
        return True


    _line_handlers = {
        ParserContexts.BASE_CTX: _parse_base_ctx,
        ParserContexts.RULE_CTX: _parse_rule_ctx,
        ParserContexts.VARIABLE_CTX: _parse_variable_ctx
    }


    def parse_line(self, mk_line: str):
        key = ParserContexts(0)
        key |= ParserContexts.BASE_CTX if isinstance(self.parser_ctx, BaseParserContext) else key
        key |= ParserContexts.RULE_CTX if isinstance(self.parser_ctx, RuleParserContext) else key
        key |= ParserContexts.VARIABLE_CTX if isinstance(self.parser_ctx, VariableParserContext) else key
        try:
            return self._line_handlers[key](self, mk_line)
        except IndexError:
            raise ValueError


    def parse(self, makefile: str):
        for line in makefile.split('\n'):
            self.parse_line(line)
