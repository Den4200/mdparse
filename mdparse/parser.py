from typing import (
    Dict, 
    Generator, 
    List, 
    TextIO, 
    Tuple, 
    Union
)
from .markdown import Markdown
from .constants import MARKS


class Parser:

    def __init__(self, fp: Union[str, List, TextIO]):
        """
        Checks whether fp is any of these
        [
            file pointer,
            string,
            list
        ]
        """
        try:
            self.content = [line.strip('\n') for line in fp.readlines()]

        except AttributeError:
            
            if isinstance(fp, str):
                self.content = fp.splitlines()

            elif isinstance(fp, list):
                self.content = [line.strip('\n') for line in fp]

            else:
                raise TypeError('Only accepts a file pointer, list, or string.')

    def parse(self) -> Markdown:
        """
        Parses a Markdown file and passes tokens to
        a Markdown class instance.

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
