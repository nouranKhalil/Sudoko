from csp import CSP

class Backtracking:
    def __init__(self, csp):
        self.csp = csp
    
    def backtrackingSearch(self):
        assignment = {}
        return self.backtrack(assignment)
    
    def backtrack(self, assignment):
        if len(assignment) == len(self.csp.variables):
            return assignment
        
        variable = self.selectUnassignedVariable(assignment)
        for value in self.orderDomainValues(variable, assignment):
            if self.csp.isConsistent(variable, value, assignment):
                assignment[variable] = value
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                del assignment[variable]
        return None
    
    def selectUnassignedVariable(self, assignment):
        unassigned = [variable for variable in self.csp.variables if variable not in assignment]
        return min(unassigned, key=lambda variable: len(self.csp.domains[variable]))
    
    def orderDomainValues(self, variable, assignment):
        return self.csp.domains[variable]
    
    

def createSudokuCsp(sudoku_grid):
    variables = [(i, j) for i in range(9) for j in range(9)]
    domains = {
        variable: set(range(1, 10)) if sudoku_grid[variable[0]][variable[1]] == 0
        else {sudoku_grid[variable[0]][variable[1]]}
        for variable in variables
    }
    constraints = {}

    def addConstraint(variable):
        constraints[variable] = set()
        # row constraints
        for i in range(9):
            if i != variable[0]:
                constraints[variable].add((i, variable[1]))
        # column constraints
        for j in range(9):
            if j != variable[1]:
                constraints[variable].add((variable[0], j))
        # 3x3 box constraints
        iOfBox, jOfBox = variable[0] // 3, variable[1] // 3
        for i in range(iOfBox * 3, (iOfBox + 1) * 3):
            for j in range(jOfBox * 3, (jOfBox + 1) * 3):
                if (i, j) != variable:
                    constraints[variable].add((i, j))

    for variable in variables:
        addConstraint(variable)
    return CSP(variables, domains, constraints)




# to check input validation
def isSolvable(sudoku_grid):
    csp = createSudokuCsp(sudoku_grid)
    solver = Backtracking(csp)
    solution = solver.backtrackingSearch()
    return solution is not None

# to check if the generated puzzle has a unique solution
def isSolvable_withUniqueSolution(sudoku_grid):
    csp = createSudokuCsp(sudoku_grid)
    solver = Backtracking(csp)

    def countSolutions(assignment, count=0):
        if len(assignment) == len(csp.variables):
            return count + 1

        variable = solver.selectUnassignedVariable(assignment)
        for value in solver.orderDomainValues(variable, assignment):
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



# if __name__ == "__main__":
#     sudoku_grid = [
# [0, 0, 0, 0, 5, 1, 0, 0, 0],
# [9, 0, 6, 0, 0, 0, 0, 0, 0],
# [0, 0, 5, 0, 4, 0, 2, 0, 0],
# [3, 0, 9, 1, 0, 0, 0, 0, 8],
# [0, 0, 0, 0, 0, 5, 0, 0, 0],
# [0, 1, 0, 7, 3, 0, 0, 9, 0],
# [0, 0, 0, 0, 0, 0, 4, 0, 7],
# [0, 3, 4, 2, 7, 0, 0, 0, 0],
# [0, 0, 2, 0, 0, 0, 0, 0, 0]
#     ]

#     print("does the puzzle have unique solution?", isSolvable_withUniqueSolution(sudoku_grid))
#     sudoku_csp = createSudokuCsp(sudoku_grid)
#     solution = Backtracking(sudoku_csp).backtrackingSearch()

#     if solution:
#         for i in range(9):
#             print([solution[(i, j)] for j in range(9)])
#     else:
#         print("No solution found.")