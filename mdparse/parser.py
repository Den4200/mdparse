from typing import Dict, Generator, List, TextIO, Tuple
from .markdown import Markdown
from .constants import MARKS


class Parser:

    def __init__(self, fp: TextIO) -> None:
        self.content = [line.strip('\n') for line in fp.readlines()]

    def parse(self) -> Markdown:
        """
        Parse a Markdown file and return tokens.

        Returns an instance of the Markdown class.
        """
        lines = list()

        for line in self.content:
            end = False

            for mark in MARKS.keys():

                if line.startswith(mark):
                    lines.append([MARKS[mark], line[len(mark)+1:]])
                    end = True
                    break

            if not end:
                lines.append(['line', line])

        combined = self._combine_lines(lines)
        lines = [line for line in lines if line[0] != 'line']

        for index, value in combined.items():
            lines.insert(index, ['line', value])

        return Markdown(lines)

    @staticmethod
    def _combine_lines(content: List[List[str]]) -> Dict[int, str]:
        """
        Combine all multi-lines into single lines.
        """
        ranges = Parser._line_range(content)
        lines = dict()

        for r in ranges:
            lines.update({
                r[list(r.keys())[0]][0]: ''.join(
                    line for line in r[list(r.keys())[0]][1]
                )
            })

        return lines

    @staticmethod
    def _line_range(content
        ) -> Generator[Dict[int, Tuple[int, List[str]]], None, None]:
        """
        Groups consecutive lines together.

        Returns start indices and their coresponding lines.
        """
        lines = [(index, line) for index, line in 
                enumerate(content) if line[0] == 'line']

        result = list()
        last = lines[0][0]
        idx = lambda idx: Parser._check_list(idx, lines)

        for value in [line[0] for line in lines]: 

            if value - last > 1:
                yield {
                    len(result): (
                        result[0], [lines[idx(r)][1][1] for r in result]
                        )
                    }
                result = list()

            result.append(value)
            last = value

        yield {
            len(result): (
                result[0], [lines[idx(r)][1][1] for r in result]
                )
            }

    @staticmethod
    def _check_list(item: int, lst: List[str]) -> int:
        """
        Returns list index from file lines index.
        """
        for value in lst:
            if value[0] == item:
                return lst.index(value)
