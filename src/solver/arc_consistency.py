import time
from csp import SudokuCSP
from collections import deque

class ArcConsistency:
    def __init__(self, csp: SudokuCSP):
        self.csp = csp  # why not copy deep?????

    ############################### don't forget to print the arc-consistency ##############################
    def ARC_3(self) -> bool:
        queue = deque()
        queue.extend(self.csp.constraints)
        while queue:
            X_i, X_j = queue.popleft()
            if self.revise(X_i, X_j):
                if len(self.csp.domains[X_i]) == 0:
                    return False
                for X_k in self.csp.constraints:
                    if X_k[0] == X_i and X_k[1] != X_j:  # revise this
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