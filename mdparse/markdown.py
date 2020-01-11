from typing import List
from .constants import HTML


class Markdown:

    def __init__(self, lines: List[List[str]]):
        self._lines = lines

    def __str__(self):
        return f'Markdown({self._lines})'

    def __repr__(self):
        return f'Markdown({self._lines})'

    def __getitem__(self, item):
        return self._lines[item]

    def html(self):
        """
        Converts Markdown to HTML.
        """
        html = list()

        ul = list()
        li = False

        for line in self._lines:

            for key, tag in HTML.items():

                if line[0] == key:
                    formatted = tag.format(line[1])

                    if key == 'bullet':
                        ul.append(formatted)
                        li = True
                    
                    elif li == True:
                        html.append(
                            HTML['ul'].format(''.join([*ul]))
                        )
                        html.append(formatted)

                        ul = list()
                        li = False

                    else:
                        html.append(formatted)
                    
                    break

        if li == True:
            html.append(
                HTML['ul'].format(''.join([*ul]))
            )

        return html
