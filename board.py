import openpyxl
from openpyxl.styles.borders import Border, Side


class CoreField():
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.status = {'d1': 0,
                       'd2': 0}

    def status_change(self, direction, player):
        if self.status.get(direction) == 0:
            self.status[direction] = player
            return True
        else:
            return False

    def available_moves(self):
        return {direction: status for direction, status in self.status.items() if status == False}


class CustomField(CoreField):
    def __init__(self, row, col, **borders):
        super().__init__(row, col)
        self.status.update(borders)

class FieldOngoingGame(CoreField):
    def __init__(self, row, col, status):
        self.row = row
        self.col = col
        self.status = status

class Board():
    # indexes of rows and columns are 1 based
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.fields = {}

    def move_executed(self, row, col, direction, player):
        return self.fields.get((row, col)).status_change(direction, player)


class BoardNewGame(Board):
    def __init__(self, rows, cols):
        super().__init__(rows, cols)

        gate_pos = [int(self.cols // 2), int(self.cols // 2) + 1]
        for x in range(1, self.rows + 1):
            for y in range(1, self.cols + 1):
                pos = (x, y)
                if x == self.rows and y == self.cols:
                    self.fields[pos] = CoreField(x, y)
                elif x == self.rows and y in gate_pos:
                    self.fields[pos] = CustomField(x, y, right=0, bottom=0)
                elif x == self.rows:
                    self.fields[pos] = CustomField(x, y, right=0)
                elif y == self.cols:
                    self.fields[pos] = CustomField(x, y, bottom=0)
                elif x == 1 and y in gate_pos:
                    self.fields[pos] = CustomField(x, y, right=0, top=0, bottom=0)
                else:
                    self.fields[pos] = CustomField(x, y, right=0, bottom=0)

        self.fields[0, gate_pos[0]] = CustomField(0, gate_pos[0], right=0)
        self.fields[0, gate_pos[1]] = CoreField(0, gate_pos[1])
        self.fields[self.rows + 1, gate_pos[0]] = CustomField(self.rows + 1, gate_pos[0], right=0)
        self.fields[self.rows + 1, gate_pos[1]] = CoreField(self.rows + 1, gate_pos[1])

        # self.board = {(x, y): SingleField(x, y) for x in range(1, rows + 1) for y in range(1, cols + 1)}

class BoardOngoingGame(Board):
    def __init__(self, rows, cols, fields):
        super().__init__(rows, cols)
        for field in fields:
            self.fields.update({(field.get('row'), field.get('col')): FieldOngoingGame(field.get('row'), field.get('col'), field.get('status'))})


def create_board(rows, cols):
    # amount of columns need to be even, and greater than 6
    pass

def draw_board(excel_sheet, field_obj):
    # offset added to place board in different location within excel sheet
    offset_row, offset_col = field_obj.row + 2, field_obj.col + 2
    excel_sheet.cell(offset_row, offset_col).border = Border(diagonalUp=True, diagonalDown=True, diagonal=Side('thick'),
                                                             right=None if None == field_obj.status.get('right') else Side('thick'),
                                                             top=None if None == field_obj.status.get('top') else Side('thick'),
                                                             left=None if None == field_obj.status.get('left') else Side('thick'),
                                                             bottom=None if None == field_obj.status.get('bottom') else Side('thick'))

# board = Board(20, 10)
#
# test_workbook = openpyxl.Workbook()
# soccer = test_workbook.active
#
# for field in board.fields.values():
#     draw_board(soccer, field)
# test_workbook.save('soccer.xlsx')
