import player_movement as player
import player_move_validation as validate
import board
import random

class Game():
    game_id = 1

    def __init__(self, player1_name, player2_name, board_row, board_col):
        Game.game_id += 1
        self.player1 = player.Player(player1_name)
        self.player2 = player.Player(player2_name)
        self.board = board.Board(board_row, board_col)
        self.current_turn = random.choice((1, 2))
        self.curr_loc_line_x = board_row // 2
        self.curr_loc_line_y = board_col // 2
        self.all_locations = [(self.curr_loc_line_x, self.curr_loc_line_y)]

    @classmethod
    def game_standard_size(cls, player1_name, player2_name):
        return cls(player1_name, player2_name, 10, 8)


    def move(self, req_line_x, req_line_y):
        if not validate.req_loc_verif(self.curr_loc_line_x, self.curr_loc_line_y, req_line_x, req_line_y):
            return False

        field = validate.board_field_sel(self.board, *validate.azimuth_identification(self.curr_loc_line_x, self.curr_loc_line_y, req_line_x, req_line_y))
        if field[2] == None:
            return False

        if not self.board.move_executed(*field):
            return False

        self.curr_loc_line_x = req_line_x
        self.curr_loc_line_y = req_line_y
        self.all_locations.append((self.curr_loc_line_x, self.curr_loc_line_y))

        if self.current_turn == 1:
            self.player1.player_move(*field)
            self.current_turn = 2
        else:
            self.player2.player_move(*field)
            self.current_turn = 1

        return True

    def avl_player_moves_geo(self):
        return validate.field_status_possibilities(validate.location_possibilities(self.board, self.curr_loc_line_x, self.curr_loc_line_y))

    def avl_player_moves_cartesian(self):
        return validate.avl_cartesian_coordinate(self.curr_loc_line_x, self.curr_loc_line_y, self.avl_player_moves_geo())

