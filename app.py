from flask import Flask, render_template
import copy
import sudoku

app = Flask(__name__)


@app.route("/")
def index():
    new_sudoku = sudoku.Sudoku()
    sudoku_puzzle = new_sudoku.generate_puzzle()  # generates sudoku puzzle with one unique solution
    sudoku_puzzle_copy = copy.deepcopy(sudoku_puzzle)  # copy the puzzle for front-end as it will be solved after
    sudoku_puzzle_solved = new_sudoku.solve_puzzle()  # solve puzzle
    return render_template("sudoku.html", sudoku_grid=sudoku_puzzle_copy, sudoku_tracking=new_sudoku.solved_path,
                           grid_solved=sudoku_puzzle_solved)


if __name__ == '__main__':
    app.run()
