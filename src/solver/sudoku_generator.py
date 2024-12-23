import random
import numpy as np
from csp import SudokuCSP
from backtracking import Backtracking

class SudokuGenerator:

    @staticmethod
    def is_valid(board, row, col, num):
        '''      
        check if placing num at row and col is valid based on suduko rules
        ensure no conflicts in the row and column and subgrid before placing a number
        '''
        # checking the row
        if num in board[row]:
            return False
        # checking the col
        if num in board[:,col]:
            return False
        # Check 3x3 subgrid
        start_row, start_col = 3*(row // 3), 3*(col // 3)
        if num in board[start_row:start_row+3, start_col:start_col+3]:
            return False
        return True

    @staticmethod
    def solve(board):
        '''
        solves the sudoku board using backtracking
        and uses backtracking algorithm to fill in the sudoku grid based on constraints
        '''
        csp = SudokuCSP(board)
        solver = Backtracking(csp)
        solution = solver.backtrackingSearch()

        if solution:
            for i in range(9):
                for j in range(9):
                    board[i,j] = solution.get((i,j), 0)
            return True
        return False

    @staticmethod
    def generate_sudoku():
        '''
        generates a completed Sudoku board using a backtracking algorithm
        '''
        board = np.zeros((9, 9), dtype=int)

        def fill_board(board):
            for row in range(9):
                for col in range(9):
                    if board[row, col] == 0:
                        random_nums = list(range(1, 10))
                        random.shuffle(random_nums)
                        for num in random_nums:
                            if SudokuGenerator.is_valid(board, row, col, num):
                                board[row, col] = num
                                if fill_board(board):
                                    return True
                                board[row, col] = 0
                        return False
            return True

        fill_board(board)
        return board

    @staticmethod
    def remove_clues(board, difficulty):
        '''
        remove clues from the board based on the difficulty level
        '''
        if difficulty == "easy":
            clues_to_remove = 36
        elif difficulty == "medium":
            clues_to_remove = 45
        elif difficulty == "hard":
            clues_to_remove = 53

        while clues_to_remove > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if board[row, col] != 0:
                board[row, col] = 0
                clues_to_remove -= 1

        return board

    @staticmethod
    def has_unique_solution(board):
        '''
        checks if the Sudoku board has a unique solution by solving it
        '''
        count = [0]

        def solve_with_check(board):
            for row in range(9):
                for col in range(9):
                    if board[row, col] == 0:
                        for num in range(1, 10):
                            if SudokuGenerator.is_valid(board, row, col, num):
                                board[row, col] = num
                                solve_with_check(board)
                                board[row, col] = 0
                        return
            count[0] += 1  

        solve_with_check(board)
        return count[0] == 1  

    @staticmethod
    def generate_sudoku_puzzle(difficulty="medium"):
        '''
        generates sudoku puzzle with a unique solution by first creating a solved board and then removing clues
        ensures that the generated puzzle has exactly one solution making it solvable
        '''
        board = SudokuGenerator.generate_sudoku()
        puzzle = SudokuGenerator.remove_clues(board,difficulty)

        while not SudokuGenerator.has_unique_solution(puzzle):
            puzzle = SudokuGenerator.remove_clues(SudokuGenerator.generate_sudoku(),difficulty)

        return puzzle

    @staticmethod
    def print_board(board):
        for row in range(9):
            print(" ".join(str(board[row, col]) if board[row, col] != 0 else '.' for col in range(9)))


difficulty = "easy"  
puzzle = SudokuGenerator.generate_sudoku_puzzle(difficulty)
SudokuGenerator.print_board(puzzle)
