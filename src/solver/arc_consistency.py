from csp import SudokuCSP
from collections import deque

class ArcConsistency:
    def __init__(self, csp: SudokuCSP):
        self.csp = csp

    def testImport(self):
        print(self.csp.variables)

    def ARC_3(self) -> bool:
        queue = deque()
        queue.extend(self.csp.constraints)
        while queue:
            X_i, X_j = queue.popleft()
            if self.revise(X_i, X_j):
                if len(self.csp.domains[X_i]) == 0:
                    return False
                for X_k in self.csp.constraints:
                    if X_k[0] == X_i and X_k[1] != X_j:
                        queue.append(X_k)
        return True

    def revise(self, X_i: tuple, X_j: tuple) -> bool:
        revised = False
        to_remove = []
        for x in self.csp.domains[X_i]:
            if not any(y != x for y in self.csp.domains[X_j]):
                to_remove.append(x)
                revised = True
        for x in to_remove:
            self.csp.domains[X_i].remove(x)
        return revised


sudoku = SudokuCSP()

sudoku.print_domains()
sudoku_grid = [
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
sudoku.update_domains(sudoku_grid)
print("after update")
sudoku.print_domains()

arc_consistency = ArcConsistency(sudoku)


arc_consistency.ARC_3()
print("after arc consistency")
arc_consistency.csp.print_domains()
