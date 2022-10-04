from pymongo import MongoClient
from bson import ObjectId

CONNECTION_STRING = 'mongodb://localhost:27017'
client = MongoClient(CONNECTION_STRING)

game_db = client.paper_soccer_db.games

class ModelHandler():
    def __init__(self, db):
        self.database = db

    @staticmethod
    def board_to_database(board):
        fields = [dict(row=val.row, col=val.col, status=val.status) for key, val in board.fields.items()]
        return {"rows": board.rows, "cols": board.cols, "fields": fields}

    @staticmethod
    def player_to_database(player):
        return dict(name=player.name, amount_of_moves=player.amount_of_moves, all_moves=player.all_moves)

    def game_to_database(self, player1, player2, board, current_turn, curr_loc_line_x, curr_loc_line_y,
                         all_locations, border, gate_player1, gate_player2, game_status):

        game_id = self.database.insert_one({"player1": self.player_to_database(player1),
                                            "player2": self.player_to_database(player2),
                                            "board": self.board_to_database(board),
                                            "current_turn": current_turn,
                                            "curr_loc_line_x": curr_loc_line_x,
                                            "curr_loc_line_y": curr_loc_line_y,
                                            "all_locations": all_locations,
                                            "border": border,
                                            "gate_player1": gate_player1,
                                            "gate_player2": gate_player2,
                                            "game_status": game_status})

        return game_id

    def update_game_database(self, current_game_id, player1, player2, board, current_turn, curr_loc_line_x, curr_loc_line_y,
                             all_locations, border, gate_player1, gate_player2, game_status):
        game_id = ObjectId(current_game_id)
        field_updates = {
            "$set": {"player1": self.player_to_database(player1),
                     "player2": self.player_to_database(player2),
                     "board": self.board_to_database(board),
                     "current_turn": current_turn,
                     "curr_loc_line_x": curr_loc_line_x,
                     "curr_loc_line_y": curr_loc_line_y,
                     "all_locations": all_locations,
                     "border": border,
                     "gate_player1": gate_player1,
                     "gate_player2": gate_player2,
                     "game_status": game_status}
        }
        self.database.update_one({"_id": game_id}, field_updates)


    def game_from_database(self, game_id):
        return self.database.find_one({"_id": game_id})
