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
    test1 = Parser(f).parse()

    f.seek(0)
    test2 = Parser(f.read()).parse()

    f.seek(0)
    test3 = Parser(f.readlines()).parse()

with open(Path('tests/result.txt'), 'r') as f:
    result = eval(f.read())

with open(Path('tests/result.html'), 'r') as f:
    html = f.read()

# ----- #

passed = list()
tests = [
    list(test1) == result, 
    list(test2) == result, 
    list(test3) == result,
    '\n'.join(test1.html()) == html
]

for idx, test in enumerate(tests, 1):
    if test:
        print(f'Test {idx} successful!')
        passed.append(True)
    else:
        print(f'Test {idx} failed.')
        passed.append(False)

if all(passed):
    sys.exit(0)
sys.exit(1)
