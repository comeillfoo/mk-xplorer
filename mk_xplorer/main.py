#!/usr/bin/env python3
import argparse
import sys
import os
import errno

from splitting_lines import eliminate_splitting_lines
from comments import eliminate_comments
from common import MakefileParser


def args_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser('mk_parser',
                                description='Makefile parser')
    p.add_argument('makefile', help='path to makefile that should be parsed')

    return p


def main() -> int:
    args = args_parser().parse_args()

    if not os.path.isfile(args.makefile):
        return errno.ENOENT

    with open(args.makefile, encoding='utf-8') as mk_file:
        makefile = mk_file.read()

    preprocessed_mk = eliminate_comments(eliminate_splitting_lines(makefile))

    mk_parser = MakefileParser()
    mk_parser.parse(preprocessed_mk)
    return 0


if __name__ == '__main__':
    sys.exit(main())
