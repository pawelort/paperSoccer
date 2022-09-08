import openpyxl
from openpyxl.styles.borders import Border, Side
class CoreField():
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.status = {'d1': False,
                       'd2': False}

    def status_change(self, direction):
        if self.status.get(direction) == False:
            self.status[direction] = True
            return True
        else:
            return False

    def available_moves(self):
        return {direction: status for direction, status in self.status.items() if status == False}

class CustomField(CoreField):
    def __init__(self, row, col, **borders):
        super().__init__(row, col)
        self.status.update(borders)



class Board():
    # indexes of rows and colums are 1 based
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.fields = {}
        gate_pos = [int(self.cols // 2), int(self.cols // 2) + 1]
        for x in range(1, self.rows + 1):
            for y in range(1, self.cols + 1):
                pos = (x, y)
                if x == self.rows and y == self.cols:
                    self.fields[pos] = CoreField(x, y)
                elif x == self.rows and y in gate_pos:
                    self.fields[pos] = CustomField(x, y, right=False, bottom=False)
                elif x == self.rows:
                    self.fields[pos] = CustomField(x, y, right=False)
                elif y == self.cols:
                    self.fields[pos] = CustomField(x, y, bottom=False)
                elif x == 1 and y in gate_pos:
                    self.fields[pos] = CustomField(x, y, right=False, top=False, bottom=False)
                else:
                    self.fields[pos] = CustomField(x, y, right=False, bottom=False)

        self.fields[0, gate_pos[0]] = CustomField(0, gate_pos[0], right=False)
        self.fields[0, gate_pos[1]] = CoreField(0, gate_pos[1])
        self.fields[self.rows + 1, gate_pos[0]] = CustomField(self.rows + 1, gate_pos[0], right=False)
        self.fields[self.rows + 1, gate_pos[1]] = CoreField(self.rows + 1, gate_pos[1])

        # self.board = {(x, y): SingleField(x, y) for x in range(1, rows + 1) for y in range(1, cols + 1)}

    def move_executed(self, row, col, direction):
        return self.fields.get((row, col)).status_change(direction)

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
