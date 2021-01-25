import copy
from random import shuffle


class Sudoku:

    def __init__(self):
        self.grid = [[0 for i in range(9)] for j in range(9)]
        self.solved_path = []

    @staticmethod
    def find_empty(grid):
        # Return empty row and col (or None if there is no empty one)
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    return row, col
        return None, None

    @staticmethod
    def is_valid(row, col, num, grid):
        # Check if number has been use in either row, column or 3x3 grid (subgrid)

        # checking if number is used in a row
        if num in grid[row]:
            return False

        # check if number is used in a column
        for r in range(9):
            if grid[r][col] == num:
                return False

        # check if number is used in 3x3 square (subgrid)
        first_row = (row // 3) * 3  # First row of the subgrid
        first_col = (col // 3) * 3  # First column of the subgrid
        for r in range(first_row, first_row + 3):
            for c in range(first_col, first_col + 3):
                if grid[r][c] == num:
                    return False

        return True

    def sudoku_grid_action(self, grid, action=None, sudoku_numbers_count=None):
        # Main solving method
        # this method is used both for generating sudoku grid and solving it, depends on action argument

        sudoku_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        # base case for recursion
        row, col = self.find_empty(grid)
        if row is None:  # If there is no empty squares, then it means that sudoku is solved
            # if we are checking how many solutions there are when generating grid (must be one unique solution)
            # return grid to compare solution to originally solved grid
            if action == "CHECK":
                return grid
            return True

        # if program is generating sudoku grid, shuffle sudoku numbers so we don't get the same grid everytime
        if action == "GENERATE":
            shuffle(sudoku_numbers)
            num_list = sudoku_numbers
        # if program is solving the puzzle, use sudoku numbers 1-9 sequentially
        elif action == "INSERT":
            num_list = sudoku_numbers
        # if program is checking number of possible solutions, list that has been passed in as argument for the method
        else:
            num_list = sudoku_numbers_count

        for number in num_list:
            # if program is solving puzzle, record attempt the attempt to input the number to the grid
            if action == "INSERT":
                self.solved_path.append(["ATTEMPT", row, col, number])
            if self.is_valid(row, col, number, grid):
                grid[row][col] = number
                # if program is solving puzzle, record successful number input
                if action == "INSERT":
                    self.solved_path.append(["INSERT", row, col, number])
                # continue solving puzzle recursively
                if self.sudoku_grid_action(grid, action, sudoku_numbers_count):
                    return grid
            # if program is solving puzzle, record the reset of the current number
            if action == "INSERT":
                self.solved_path.append(["DELETE", row, col, number])
            grid[row][col] = 0  # reset guess if none values are valid (1-9)
        return False

    def get_solutions(self, grid, full_grid):
        # Return boolean value which will determine whether there is more than one solution after the number was removed
        sudoku_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # number of possible solutions (for valid sudoku should be one)
        for i in range(len(sudoku_numbers)):
            solved_grid = self.sudoku_grid_action(grid, "CHECK", sudoku_numbers)
            if solved_grid != full_grid:  # Check if solved grid is equals to the original one (must be one solution)
                return False
            sudoku_numbers.append(sudoku_numbers.pop(0))  # Add first sudoku number to the end to try more combinations
        return True

    def get_squares(self):
        # Return a list of occupied squares on the whole sudoku grid
        return [(row, col) for row in range(9) for col in range(9) if self.grid[row][col] != 0]

    def remove_numbers_grid(self):
        # Remove numbers from full valid grid to generate sudoku puzzle

        taken_squares = self.get_squares()  # Get squares that are occupied
        shuffle(taken_squares)  # Shuffle occupied squares to select random squares
        taken_squares_count = len(taken_squares)

        # Attempt count to find unique solutions, the greater attempt count the more difficult sudoku will be
        # Code will run longer to find unique solution with less clues
        attempt_count = 3

        # Copy of the original grid used for comparison to make sure there is one unique solution
        full_grid = copy.deepcopy(self.grid)

        # 17 is the minimum number of clues which leads to a unique solution
        while attempt_count > 0 and taken_squares_count >= 17:
            row, col = taken_squares.pop()  # get row and column that will be deleted from grid
            taken_squares_count -= 1  # decrement number of occupied squares on the grid
            deleted_square = self.grid[row][col]  # memorise deleted square for back-tracking
            self.grid[row][col] = 0
            grid_copy = copy.deepcopy(self.grid)
            if not self.get_solutions(grid_copy,
                                      full_grid):  # If there is more than one solution, means sudoku is not valid
                self.grid[row][col] = deleted_square  # restore deleted value to the grid
                taken_squares_count += 1  # Increment occupied squares
                attempt_count -= 1  # Allow less tries to generate grid
        return

    def generate_puzzle(self):
        self.sudoku_grid_action(self.grid, "GENERATE")
        self.remove_numbers_grid()
        return self.grid

    def solve_puzzle(self):
        self.sudoku_grid_action(self.grid, "INSERT")
        return self.grid

