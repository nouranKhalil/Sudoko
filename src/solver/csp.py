class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        
    
    def isConsistent(self, variable, value, assignment):
        for neighbor in self.constraints[variable]:
            if neighbor in assignment and assignment[neighbor] == value:
                return False
        return True