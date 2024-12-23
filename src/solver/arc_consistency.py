import time
from csp import SudokuCSP
from collections import deque
import copy

class ArcConsistency:
    def __init__(self, csp: SudokuCSP):
        self.csp = csp

    def ARC_3(self) -> bool:
        queue = deque()
        queue.extend(self.csp.constraints)
        while queue:
            X_i, X_j = queue.popleft()
            if self.revise(X_i, X_j):
                if len(self.csp.domains[X_i]) == 0:
                    return False
                for X_k in self.csp.dict_constraints[X_i]:
                    if X_k != X_j:
                        queue.append((X_k, X_i))
        return True

    def revise(self, X_i: tuple, X_j: tuple) -> bool:
        revised = False
        to_remove = []
        for x in self.csp.domains[X_i]:
            if all(x == y for y in self.csp.domains[X_j]):
                to_remove.append(x)
                revised = True
        for x in to_remove:
            self.csp.domains[X_i].remove(x)
        return revised
