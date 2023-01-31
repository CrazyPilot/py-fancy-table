from colorama import Fore


def colorize(text, color, colors_enabled):
    if colors_enabled:
        return color + text + Fore.RESET
    else:
        return text


class TableRowBase:
    def to_string(self, prev_row, next_row, colors_enabled):
        raise NotImplementedError()


class Section(TableRowBase):
    name = None
    _table: 'FancyTable' = None

    def __init__(self, name, table):
        self.name = name
        self._table = table

    def to_string(self, prev_row, next_row, colors_enabled):
        def border(t):
            return colorize(t, Fore.LIGHTBLACK_EX, colors_enabled)

        widths = self._table.widths
        result = list()

        if prev_row is None:  # первая строка в таблице
            # рисуем нижнюю часть шапки
            result.append(border('┣━' + '━┷━'.join(['━' * w for w in widths]) + '━┫'))
        elif type(prev_row) is Row:
            # перед секцией была обычная строка
            result.append(border('┠─' + '─┴─'.join(['─'*w for w in widths]) + '─┨'))
        elif type(prev_row) is Section:
            pass
        else:
            raise NotImplementedError

        result.append(border('┃ ') + self.name.center(sum(widths) + 3 * (len(widths) - 1)) + border(' ┃'))

        if next_row is None:  # это последняя строка
            result.append(border('┗━' + '━━━'.join(['━' * w for w in widths]) + '━┛'))
        elif type(next_row) is Row:
            result.append(border('┠─' + '─┬─'.join(['─' * w for w in widths]) + '─┨'))
        elif type(next_row) is Section:
            result.append(border('┠─' + '───'.join(['─' * w for w in widths]) + '─┨'))
        else:
            raise NotImplementedError
        return result


class Row(TableRowBase):
    row: list = None
    _table: 'FancyTable' = None

    def __init__(self, row, table):
        self.row = row
        self._table = table

    def to_string(self, prev_row, next_row, colors_enabled):
        def border(t):
            return colorize(t, Fore.LIGHTBLACK_EX, colors_enabled)

        widths = self._table.widths
        result = list()

        if prev_row is None:  # первая строка в таблице
            # рисуем нижнюю часть шапки
            result.append(border('┣━' + '━┿━'.join(['━' * w for w in widths]) + '━┫'))

        result.append(
            border('┃ ') +
            border(' │ ').join([str(td).center(widths[idx]) for idx, td in enumerate(self.row)]) +
            border(' ┃')
        )

        if next_row is None:  # это последняя строка
            result.append(border('┗━' + '━┷━'.join(['━' * w for w in widths]) + '━┛'))

        return result


class FancyTable:
    caption = None
    columns: list = None
    rows: list = None
    widths: list = None

    def __init__(self, columns: list, caption=None):
        self.caption = caption
        self.columns = columns
        self.widths = [len(i) for i in columns]
        self.rows = []

    def __str__(self):
        return self.to_string()

    def add_row(self, row: list):
        assert len(row) == len(self.columns)
        # setting maximum widths for columns
        for idx, field in enumerate(row):
            if self.widths[idx] < len(str(field)):
                self.widths[idx] = len(str(field))
        self.rows.append(Row(row, self))

    def add_rows(self, rows: list):
        for row in rows:
            self.add_row(row)

    def add_section(self, section_name):
        self.rows.append(Section(section_name, self))

    def to_string(self, colors_enabled=True):
        def border(t):
            return colorize(t, Fore.LIGHTBLACK_EX, colors_enabled)

        result = []
        total_width = sum(self.widths) + (len(self.widths) - 1) * 3 + 4
        if self.caption:
            result.append(border('┏' + '━'*(total_width-2) + '┓'))
            result.append(border('┃ ') + self.caption.center(total_width - 4) + border(' ┃'))
            result.append(border('┣━' + '━┯━'.join(['━' * w for w in self.widths]) + '━┫'))
        else:
            result.append(border('┏━' + '━┯━'.join(['━' * w for w in self.widths]) + '━┓'))

        header = [col.center(self.widths[idx]) for idx, col in enumerate(self.columns)]
        header = border('┃ ') + border(' │ ').join(header) + border(' ┃')
        result.append(header)

        for idx, row in enumerate(self.rows):
            result += row.to_string(
                self.rows[idx-1] if idx > 0 else None,
                self.rows[idx+1] if idx < len(self.rows)-1 else None,
                colors_enabled
            )

        return '\n'.join(result)
