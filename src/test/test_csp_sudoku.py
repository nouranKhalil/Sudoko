import unittest
from src.solver.csp import SudokuCSP
import numpy as np


class TestSudokuCSP(unittest.TestCase):
    def test_udpate_domain(self):
        # lecture's example
        sudoku_grid_1 = np.array(
            [
                [8, 0, 9, 5, 0, 1, 7, 3, 6],
                [2, 0, 7, 0, 6, 3, 0, 0, 0],
                [1, 6, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 9, 0, 4, 0, 7],
                [0, 9, 0, 3, 0, 7, 0, 2, 0],
                [7, 0, 6, 0, 8, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 6, 3],
                [0, 0, 0, 9, 3, 0, 5, 0, 2],
                [5, 3, 2, 6, 0, 4, 8, 0, 9],
            ]
        )

        CSP_1 = SudokuCSP(sudoku_grid_1)
        sudoku_grid_2 = np.array([
            [1, 0, 0, 5, 0, 0, 6, 0, 0],
            [0, 2, 0, 7, 0, 0, 0, 0, 0],
            [0, 0, 8, 0, 2, 6, 0, 0, 3],
            [9, 0, 0, 0, 0, 0, 0, 0, 8],
            [0, 0, 0, 6, 0, 0, 0, 0, 0],
            [0, 5, 0, 0, 4, 1, 3, 0, 0],
            [0, 0, 5, 0, 0, 0, 0, 4, 0],
            [0, 4, 0, 0, 3, 2, 1, 0, 0],
            [0, 0, 0, 0, 7, 0, 0, 0, 0],
        ])
        CSP_2 = SudokuCSP(sudoku_grid_2)
        CSP_2.update_domains(sudoku_grid_1)
        self.assertEqual(CSP_1.domains, CSP_2.domains)


if __name__ == "__main__":
    unittest.main()
