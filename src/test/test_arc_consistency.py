import unittest
import numpy as np
from src.solver.csp import SudokuCSP
from src.solver.backtracking import Backtracking
import time

"""This script tests the Sudoku solver using the Backtracking algorithm.
    to run the script, run the following command:
    python -m unittest src.test.test_sudoku_solver.py """


def test_sudoku_solver(sudoku_grid, expected_solution, level):
    print(f"Testing Sudoku solver for level: {level}")
    sudoku_csp = SudokuCSP(sudoku_grid)
    start = time.time()
    solution = Backtracking(sudoku_csp).backtrackingSearch()
    end = time.time()

    print(f"Time taken: {end - start:.2f} sec")

    if solution:
        solved_grid = np.zeros((9, 9), dtype=int)
        for (i, j), value in solution.items():
            solved_grid[i, j] = value

        print("Solution:")
        for row in solved_grid:
            print(row)

        if np.array_equal(solved_grid, expected_solution):
            print("Test passed!")
        else:
            print("Test failed!")
    else:
        print("No solution found.")
    print("\n")


class TestSudokuSolver(unittest.TestCase):
    # Level: easy
    # time: 0.21 sec
    def test_easy(self):
        sudoku_grid_easy = np.array(
            [
                [0, 0, 1, 0, 3, 4, 0, 0, 6],
                [0, 4, 0, 0, 0, 2, 5, 8, 0],
                [0, 5, 0, 1, 8, 0, 0, 4, 0],
                [1, 3, 2, 0, 4, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 6, 0, 0, 0],
                [7, 6, 4, 8, 5, 0, 0, 2, 0],
                [0, 0, 0, 3, 9, 1, 0, 5, 8],
                [9, 1, 0, 7, 0, 8, 4, 0, 0],
                [6, 0, 0, 4, 2, 0, 0, 0, 7],
            ]
        )
        expected_solution_easy = np.array(
            [
                [8, 7, 1, 5, 3, 4, 2, 9, 6],
                [3, 4, 9, 6, 7, 2, 5, 8, 1],
                [2, 5, 6, 1, 8, 9, 7, 4, 3],
                [1, 3, 2, 9, 4, 7, 8, 6, 5],
                [5, 9, 8, 2, 1, 6, 3, 7, 4],
                [7, 6, 4, 8, 5, 3, 1, 2, 9],
                [4, 2, 7, 3, 9, 1, 6, 5, 8],
                [9, 1, 5, 7, 6, 8, 4, 3, 2],
                [6, 8, 3, 4, 2, 5, 9, 1, 7],
            ]
        )
        test_sudoku_solver(sudoku_grid_easy, expected_solution_easy, "easy")

    # Level: medium
    # time: 0.31 sec
    def test_medium(self):
        sudoku_grid_medium = np.array(
            [
                [6, 0, 0, 0, 3, 0, 0, 4, 8],
                [0, 1, 0, 9, 0, 0, 0, 0, 0],
                [0, 0, 0, 2, 6, 0, 9, 0, 5],
                [1, 8, 6, 7, 0, 4, 3, 0, 9],
                [0, 2, 0, 8, 0, 5, 0, 0, 0],
                [5, 0, 9, 6, 0, 3, 2, 0, 7],
                [0, 0, 0, 0, 8, 0, 4, 0, 0],
                [0, 3, 1, 0, 0, 0, 0, 9, 2],
                [9, 0, 4, 3, 0, 0, 0, 0, 0],
            ]
        )
        expected_solution_medium = np.array(
            [
                [6, 9, 2, 5, 3, 7, 1, 4, 8],
                [3, 1, 5, 9, 4, 8, 7, 2, 6],
                [4, 7, 8, 2, 6, 1, 9, 3, 5],
                [1, 8, 6, 7, 2, 4, 3, 5, 9],
                [7, 2, 3, 8, 9, 5, 6, 1, 4],
                [5, 4, 9, 6, 1, 3, 2, 8, 7],
                [2, 5, 7, 1, 8, 9, 4, 6, 3],
                [8, 3, 1, 4, 7, 6, 5, 9, 2],
                [9, 6, 4, 3, 5, 2, 8, 7, 1],
            ]
        )
        test_sudoku_solver(sudoku_grid_medium, expected_solution_medium, "medium")

    # Level: hard
    # time: 0.31 sec
    def test_hard(self):
        sudoku_grid_hard = np.array(
            [
                [0, 0, 0, 0, 0, 8, 0, 6, 0],
                [9, 4, 0, 0, 7, 0, 1, 0, 0],
                [6, 0, 0, 0, 0, 0, 7, 8, 0],
                [8, 0, 3, 0, 5, 1, 0, 4, 9],
                [0, 0, 0, 0, 9, 0, 0, 2, 1],
                [1, 6, 9, 4, 0, 0, 3, 0, 0],
                [0, 0, 0, 5, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 3, 7],
                [4, 9, 2, 0, 0, 0, 0, 0, 0],
            ]
        )
        expected_solution_hard = np.array(
            [
                [2, 7, 5, 1, 3, 8, 9, 6, 4],
                [9, 4, 8, 2, 7, 6, 1, 5, 3],
                [6, 3, 1, 9, 4, 5, 7, 8, 2],
                [8, 2, 3, 7, 5, 1, 6, 4, 9],
                [7, 5, 4, 6, 9, 3, 8, 2, 1],
                [1, 6, 9, 4, 8, 2, 3, 7, 5],
                [3, 8, 7, 5, 1, 4, 2, 9, 6],
                [5, 1, 6, 8, 2, 9, 4, 3, 7],
                [4, 9, 2, 3, 6, 7, 5, 1, 8],
            ]
        )
        test_sudoku_solver(sudoku_grid_hard, expected_solution_hard, "hard")

    # Level: master
    # time: 0.43 sec
    def test_master(self):
        sudoku_grid_master = np.array(
            [
                [1, 0, 0, 5, 0, 0, 6, 0, 0],
                [0, 2, 0, 7, 0, 0, 0, 0, 0],
                [0, 0, 8, 0, 2, 6, 0, 0, 3],
                [9, 0, 0, 0, 0, 0, 0, 0, 8],
                [0, 0, 0, 6, 0, 0, 0, 0, 0],
                [0, 5, 0, 0, 4, 1, 3, 0, 0],
                [0, 0, 5, 0, 0, 0, 0, 4, 0],
                [0, 4, 0, 0, 3, 2, 1, 0, 0],
                [0, 0, 0, 0, 7, 0, 0, 0, 0],
            ]
        )
        expected_solution_master = np.array(
            [
                [1, 9, 3, 5, 8, 4, 6, 7, 2],
                [5, 2, 6, 7, 1, 3, 9, 8, 4],
                [4, 7, 8, 9, 2, 6, 5, 1, 3],
                [9, 6, 1, 3, 5, 7, 4, 2, 8],
                [2, 3, 4, 6, 9, 8, 7, 5, 1],
                [8, 5, 7, 2, 4, 1, 3, 9, 6],
                [3, 8, 5, 1, 6, 9, 2, 4, 7],
                [7, 4, 9, 8, 3, 2, 1, 6, 5],
                [6, 1, 2, 4, 7, 5, 8, 3, 9],
            ]
        )
        test_sudoku_solver(sudoku_grid_master, expected_solution_master, "master")

    # Level: extreme
    # time: 1.27 sec
    def test_extreme_1(self):
        sudoku_grid_extreme = np.array(
            [
                [6, 0, 8, 0, 0, 0, 0, 0, 0],
                [0, 4, 0, 1, 0, 0, 5, 0, 0],
                [0, 0, 1, 0, 0, 6, 9, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 2, 0, 0, 9, 0],
                [0, 3, 0, 4, 0, 0, 7, 0, 0],
                [0, 0, 0, 6, 0, 0, 0, 8, 0],
                [3, 8, 0, 0, 0, 4, 0, 2, 0],
                [0, 9, 0, 7, 0, 0, 0, 3, 0],
            ]
        )
        expected_solution_extreme = np.array(
            [
                [6, 7, 8, 2, 9, 5, 3, 1, 4],
                [9, 4, 3, 1, 7, 8, 5, 6, 2],
                [2, 5, 1, 3, 4, 6, 9, 7, 8],
                [5, 6, 9, 8, 1, 7, 2, 4, 3],
                [4, 1, 7, 5, 2, 3, 8, 9, 6],
                [8, 3, 2, 4, 6, 9, 7, 5, 1],
                [7, 2, 5, 6, 3, 1, 4, 8, 9],
                [3, 8, 6, 9, 5, 4, 1, 2, 7],
                [1, 9, 4, 7, 8, 2, 6, 3, 5],
            ]
        )
        test_sudoku_solver(sudoku_grid_extreme, expected_solution_extreme, "extreme")

    # Level: extreme
    # time: 0.35 sec
    def test_extreme_2(self):
        sudoku_grid_extreme = np.array(
            [
                [8, 2, 0, 5, 0, 0, 3, 6, 0],
                [0, 0, 0, 0, 0, 9, 0, 5, 0],
                [7, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 6, 0, 0, 0, 0, 0, 0],
                [5, 3, 0, 9, 0, 0, 8, 0, 0],
                [0, 0, 0, 0, 4, 0, 0, 0, 1],
                [0, 0, 7, 2, 0, 0, 0, 0, 0],
                [2, 6, 0, 0, 0, 1, 0, 0, 8],
                [0, 0, 9, 0, 0, 0, 6, 0, 0],
            ]
        )
        expected_solution_extreme = np.array(
            [
                [8, 2, 1, 5, 7, 4, 3, 6, 9],
                [6, 4, 3, 1, 8, 9, 2, 5, 7],
                [7, 9, 5, 3, 6, 2, 1, 8, 4],
                [4, 1, 6, 8, 2, 5, 7, 9, 3],
                [5, 3, 2, 9, 1, 7, 8, 4, 6],
                [9, 7, 8, 6, 4, 3, 5, 2, 1],
                [3, 8, 7, 2, 9, 6, 4, 1, 5],
                [2, 6, 4, 7, 5, 1, 9, 3, 8],
                [1, 5, 9, 4, 3, 8, 6, 7, 2],
            ]
        )

        test_sudoku_solver(sudoku_grid_extreme, expected_solution_extreme, "extreme")

    # Level: hardest sudoku in the world
    # time: 15.19 sec
    def test_insane(self):
        sudoku_grid_insane = np.array(
            [
                [8, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 3, 6, 0, 0, 0, 0, 0],
                [0, 7, 0, 0, 9, 0, 2, 0, 0],
                [0, 5, 0, 0, 0, 7, 0, 0, 0],
                [0, 0, 0, 0, 4, 5, 7, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 3, 0],
                [0, 0, 1, 0, 0, 0, 0, 6, 8],
                [0, 0, 8, 5, 0, 0, 0, 1, 0],
                [0, 9, 0, 0, 0, 0, 4, 0, 0],
            ]
        )
        expected_solution_insane = np.array(
            [
                [8, 1, 2, 7, 5, 3, 6, 4, 9],
                [9, 4, 3, 6, 8, 2, 1, 7, 5],
                [6, 7, 5, 4, 9, 1, 2, 8, 3],
                [1, 5, 4, 2, 3, 7, 8, 9, 6],
                [3, 6, 9, 8, 4, 5, 7, 2, 1],
                [2, 8, 7, 1, 6, 9, 5, 3, 4],
                [5, 2, 1, 9, 7, 4, 3, 6, 8],
                [4, 3, 8, 5, 2, 6, 9, 1, 7],
                [7, 9, 6, 3, 1, 8, 4, 5, 2],
            ]
        )
        test_sudoku_solver(sudoku_grid_insane, expected_solution_insane, "insane")


if __name__ == "__main__":
    unittest.main()
