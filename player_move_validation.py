'''
This module should check all possible player movement
'''

def req_loc_verif(line_x, line_y, req_line_x, req_line_y):
    if line_x == req_line_x and line_y == req_line_y:
        return False
    elif abs(line_x - req_line_x) > 1 or abs(line_y - req_line_y) > 1:
        return False
    else:
        return True

def location_possibilities(board, line_x, line_y):
    possible_fields = []
    try:
        possible_fields.append(board.fields.get((line_x, line_y + 1)))
    except:
        possible_fields.append(False)
    try:
        possible_fields.append(board.fields.get((line_x, line_y)))
    except:
        possible_fields.append(False)
    try:
        possible_fields.append(board.fields.get((line_x + 1, line_y)))
    except:
        possible_fields.append(False)
    try:
        possible_fields.append(board.fields.get((line_x + 1, line_y + 1)))
    except:
        possible_fields.append(False)

    return possible_fields

def field_status_possibilities(pos_fields):
    # moves availability based on compass rose
    player_available_moves = []
    if pos_fields[0]:
        if pos_fields[0].status.get('bottom') == False:
            player_available_moves.append('e')
        if pos_fields[0].status.get('d2') == False:
            player_available_moves.append('ne')
        if pos_fields[0].status.get('left') == False:
            player_available_moves.append('n')

    if pos_fields[1]:
        if pos_fields[1].status.get('right') == False:
            player_available_moves.append('n')
        if pos_fields[1].status.get('d1') == False:
            player_available_moves.append('nw')
        if pos_fields[1].status.get('bottom') == False:
            player_available_moves.append('w')

    if pos_fields[2]:
        if pos_fields[2].status.get('top') == False:
            player_available_moves.append('w')
        if pos_fields[2].status.get('d2') == False:
            player_available_moves.append('sw')
        if pos_fields[2].status.get('right') == False:
            player_available_moves.append('s')

    if pos_fields[3]:
        if pos_fields[3].status.get('left') == False:
            player_available_moves.append('s')
        if pos_fields[3].status.get('d1') == False:
            player_available_moves.append('se')
        if pos_fields[3].status.get('top') == False:
            player_available_moves.append('e')

    return player_available_moves

def avl_cartesian_coordinate(line_x, line_y, player_avl_moves):
    cartesian_coordinates = []
    if 'e' in player_avl_moves:
        cartesian_coordinates.append((line_x, line_y + 1))
    if 'ne' in player_avl_moves:
        cartesian_coordinates.append((line_x - 1, line_y + 1))
    if 'n' in player_avl_moves:
        cartesian_coordinates.append((line_x - 1, line_y))
    if 'nw' in player_avl_moves:
        cartesian_coordinates.append((line_x - 1, line_y - 1))
    if 'w' in player_avl_moves:
        cartesian_coordinates.append((line_x, line_y - 1))
    if 'sw' in player_avl_moves:
        cartesian_coordinates.append((line_x + 1, line_y - 1))
    if 's' in player_avl_moves:
        cartesian_coordinates.append((line_x + 1, line_y))
    if 'se' in player_avl_moves:
        cartesian_coordinates.append((line_x + 1, line_y + 1))

    return cartesian_coordinates


def player_move_check(board, line_x, line_y, req_line_x, req_line_y):
    player_pos_moves_geo = field_status_possibilities(location_possibilities(board, line_x, line_y))
    player_pos_moves_cartesian = avl_cartesian_coordinate(line_x, line_y, player_pos_moves_geo)
    return (req_line_x, req_line_y) in player_pos_moves_cartesian


def azimuth_identification(line_x, line_y, req_line_x, req_line_y):

    if req_line_y > line_y:
        if req_line_x == line_x:
            azimuth = 'e'
        elif req_line_x < line_x:
            azimuth = 'ne'
        elif req_line_x > line_x:
            azimuth = 'se'
    elif req_line_y < line_y:
        if req_line_x == line_x:
            azimuth = 'w'
        elif req_line_x < line_x:
            azimuth = 'nw'
        elif req_line_x > line_x:
            azimuth = 'sw'
    elif req_line_y == line_y:
        if req_line_x < line_x:
            azimuth = 'n'
        elif req_line_x > line_x:
            azimuth = 's'
    else:
        azimuth = None

    return line_x, line_y, azimuth


