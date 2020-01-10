from sys import path
from os.path import dirname

path.append(dirname(path[0]))
__package__ = 'tests'

# ----- #

import sys
from pathlib import Path
from mdparse.parser import Parser

# ----- #

with open(Path('tests/example.md'), 'r') as f:
    content = Parser(f).parse()

with open(Path('tests/result.txt'), 'r') as f:
    result = eval(f.read())

# ----- #

if content == result:
    print('Test successful!')
    sys.exit(0)
else:
    print('Test failed.')
    sys.exit(1)
