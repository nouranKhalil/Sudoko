# Remember to change the grid to numpy array in all the project for optimaisation
class SudokuCSP:
    def __init__(self, sudoku_grid : list):
        self.variables = [(i, j) for i in range(9) for j in range(9)]
        self.domains = {}
        self.update_domains(sudoku_grid)
        self.constraints = self.initialize_constraints()
        self.dict_constraints = {}
        self.addConstraints()

    def addConstraint(self, variable):
        self.dict_constraints[variable] = set()
        # row self.dict_constraints
        for i in range(9):
            if i != variable[0]:
                self.dict_constraints[variable].add((i, variable[1]))
        # column self.dict_constraints
        for j in range(9):
            if j != variable[1]:
                self.dict_constraints[variable].add((variable[0], j))
        # 3x3 box self.dict_constraints
        iOfBox, jOfBox = variable[0] // 3, variable[1] // 3
        for i in range(iOfBox * 3, (iOfBox + 1) * 3):
            for j in range(jOfBox * 3, (jOfBox + 1) * 3):
                if (i, j) != variable:
                    self.dict_constraints[variable].add((i, j))

    def addConstraints(self):
        for variable in self.variables:
            self.addConstraint(variable)

    def isConsistent(self, variable, value, assignment):
        for neighbor in self.dict_constraints[variable]:
            if neighbor in assignment and assignment[neighbor] == value:
                return False
        return True

    def initialize_constraints(self) -> list:
        """
        Initialize the constraints of the CSP.
        """
        return [
            (X1, X2)
            for X1 in self.variables
            for X2 in self.variables
            if (
                (X1 != X2)
                and (
                    X1[0] == X2[0]
                    or X1[1] == X2[1]
                    or (X1[0] // 3 == X2[0] // 3 and X1[1] // 3 == X2[1] // 3)
                )
            )
        ]

    def update_domains(self, sudoku_grid: list) -> None:
        """
        Update the domains of the variables based on the given Sudoku grid.

        Parameters:
        sudoku_grid (list): A 2D list representing the Sudoku grid where 0 indicates an empty cell.
        """
        self.domains = {
            variable: (
                set(range(1, 10))
                if sudoku_grid[variable[0]][variable[1]] == 0
                else {sudoku_grid[variable[0]][variable[1]]}
            )
            for variable in self.variables
        }

    def print_domains(self) -> None:
        # print(self.domains)
        for key, value in self.domains.items():
            print(f"{key}: {value}")
