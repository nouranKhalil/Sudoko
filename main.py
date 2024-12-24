import sys
from PyQt5.QtWidgets import QApplication
from src.gui.sudoku_app import SudokuApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SudokuApp()
    window.show()
    sys.exit(app.exec_())
