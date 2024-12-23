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


# Remember to change the grid to numpy array in all the project for optimaisation


class SudokuCSP:
    def __init__(self):
        self.variables = [(i, j) for i in range(9) for j in range(9)]
        self.domains = {variable: set(range(1, 10)) for variable in self.variables}
        self.constraints = [
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
        for variable in self.variables:
            x, y = variable
            if sudoku_grid[x][y] != 0:
                self.domains[variable] = {sudoku_grid[x][y]}

    def print_domains(self) -> None:
        # print(self.domains)
        for key, value in self.domains.items():
            print(f"{key}: {value}")


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
