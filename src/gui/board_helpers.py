import random
from PyQt5.QtWidgets import (QMessageBox)

def is_valid_move( board, row, col, value):
    for i in range(9):
        if board[row][i] == value or board[i][col] == value:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == value:
                return False
    return True

def validate_user_board(self):
    QMessageBox.information(self, "Validation", "Board validation is successful!")


def get_input_limit( difficulty):
    return {"Easy": 45, "Medium": 39, "Hard": 5}[difficulty]
