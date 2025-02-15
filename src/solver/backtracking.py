from src.solver.csp import SudokuCSP
from src.solver.arc_consistency import ArcConsistency
import numpy as np
import copy

class Backtracking:
    def __init__(self, csp: SudokuCSP):
        self.csp = csp

    def backtrackingSearch(self):
        assignment = {}
        arc_consistency = ArcConsistency(self.csp)
        old_domains = copy.deepcopy(self.csp.domains)
        if arc_consistency.ARC_3():
            if self.csp.domains != old_domains:
                print("Updated domains:")
                self.csp.print_domains()
            return self.backtrack(assignment, arc_consistency)
        return None

    def backtrack(self, assignment, arc_consistency : ArcConsistency):
        if len(assignment) == len(self.csp.variables):
            return assignment
        
        variable = self.selectUnassignedVariable(assignment)
        for value in self.orderDomainValues(variable,assignment):
            if self.csp.isConsistent(variable, value, assignment):
                assignment[variable] = value
                old_domains = copy.deepcopy(self.csp.domains)
                arc_consistency.csp.domains[variable] = {value}
                if arc_consistency.ARC_3():
                    if self.csp.domains != old_domains:
                        print("Updated domains:")
                        self.csp.print_domains()
                    result = self.backtrack(assignment, arc_consistency)
                    if result is not None:
                        return result
                arc_consistency.csp.domains = old_domains.copy()
                del assignment[variable]
        return None

# MRV 
    def selectUnassignedVariable(self, assignment):
        # choose the variable with the fewest remaining values
        unassigned = [
            variable for variable in self.csp.variables if variable not in assignment
        ]
        return min(unassigned, key=lambda variable: len(self.csp.domains[variable]))

    # LCV
    def orderDomainValues(self, variable, assignment):
        # count the number of constraints that would be violated by each value
        def countConstraints(value):
            count = 0
            if variable in self.csp.constraints:
                for neighbor in self.csp.constraints[variable]:
                    if neighbor not in assignment:
                        # count the number of values that would be invalid for the neighbor
                        count += sum(
                            1 for neighbor_value in self.csp.domains[neighbor]
                            if not self.csp.isConsistent(neighbor, neighbor_value, {**assignment, variable: value})
                        )
            return count
        return sorted(self.csp.domains[variable], key=countConstraints)



# to validate input sudoku grid
def isSolvable(sudoku_grid):
    csp = SudokuCSP(sudoku_grid)
    solver = Backtracking(csp)
    solution = solver.backtrackingSearch()
    return solution is not None


# to check if the generated puzzle has a unique solution
def isSolvable_withUniqueSolution(sudoku_grid):
    csp = SudokuCSP(sudoku_grid)
    solver = Backtracking(csp)

    def countSolutions(assignment, count=0):
        if len(assignment) == len(csp.variables):
            return count + 1

        variable = solver.selectUnassignedVariable(assignment)
        for value in solver.orderDomainValues(variable):
            if csp.isConsistent(variable, value, assignment):
                assignment[variable] = value
                count = countSolutions(assignment, count)
                if count > 1:
                    return count
                del assignment[variable]
        return count
    
    count = countSolutions({})
    if count == 1:
        return count, True
    return count, False


if __name__ == "__main__":
    sudoku_grid = np.array(
        [
            [0, 0, 0, 0, 5, 1, 0, 0, 0],
            [9, 0, 6, 0, 0, 0, 0, 0, 0],
            [0, 0, 5, 0, 4, 0, 2, 0, 0],
            [3, 0, 9, 1, 0, 0, 0, 0, 8],
            [0, 0, 0, 0, 0, 5, 0, 0, 0],
            [0, 1, 0, 7, 3, 0, 0, 9, 0],
            [0, 0, 0, 0, 0, 0, 4, 0, 7],
            [0, 3, 4, 2, 7, 0, 0, 0, 0],
            [0, 0, 2, 0, 0, 0, 0, 0, 0],
        ]
    )

    print(
        "does the puzzle have unique solution?",
        isSolvable_withUniqueSolution(sudoku_grid),
    )
    sudoku_csp = SudokuCSP(sudoku_grid)
    solution = Backtracking(sudoku_csp).backtrackingSearch()

    if solution:
        for i in range(9):
            print([solution[(i, j)] for j in range(9)])
    else:
        print("No solution found.")
