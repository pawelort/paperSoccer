from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import game

app = Flask('paper soccer')

# temporary visualisation auxiliary parameters

temp_visu_px_res = 30
temp_visu_px_offset_x = 0
temp_visu_px_offset_y = 15

@app.route("/")
def main_screen():
    return render_template('main_screen.html')

@app.route("/new_game", methods=["POST", "GET"])
def new_game():
    if request.method == "POST":
        game_param = (request.form.get('pl1_name'),
                      request.form.get('pl2_name'),
                      int(request.form.get('board_rows')),
                      int(request.form.get('board_cols')))
        paper_soccer = game.Game(*game_param)
        return redirect(url_for('ongoing_game', game_id=paper_soccer.game_id))
    else:
        return render_template('new_game.html')

@app.route("/load_game", methods=["POST", "GET"])
def load_game():
    if request.method == "GET":
        return render_template('load_game.html')
    else:
        return redirect(url_for('ongoing_game', game_id=request.form.get('game_no')))

@app.route("/game_finished/<game_id>")
def game_finished(game_id):
    current_game = game.OngoingGame(game_id)
    return render_template('game_finished.html', game=current_game,
                           pixel_res=temp_visu_px_res,
                           offset_x=temp_visu_px_offset_x,
                           offset_y=temp_visu_px_offset_y)

@app.route("/game/<game_id>", methods=["POST", "GET"])
def ongoing_game(game_id):
    current_game = game.OngoingGame(game_id)
    if request.method == "GET":
        if current_game.game_status == 1:
            cartesian_moves = current_game.avl_player_moves_cartesian()
            return render_template('ongoing_game.html', game=current_game,
                                   avl_moves=cartesian_moves,
                                   pixel_res=temp_visu_px_res,
                                   offset_x=temp_visu_px_offset_x,
                                   offset_y=temp_visu_px_offset_y)
        else:
            return redirect(url_for('game_finished', game_id=current_game.game_id))
    else:
        move_request = request.form.get('sel_move')
        if move_request == None:
            move_selected = current_game.avl_player_moves_cartesian()[0]
        else:
            move_selected = tuple(map(int, move_request[1:-1].split(',')))
        current_game.move(*move_selected)
        current_game.update_game()
        if current_game.game_status == 1:
            return redirect(url_for('ongoing_game', game_id=current_game.game_id))
        else:
            return redirect(url_for('game_finished', game_id=current_game.game_id))