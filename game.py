import player_movement as player
import player_move_validation as validate
import board
import model
import random

model_handler = model.ModelHandler(model.game_db)

class Game():

    def __init__(self, player1_name, player2_name, max_board_row, max_board_col):
        self.player1 = player.Player(player1_name)
        self.player2 = player.Player(player2_name)
        self.board = board.BoardNewGame(max_board_row, max_board_col)
        self.current_turn = random.choice((1, 2))
        self.curr_loc_line_x = max_board_row // 2
        self.curr_loc_line_y = max_board_col // 2
        self.all_locations = [(self.curr_loc_line_x, self.curr_loc_line_y)]
        self.border = {'horizontal': [0, max_board_row], 'vertical': [0, max_board_col]}
        self.gate_player1 = ((-1, (max_board_col // 2) - 1),
                             (-1, (max_board_col // 2)),
                             (-1, (max_board_col // 2) + 1))
        self.gate_player2 = ((max_board_row + 1, (max_board_col // 2) - 1),
                             (max_board_row + 1, (max_board_col // 2)),
                             (max_board_row + 1, (max_board_col // 2) + 1))
        self.game_status = 1

        self.game_id = str(model_handler.game_to_database(self.player1,
                                                          self.player2,
                                                          self.board,
                                                          self.current_turn,
                                                          self.curr_loc_line_x,
                                                          self.curr_loc_line_y,
                                                          self.all_locations,
                                                          self.border,
                                                          self.gate_player1,
                                                          self.gate_player2,
                                                          self.game_status).inserted_id)
        """game status
        1 = game in progress; 
        11 = pl1 wins due to score; 
        12 = pl1 wins due to lack of move by pl2; 
        21 = pl2 wins due to score; 
        22 = pl2 wins due to lack of move by pl1"""

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


        if self.current_turn == 1:
            self.player1.player_move(*field)
            if not (self.detect_previous_loc() or self.detect_border()):
                self.current_turn = 2
        else:
            self.player2.player_move(*field)
            if not (self.detect_previous_loc() or self.detect_border()):
                self.current_turn = 1

        self.all_locations.append((self.curr_loc_line_x, self.curr_loc_line_y))
        self.win_detection()
        self.defeat_detection()
        return True

    def detect_border(self):
        if self.curr_loc_line_x in self.border.get('horizontal'):
            if self.curr_loc_line_y == self.border.get('vertical')[1] // 2:
                # gate detection
                return False
            else:
                return True
        elif self.curr_loc_line_y in self.border.get('vertical'):
            return True
        else:
            return False

    def detect_previous_loc(self):
        if (self.curr_loc_line_x, self.curr_loc_line_y) in self.all_locations:
            return True
        else:
            return False

    def win_detection(self):
        if (self.curr_loc_line_x, self.curr_loc_line_y) in self.gate_player1:
            self.game_status = 21
        elif (self.curr_loc_line_x, self.curr_loc_line_y) in self.gate_player2:
            self.game_status = 11

    def defeat_detection(self):
        if not self.avl_player_moves_geo() and self.current_turn == 1:
            self.game_status = 22
        elif not self.avl_player_moves_geo() and self.current_turn == 2:
            self.game_status = 12

    def avl_player_moves_geo(self):
        return validate.field_status_possibilities(validate.location_possibilities(self.board, self.curr_loc_line_x, self.curr_loc_line_y))

    def avl_player_moves_cartesian(self):
        return validate.avl_cartesian_coordinate(self.curr_loc_line_x, self.curr_loc_line_y, self.avl_player_moves_geo())


class OngoingGame(Game):
    def __init__(self, game_id):
        game = model_handler.game_from_database(game_id)
        self.player1 = player.PlayerExisting(game.get("player1").get("name"),
                                             game.get("player1").get("amount_of_moves"),
                                             game.get("player1").get("all_moves"))
        self.player2 = player.PlayerExisting(game.get("player2").get("name"),
                                             game.get("player2").get("amount_of_moves"),
                                             game.get("player2").get("all_moves"))
        self.board = board.BoardOngoingGame(game.get("board").get('rows'),
                                            game.get("board").get('cols'),
                                            game.get("board").get('fields'))
        self.current_turn = game.get("current_turn")
        self.curr_loc_line_x = game.get("curr_loc_line_x")
        self.curr_loc_line_y = game.get("curr_loc_line_y")
        self.all_locations = game.get("all_locations")
        self.border = game.get("border")
        self.gate_player1 = game.get("gate_player1")
        self.gate_player2 = game.get("gate_player2")
        self.game_status = game.get("game_status")
        self.game_id = game_id

    def update_game(self):
        model_handler.update_game_database(self.game_id,
                                           self.player1,
                                           self.player2,
                                           self.board,
                                           self.current_turn,
                                           self.curr_loc_line_x,
                                           self.curr_loc_line_y,
                                           self.all_locations,
                                           self.border,
                                           self.gate_player1,
                                           self.gate_player2,
                                           self.game_status)