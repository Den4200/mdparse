from typing import List

class Markdown:

    def __init__(self, lines: List[List[str]]):
        self._lines = lines

    def __str__(self):
        return f'Markdown({self._lines})'

    def __repr__(self):
        return f'Markdown({self._lines})'

    def __getitem__(self, item):
        return self._lines[item]
