'''
module for all playable demo
menus and main loop created for demo purpose
'''

import game
import pprint as pp

class Menu():
    def __init__(self):
        self.menu_lvl = 0
        self.exit_game = False

    def main_menu(self):
        if demo_game.current_turn == 1:
            print(f"{demo_game.player1.name} turn")
        else:
            print(f"{demo_game.player2.name} turn")

        print("==============")
        print("Please select, what You want to do:")
        print("1. Make a move")
        print("2. See available moves (map oriented)")
        print("3. See available moves (cartesian coordinate)")
        print("4. See all moves done by current player")
        print("5. See all visited location")
        print("9. Exit game")
        try:
            choice = int(input())
            if choice == 1:
                self.menu_lvl = 1
            elif choice == 2:
                print(demo_game.avl_player_moves_geo())
            elif choice == 3:
                print(demo_game.avl_player_moves_cartesian())
            elif choice == 4:
                if demo_game.current_turn == 1:
                    pp.pp(demo_game.player1.all_moves)
                else:
                    pp.pp(demo_game.player2.all_moves)
            elif choice == 5:
                pp.pp(demo_game.all_locations)
            elif choice == 9:
                self.exit_game = True
            else:
                print("undefined command")

        except ValueError:
            print("please type integers as menu selection")
            self.display_menu()

    def move_menu(self):
        if demo_game.current_turn == 1:
            print(f"{demo_game.player1.name} turn")
        else:
            print(f"{demo_game.player2.name} turn")

        print("==============")
        print(f"Please give coordinates (line_x line_y) or press 9 to return to main menu")

        choice = input().split()
        if len(choice) == 1 and choice[0] == '9':
            self.menu_lvl = 0
        elif len(choice) == 2:
            try:
                req_line_x = int(choice[0])
                req_line_y = int(choice[1])

                if demo_game.move(req_line_x, req_line_y):
                    print("move successfully executed")
                    self.end_game()
                    self.menu_lvl = 0
                else:
                    print("not possible to move, try again")
            except ValueError:
                print("please type integers as coordinates")
        else:
            print("undefined command")

    def end_game(self):
        if demo_game.game_status == 11:
            print('Congratulations, player1 scores and wins the game!')
            self.exit_game = True
        elif demo_game.game_status == 21:
            print('Congratulations, player2 scores and wins the game!')
            self.exit_game = True
        elif demo_game.game_status == 12:
            print('Player1 wins! Player2 has no possible movement')
            self.exit_game = True
        elif demo_game.game_status == 22:
            print('Player2 wins! Player1 has no possible movement')
            self.exit_game = True

    def display_menu(self):
        if self.menu_lvl == 0:
            self.main_menu()
        elif self.menu_lvl == 1:
            self.move_menu()

demo_game = game.Game.game_standard_size('Player1', 'Player2')
menu = Menu()

while not menu.exit_game:
    menu.display_menu()
