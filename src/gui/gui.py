from src.solver.csp import SudokuCSP
from src.solver.sudoku_generator import SudokuGenerator
from src.solver.backtracking import Backtracking


class GUI:
    def __init__(self):
        pass

    def TestImport(self):
        difficulty = "hard"
        puzzle = SudokuGenerator.generate_sudoku_puzzle(difficulty)
        SudokuGenerator.print_board(puzzle)