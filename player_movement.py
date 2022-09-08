'''
module for all player handling
please note, that player moves based on lines 0 based, which are located between fields
'''
class Player():
    def __init__(self, name):
        self.name = name
        self.amount_of_moves = 0
        self.all_moves = []

    def player_move(self, row, col, direction):
        self.amount_of_moves += 1
        self.all_moves.append((row, col, direction))


