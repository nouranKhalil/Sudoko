import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton,
    QWidget, QLabel, QLineEdit, QMessageBox
)
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtCore import Qt, QEvent
from src.gui.board_helpers import is_valid_move
import numpy as np

def create_button(text):
    button = QPushButton(text)
    button.setFont(QFont("Arial", 16, QFont.Bold))
    button.setStyleSheet("""
        QPushButton {
            background-color: #5A7BC0;  
            color: white;  
            border-radius: 8px; 
            padding: 10px 20px; 
            margin-right:10px;
            margin-bottom:10px;
            width: 300px; 
            height: 50px;
        }
        QPushButton:hover {
            background-color: #BFDBFE;  
            color: #1D4ED8;  
        }
        QPushButton:pressed {
            background-color: #93C5FD;  
            border: 2px solid #2563EB;  
            color: #1E3A8A;  
        }
        QPushButton:disabled {
            background-color: #D1D5DB;  
            color: #9CA3AF; 
            border: 2px solid #D1D5DB;  
        }
    """)
    button.setCursor(Qt.PointingHandCursor)  
    return button


def highlight_related_cells(self, row, col):
    if self.current_mode != 3:
        return

    default_cell_style_template = """
        QLineEdit {{
            background-color: #FFFFFF;
            border: 1px solid #CCCCCC;
            border-radius: 0px;
            padding: 0px;
            {border_style}
            margin: 0px;
            text-align: center;
        }}
    """
    prefilled_cell_style_template = """
        QLineEdit {{
            background-color: #E6E6FA;
            color: #333333;
            border: 1px solid #CCCCCC;
            border-radius: 0px;
            padding: 0px;
            {border_style}
            margin: 0px;
            text-align: center;
            font-weight: bold;
        }}
    """
    highlight_style_template = """
        QLineEdit {{
            background-color: #E0F7FA;
            border: 1px solid #999999;
            border-radius: 0px;
            padding: 0px;
            {border_style}
            margin: 0px;
            text-align: center;
        }}
    """
    dark_highlight_style_template = """
        QLineEdit {{
            background-color: #B2EBF2;
            border: 1px solid #999999;
            border-radius: 0px;
            padding: 0px;
            {border_style}
            margin: 0px;
            text-align: center;
            font-weight: bold;
        }}
    """
    same_number_style_template = """
        QLineEdit {{
            background-color: #3282bf;
            border: 1px solid #3282bf;
            border-radius: 0px;
            padding: 0px;
            {border_style}
            margin: 0px;
            text-align: center;
        }}
    """
    selected_cell_style_template = """
        QLineEdit {{
            background-color: #FBEC5D;
            border: 2px solid #FFB74D;
            border-radius: 0px;
            {border_style}
            padding: 0px;
            margin: 0px;
            text-align: center;
        }}
    """
    correct_cell_style_template = """
        QLineEdit {{
            background-color: #A5D6A7;
            border: 2px solid #66BB6A;
            border-radius: 0px;
            padding: 0px;
            {border_style}
            margin: 0px;
            text-align: center;
            font-weight: bold;
        }}
    """
    incorrect_cell_style_template = """
        QLineEdit {{
            background-color: #EF9A9A;
            border: 2px solid #E57373;
            border-radius: 0px;
            padding: 0px;
            {border_style}
            margin: 0px;
            text-align: center;
            font-weight: bold;
        }}
    """

    # reset all cells to their default or prefilled styles unless they are correct or incorrect
    for r in range(9):
        for c in range(9):
            cell = self.cells[r][c]
            border_style = get_border_style(r, c)
            if cell.is_correct == -1:
                print("ll")
                style = default_cell_style_template.format(border_style=border_style)
            elif hasattr(cell, "is_correct") and cell.is_correct == 1:
                style = correct_cell_style_template.format(border_style=border_style)
            elif hasattr(cell, "is_correct") and cell.is_correct == 0:
                print(cell.is_correct)
                style = incorrect_cell_style_template.format(border_style=border_style)
            elif cell.text().strip():
                style = prefilled_cell_style_template.format(border_style=border_style)
            
                
            
            cell.setStyleSheet(style)

    # highlight the row and column
    for c in range(9):
        cell = self.cells[row][c]
        border_style = get_border_style(row, c)
        if cell.is_correct == 0:
            style = incorrect_cell_style_template.format(border_style=border_style)
        elif cell.text().strip():
            style = dark_highlight_style_template.format(border_style=border_style)
        else:
            style = highlight_style_template.format(border_style=border_style)
        cell.setStyleSheet(style)

    for r in range(9):
        cell = self.cells[r][col]
        border_style = get_border_style(r, col)
        if cell.is_correct == 0:
            style = incorrect_cell_style_template.format(border_style=border_style)
        elif cell.text().strip():
            style = dark_highlight_style_template.format(border_style=border_style)
        else:
            style = highlight_style_template.format(border_style=border_style)
        cell.setStyleSheet(style)

    # highlight the 3x3 grid
    start_row = 3 * (row // 3)
    start_col = 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            cell = self.cells[r][c]
            border_style = get_border_style(r, c)
            if cell.is_correct == 0:
                style = incorrect_cell_style_template.format(border_style=border_style)
            elif cell.text().strip():
                
                style = dark_highlight_style_template.format(border_style=border_style)
            else:
                style = highlight_style_template.format(border_style=border_style)
            cell.setStyleSheet(style)

    # highlight all cells with the same number
    selected_value = self.cells[row][col].text()
    if selected_value.strip():
        for r in range(9):
            for c in range(9):
                if cell.is_correct == 0:
                    style = incorrect_cell_style_template.format(border_style=border_style)
                if self.cells[r][c].text() == selected_value:
                    print("d")
                    cell = self.cells[r][c]
                    border_style = get_border_style(r, c)
                    style = same_number_style_template.format(border_style=border_style)
                    cell.setStyleSheet(style)

    cell = self.cells[row][col]
    border_style = get_border_style(row, col)
    selected_cell_style = selected_cell_style_template.format(border_style=border_style)
    cell.setStyleSheet(selected_cell_style)





def handle_mouse_click(self, event, row, col):
    """Handles mouse click on a Sudoku cell."""
    if event.button() == Qt.LeftButton:
        self.current_cell = (row, col)
        highlight_related_cells(self,row, col)  
        self.cells[row][col].setFocus()  

def get_current_board(self):
    board = []
    for row in self.cells:
        board.append([int(cell.text()) if cell.text() else 0 for cell in row])
    return np.array(board)
def update_remaining_cells(self):
    self.remaining_label.setText(f"Remaining cells: {self.remaining_cells}")
    if self.remaining_cells == 0:
        QMessageBox.information(self, "Board Complete", "You have filled all required cells!")
def handle_user_input(self, row, col):
    cell_value = self.cells[row][col].text()
    
    if cell_value.isdigit() and not self.ai and self.remaining_cells == 0:
        print(self.ai)
        self.cells[row][col].clear() 
        QMessageBox.warning(self, "Cell Limit Exceeded", "You cannot fill more cells than allowed.")
    elif cell_value.isdigit():
        value = int(cell_value)
        board = get_current_board(self)
        board[row][col] = 0  

        if not is_valid_move(board, row, col, value):
            QMessageBox.warning(self, "Invalid Input", "This violates Sudoku rules!")
            self.cells[row][col].clear() 
        else:
            if self.remaining_cells > 0:
                self.remaining_cells -= 1  
                update_remaining_cells(self)
                self.current_cell = (row, col)  
            
    elif self.remaining_cells !=0:
        self.remaining_cells += 1
        update_remaining_cells(self)
        self.current_cell = (row, col)
    self.remaining_label.setText(f"Remaining cells: {self.remaining_cells}")

def get_border_style( row, col):
    """Returns the border style for a cell based on its position."""
    border_style = "border: 1px solid #CCCCCC;"
    if row % 3 == 0:
        border_style += "border-top: 3px solid #333333;"
    if col % 3 == 0:
        border_style += "border-left: 3px solid #333333;"
    if row == 8:
        border_style += "border-bottom: 3px solid #333333;"
    if col == 8:
        border_style += "border-right: 3px solid #333333;"
    return border_style



