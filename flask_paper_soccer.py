from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import game

app = Flask('paper soccer')

@app.route("/")
def main_screen():
    return render_template('main_screen.html')

@app.route("/new_game", methods=['POST', 'GET'])
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

@app.route("/load_game")
def load_game():
    return render_template('load_game.html')

@app.route("/game/<game_id>")
def ongoing_game(game_id):
    current_game = game.OngoingGame(str(game_id))
    return render_template('ongoing_game.html',
                           game_id=current_game.game_id,
                           player1_name=current_game.player1.name,
                           player2_name=current_game.player2.name)
