import random
import backtracking

class PuzzleGenerator:
    def generateRandomSudoku(self, difficulty):
        sudoku_grid = [[0 for _ in range(9)] for _ in range(9)]
        if difficulty == "easy":
            noOfFilledCells = random.randint(35, 40)
        elif difficulty == "medium":
            noOfFilledCells = random.randint(28, 34)
        elif difficulty == "hard":
            noOfFilledCells = random.randint(20, 27)
        else:
            raise ValueError("Invalid difficulty level")
        
        filled_cells = 0
        # print("Generating Sudoku puzzle with", noOfFilledCells)
        while filled_cells < noOfFilledCells:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if sudoku_grid[row][col] == 0:
                value = random.randint(1, 9)
                sudoku_grid[row][col] = value
                
                if backtracking.isSolvable(sudoku_grid):
                    filled_cells += 1
                else:
                    sudoku_grid[row][col] = 0
        
        if backtracking.isSolvable(sudoku_grid):
            return sudoku_grid
        else:
            print("Generated puzzle was not solvable, retrying...")
            return self.generateRandomSudoku(difficulty)


# if __name__ == "__main__":
#     print("Generated Sudoku puzzle:")
#     puzzleGenerator = PuzzleGenerator()
#     generatedPuzzle = puzzleGenerator.generateRandomSudoku("hard")
#     for row in generatedPuzzle:
#         print(row)