def board_field_sel(board, line_x, line_y, azimuth):
    if azimuth == 'e':
        fields = [(board.fields.get((line_x, line_y + 1)), 'bottom'), (board.fields.get((line_x + 1, line_y + 1)), 'top')]
        dir_status = [field.status.get(dir) for field, dir in fields]
        if None not in dir_status:
            raise Exception("ambiguity in board fields!")
        fields.pop(dir_status.index(None))
        row = fields[0][0].row
        col = fields[0][0].col
        direction = fields[0][1]

    elif azimuth == 'ne':
        row = board.fields.get((line_x, line_y + 1)).row
        col = board.fields.get((line_x, line_y + 1)).col
        direction = 'd2'

    elif azimuth == 'n':
        fields = [(board.fields.get((line_x, line_y + 1)), 'left'), (board.fields.get((line_x, line_y)), 'right')]
        dir_status = [field.status.get(dir) for field, dir in fields]
        if None not in dir_status:
            raise Exception("ambiguity in board fields!")
        fields.pop(dir_status.index(None))
        row = fields[0][0].row
        col = fields[0][0].col
        direction = fields[0][1]

    elif azimuth == 'nw':
        row = board.fields.get((line_x, line_y)).row
        col = board.fields.get((line_x, line_y)).col
        direction = 'd1'

    elif azimuth == 'w':
        fields = [(board.fields.get((line_x, line_y)), 'bottom'), (board.fields.get((line_x + 1, line_y)), 'top')]
        dir_status = [field.status.get(dir) for field, dir in fields]
        if None not in dir_status:
            raise Exception("ambiguity in board fields!")
        fields.pop(dir_status.index(None))
        row = fields[0][0].row
        col = fields[0][0].col
        direction = fields[0][1]

    elif azimuth == 'sw':
        row = board.fields.get((line_x + 1, line_y)).row
        col = board.fields.get((line_x + 1, line_y)).col
        direction = 'd2'

    elif azimuth == 's':
        fields = [(board.fields.get((line_x + 1, line_y)), 'right'), (board.fields.get((line_x + 1, line_y + 1)), 'left')]
        dir_status = [field.status.get(dir) for field, dir in fields]
        if None not in dir_status:
            raise Exception("ambiguity in board fields!")
        fields.pop(dir_status.index(None))
        row = fields[0][0].row
        col = fields[0][0].col
        direction = fields[0][1]

    elif azimuth == 'se':
        row = board.fields.get((line_x + 1, line_y + 1)).row
        col = board.fields.get((line_x + 1, line_y + 1)).col
        direction = 'd1'

    else:
        row = -1
        col = -1
        direction = -1

    return row, col, direction

# errors = []
#
# for field in board.board.fields.values():
#     avl_moves = field_status_possibilities(location_possibilities(field.row, field.col))
#     if avl_moves.count('e') > 1:
#         errors.append(('e', f'row {field.row} col {field.col}'))
#     if avl_moves.count('ne') > 1:
#         errors.append(('ne', f'row {field.row} col {field.col}'))
#     if avl_moves.count('n') > 1:
#         errors.append(('n', f'row {field.row} col {field.col}'))
#     if avl_moves.count('nw') > 1:
#         errors.append(('nw', f'row {field.row} col {field.col}'))
#     if avl_moves.count('w') > 1:
#         errors.append(('w', f'row {field.row} col {field.col}'))
#     if avl_moves.count('sw') > 1:
#         errors.append(('sw', f'row {field.row} col {field.col}'))
#     if avl_moves.count('s') > 1:
#         errors.append(('s', f'row {field.row} col {field.col}'))
#     if avl_moves.count('se') > 1:
#         errors.append(('se', f'row {field.row} col {field.col}'))
#
# print(errors)