from colorama import Fore


def colorize(text, color, colors_enabled):
    if colors_enabled:
        return color + text + Fore.RESET
    else:
        return text


class TableRowBase:
    def to_string(self, prev, next, colors_enabled):
        raise NotImplementedError()


class Section(TableRowBase):
    name = None
    _table: 'FancyTable' = None

    def __init__(self, name, table):
        self.name = name
        self._table = table

    def to_string(self, prev, next, colors_enabled):
        def border(t):
            return colorize(t, Fore.LIGHTBLACK_EX, colors_enabled)

        widths = self._table.widths
        result = list()
        result.append(border('┠─' + '─┴─'.join(['─'*w for w in widths]) + '─┨'))
        result.append(border('┃ ') + self.name.center(sum(widths) + 3 * (len(widths) - 1)) + border(' ┃'))
        result.append(border('┠─' + '─┬─'.join(['─' * w for w in widths]) + '─┨'))
        return result


class Row(TableRowBase):
    row: list = None
    _table: 'FancyTable' = None

    def __init__(self, row, table):
        self.row = row
        self._table = table

    def to_string(self, prev=None, next=None, colors_enabled):
        def border(t):
            return colorize(t, Fore.LIGHTBLACK_EX, colors_enabled)

        widths = self._table.widths
        result = list()
        result.append(
            border('┃ ') +
            border(' │ ').join([td.center(widths[idx]) for idx, td in enumerate(self.row)]) +
            border(' ┃')
        )
        return result


class FancyTable:
    columns = []
    rows = []
    widths = []

    def __init__(self, columns):
        self.columns = columns
        self.widths = [len(i) for i in columns]

    def __str__(self):
        return self.to_string()

    def add_row(self, row: list):
        assert len(row) == len(self.columns)
        # setting maximum widths for columns
        for idx, field in enumerate(row):
            if self.widths[idx] < len(field):
                self.widths[idx] = len(field)
        self.rows.append(Row(row, self))

    def add_section(self, section_name):
        self.rows.append(Section(section_name, self))

    def to_string(self, colors_enabled=True):
        def border(t):
            return colorize(t, Fore.LIGHTBLACK_EX, colors_enabled)

        result = []
        total_width = sum(self.widths) + (len(self.widths) - 1) * 3 + 4
        result.append(border(
            '┏━' + '━┯━'.join(['━' * w for w in self.widths]) + '━┓'
        ))

        header = [col.center(self.widths[idx]) for idx, col in enumerate(self.columns)]
        header = border('┃ ') + border(' │ ').join(header) + border(' ┃')
        result.append(header)

        if type(self.rows[0]) == Row:
            result.append(border('┣━' + '━┿━'.join(['━' * w for w in self.widths]) + '━┫'))
        else:
            result.append(border('┣━' + '━┷━'.join(['━' * w for w in self.widths]) + '━┫'))

        for idx, row in enumerate(self.rows):
            result += row.to_string(
                row[idx-1] if idx > 0 else None,
                row[idx+1] if idx < len(self.rows)-1 else None,
                colors_enabled
            )

        result.append(border('┗━' + '━┷━'.join(['━' * w for w in self.widths]) + '━┛'))
        return '\n'.join(result)
