class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
    
    def backtrackingSearch(self):
        assignment = {}
        return self.backtrack(assignment)
    
    def backtrack(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment
        
        variable = self.selectUnassignedVariable(assignment)
        for value in self.orderDomainValues(variable, assignment):
            if self.isConsistent(variable, value, assignment):
                assignment[variable] = value
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                del assignment[variable]
        return None
    
    def selectUnassignedVariable(self, assignment):
        unassigned = [variable for variable in self.variables if variable not in assignment]
        return min(unassigned, key=lambda variable: len(self.domains[variable]))
    
    def orderDomainValues(self, variable, assignment):
        return self.domains[variable]
    
    def isConsistent(self, variable, value, assignment):
        for neighbor in self.constraints[variable]:
            if neighbor in assignment and assignment[neighbor] == value:
                return False
        return True


variables = [(i, j) for i in range(9) for j in range(9)]
domains = {
    variable: set(range(1, 10)) if sudoku_grid[variable[0]][variable[1]] == 0
    else {sudoku_grid[variable[0]][variable[1]]}
    for variable in variables
}
constraints = {}

def addConstraint(variable):
    constraints[variable] = set()
    # cow constraints
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