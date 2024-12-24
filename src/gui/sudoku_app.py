import sys
import random
from tkinter import N
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout,
    QWidget, QLabel, QLineEdit
)
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtCore import Qt, QEvent,QTimer
from src.gui.board_helpers import get_input_limit
from PyQt5.QtWidgets import QMessageBox
from src.gui.utils import create_button, get_current_board, highlight_related_cells,handle_user_input,handle_user_input,handle_mouse_click,get_border_style
from PyQt5.QtGui import QFont, QPixmap
from src.solver.sudoku_generator import SudokuGenerator
from src.solver.csp import SudokuCSP
from src.solver.backtracking import Backtracking
import time
class SudokuApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku Solver")
        self.setGeometry(500, 100, 1000, 900)
        self.setFixedSize(1000,900)  
        self.setStyleSheet("background-color: #f0f4f7;")
        self.current_cell = (0, 0)
        self.remaining_cells = 0
        self.ai = False
        self.correct_solution = None
        self.current_mode = None
        self.time_label = None 
        self.main_menu()



    def main_menu(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop) 

        # title
        title = QLabel("Welcome to Sudoku Solver ✨")
        title.setFont(QFont("Arial", 30, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setFixedHeight(100) 
        title.setStyleSheet("""
        QLabel {
            color: #FFFFFF;
            background: qlineargradient(
                spread:pad, x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(92, 92, 255, 1),
                stop:0.5 rgba(90, 123, 192, 1),
                stop:1 rgba(92, 92, 255, 1) 
            );
            border-top-left-radius: 0px;   
            border-top-right-radius: 0px; 
            border-bottom-left-radius: 50px;  
            border-bottom-right-radius: 50px; 
            font-size: 48px;
            margin-top:0px;
            margin-bottom:10px;
            font-weight: bold;
            letter-spacing: 1px;
        }
    """)
        layout.addWidget(title)
        # sudoku image
        sudoku_image = QLabel()
        sudoku_pixmap = QPixmap("src\gui\sudoku.png")
        sudoku_pixmap = sudoku_pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        sudoku_image.setPixmap(sudoku_pixmap)
        sudoku_image.setAlignment(Qt.AlignCenter)
        layout.addWidget(sudoku_image)
        layout.addStretch(1)

        # buttons
        mode1_btn = create_button("Random Shuffle")
        mode1_btn.clicked.connect(lambda: self.select_difficulty(1))
        layout.addWidget(mode1_btn, alignment=Qt.AlignCenter)

        mode2_btn = create_button("User Inputs Board")
        mode2_btn.clicked.connect(lambda: self.select_difficulty(2))
        layout.addWidget(mode2_btn, alignment=Qt.AlignCenter)

        mode3_btn = create_button("Interactive Play")
        mode3_btn.clicked.connect(lambda: self.select_difficulty(3))
        layout.addWidget(mode3_btn, alignment=Qt.AlignCenter)

        quit_btn = create_button("Quit")
        quit_btn.clicked.connect(self.close)
        layout.addWidget(quit_btn, alignment=Qt.AlignCenter)
        layout.addStretch(1)

        # set layout to central widget
        self.central_widget.setLayout(layout)



    def select_difficulty(self, mode):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # vertical layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # title
        title = QLabel("Select Difficulty")
        title.setFont(QFont("Arial", 30, QFont.Bold))  
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: #333333;
                margin-top:50px;
                margin-bottom: 30px;
            }
        """)
        layout.addWidget(title)
        layout.addStretch(1)

        # buttons
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        icons = ["🥉", "🥈", "🏅"] 

        for difficulty, icon in zip(["Easy", "Medium", "Hard"], icons):
            btn = create_button(icon+" "+difficulty)
            btn.clicked.connect(lambda _, d=difficulty: self.start_game(mode, d))
            button_layout.addWidget(btn)


        back_btn = create_button("Back to Main Menu")
        back_btn.clicked.connect(self.main_menu)
        button_layout.addWidget(back_btn)

        layout.addLayout(button_layout)
        layout.addStretch(1)

        # apply the layout to the central widget
        self.central_widget.setLayout(layout)


    def start_game(self, mode, difficulty):
        if mode == 1 or mode == 3:
            self.start_prefilled_game(mode, difficulty)
        elif mode == 2:
            self.start_user_input_game(difficulty)

    def start_prefilled_game(self, mode, difficulty):
        self.current_mode = mode
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # main vertical layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # title at the top
        title = QLabel(f"Sudoku - {difficulty} Mode {mode}")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #333333; margin-bottom: 20px;")
        layout.addWidget(title)
        

        # initialize qtimer for the clock
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.start_time = time.time()  # record start time
        self.timer.start(1000)  # update every second

        # initialize the time_label for showing time taken
        self.time_label = QLabel("⏰ Time taken: 00.00 seconds")
        self.time_label.setFont(QFont("Arial", 16))
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("color: #333333; margin-top: 10px;")
        layout.addWidget(self.time_label)

        # sudoku grid
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.cells = []
        self.current_cell = (0, 0)
        
        board = SudokuGenerator.generate_sudoku_puzzle(difficulty=difficulty)

        # get the correct solution for interactive mode
        if mode == 3:  
            csp = SudokuCSP(board)
            solver = Backtracking(csp)
            solution_dict = Backtracking.backtrackingSearch(solver)
            if solution_dict:
                self.correct_solution = [[0 for _ in range(9)] for _ in range(9)]
                for (row, col), value in solution_dict.items():
                    self.correct_solution[row][col] = value

        grid_widget = QWidget()
        grid_widget.setFixedSize(450, 450)
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(0)
        grid_layout.setContentsMargins(0, 0, 0, 30)

        for row in range(9):
            row_cells = []
            for col in range(9):
                cell = QLineEdit()
                cell.setFont(QFont("Arial", 16))
                cell.setAlignment(Qt.AlignCenter)
                cell.setFixedSize(50, 50)
                cell.setValidator(QIntValidator(1, 9, self))
                cell.is_correct = -1  # default to unfilled

                border_style = get_border_style(row, col)
                cell.setStyleSheet(f"""
                    QLineEdit {{
                        background-color: #FFFFFF;
                        {border_style}
                        border-radius: 0px;
                        padding: 0px;
                        margin: 0px;
                    }}
                """)

                # prefilled cells
                if board[row][col] != 0:
                    cell.setText(str(board[row][col]))
                    cell.setReadOnly(True)
                    cell.is_correct = 2  # prefilled
                    cell.setStyleSheet(f"""
                        QLineEdit {{
                            background-color: #E6E6FA; 
                            color: #333333;
                            {border_style}
                            border-radius: 0px;
                            font-weight: bold;
                        }}
                    """)
                else:
                    if mode == 3:  # validation for interactive mode
                        cell.textChanged.connect(lambda _, r=row, c=col: self.validate_input(r, c))
                        cell.installEventFilter(self)
                        
                cell.mousePressEvent = lambda event, r=row, c=col: handle_mouse_click(self, event, r, c)
                row_cells.append(cell)
                grid_layout.addWidget(cell, row, col)
            self.cells.append(row_cells)

        grid_widget.setLayout(grid_layout)
        layout.addWidget(grid_widget, alignment=Qt.AlignCenter)

        buttons_layout = QVBoxLayout()
        row_1 = QHBoxLayout()
        new_game_btn = create_button("New Game")
        new_game_btn.clicked.connect(lambda: self.start_prefilled_game(mode, difficulty))
        row_1.addWidget(new_game_btn)

        back_btn = create_button("Back")
        back_btn.clicked.connect(lambda: self.select_difficulty(mode))
        row_1.addWidget(back_btn)

        buttons_layout.addLayout(row_1)

        row_2 = QHBoxLayout()
        quit_btn = create_button("Quit")
        quit_btn.clicked.connect(self.close)
        row_2.addWidget(quit_btn)

        solve_btn = create_button("Solve")
        solve_btn.clicked.connect(lambda: self.solve_game(board=board))
        if mode != 1:  # disable ai solving for interactive mode
            solve_btn.setEnabled(False)
        row_2.addWidget(solve_btn)

        buttons_layout.addLayout(row_2)
        layout.addLayout(buttons_layout)
        self.central_widget.setLayout(layout)

        if mode == 1:
            self.start_ai_clock(board)
        elif mode == 3:
            self.start_user_clock()

    def update_clock(self):
        time_taken = time.time() - self.start_time
        minutes, seconds = divmod(int(time_taken), 60)
        self.time_label.setText(f"⏰ Time Taken: {minutes:02}:{seconds:02}")

    def start_ai_clock(self, board):
        self.start_time = time.time()  
        csp = SudokuCSP(board)
        solver = Backtracking(csp)
        solution_dict = Backtracking.backtrackingSearch(solver)
 
        if solution_dict:
            self.correct_solution = [[0 for _ in range(9)] for _ in range(9)]
            for (row, col), value in solution_dict.items():
                self.correct_solution[row][col] = value
            self.timer.stop()  

    def start_user_clock(self):
        """Start the clock for user in Mode 3."""
        self.start_time = time.time() 
        
    def stop_clock(self):
        """Stop the clock when the puzzle is completed."""
        self.timer.stop()


    def stop_clock(self):
        """Stop the clock when the puzzle is completed."""
        self.timer.stop()

    def validate_input(self, row, col):
        """Validate the user's input against the correct solution."""
        if self.current_mode != 3:  
            return

        user_input = self.cells[row][col].text()
        print(user_input)
        correct_value = str(self.correct_solution[row][col])

        if hasattr(self, 'correct_solution') and self.correct_solution: 
            if user_input == correct_value:
                self.cells[row][col].is_correct = 1
                self.cells[row][col].setStyleSheet("""
                    QLineEdit {
                        background-color: #d4edda;  
                        border: 1px solid #ccc;
                    }
                """)
            else:
                self.cells[row][col].is_correct = 0
                self.cells[row][col].setStyleSheet("""
                    QLineEdit {
                        background-color: #f8d7da; 
                        border: 1px solid #ccc;
                    }
                """)

        highlight_related_cells(self,row, col)
        if self.is_puzzle_complete():
            self.stop_clock()  
            self.show_completion_message() 

    def start_user_input_game(self, difficulty):
        self.current_mode=2
        self.remaining_cells = get_input_limit(difficulty)
        self.filled_cells_count = 0  
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        title = QLabel(f"Sudoku - User Input ({difficulty})")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #333333; margin-bottom: 20px;")
        layout.addWidget(title)

        self.remaining_label = QLabel(f"Remaining cells: {self.remaining_cells}")
        self.remaining_label.setFont(QFont("Arial", 16))
        self.remaining_label.setAlignment(Qt.AlignCenter)
        self.remaining_label.setStyleSheet("margin-bottom: 10px; color: #555555;")
        layout.addWidget(self.remaining_label)
        # timer label
        self.time_label = QLabel("⏰ Time taken: 0.00 seconds")
        self.time_label.setFont(QFont("Arial", 16))
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("margin-top: 10px; color: #555555;")
        layout.addWidget(self.time_label)
        grid_clear_layout = QHBoxLayout()
        grid_clear_layout.setAlignment(Qt.AlignCenter)

        grid_widget = QWidget()
        grid_widget.setFixedSize(450, 450)
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(0) 
        grid_layout.setContentsMargins(50, 20, 10, 30)

        self.cells = []
        self.current_cell = (0, 0)
        for row in range(9):
            row_cells = []
            for col in range(9):
                cell = QLineEdit()
                cell.setFont(QFont("Arial", 16))
                cell.setAlignment(Qt.AlignCenter)
                cell.setValidator(QIntValidator(1, 9, self))
                cell.setFixedSize(50, 50)

                border_style = get_border_style(row, col)
                cell.setStyleSheet(f"""
                    QLineEdit {{
                        background-color: #FFFFFF;
                        {border_style}
                        border-radius: 0px;
                        padding: 0px;
                        margin: 0px;
                    }}
                """)

                cell.textChanged.connect(lambda _, r=row, c=col: handle_user_input(self, r, c))
                cell.installEventFilter(self)

                row_cells.append(cell)
                grid_layout.addWidget(cell, row, col)
            self.cells.append(row_cells)

        grid_widget.setLayout(grid_layout)
        grid_clear_layout.addWidget(grid_widget, alignment=Qt.AlignCenter)

        # clear
        clear_btn = create_button("🗘")
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #D1D5DB;
                color: #333333;
                border-radius: 5px;
                padding: 10px;
                font-size: 40px;
                width: 60px;
                height: 60px;
                margin-left: 20px;
            }
            QPushButton:hover {
                background-color: #E5E7EB;
            }
        """)
        clear_btn.clicked.connect(lambda: self.clear_board(difficulty))
        grid_clear_layout.addWidget(clear_btn, alignment=Qt.AlignCenter)

        layout.addLayout(grid_clear_layout)

        buttons_layout = QVBoxLayout()

        row_1 = QHBoxLayout()
        set_btn = create_button("Set")
        set_btn.clicked.connect(lambda: self.set_board(difficulty))
        row_1.addWidget(set_btn)

        back_btn = create_button("Back")
        back_btn.clicked.connect(lambda: self.select_difficulty(2))
        row_1.addWidget(back_btn)
        buttons_layout.addLayout(row_1)

        row_2 = QHBoxLayout()
        quit_btn = create_button("Quit")
        quit_btn.clicked.connect(self.close)
        row_2.addWidget(quit_btn)

        self.solve_btn = create_button("Solve")
        self.solve_btn.clicked.connect(lambda: self.solve_game(get_current_board(self))) 
        self.solve_btn.setEnabled(False)
        row_2.addWidget(self.solve_btn)
        buttons_layout.addLayout(row_2)
        layout.addLayout(buttons_layout)
        self.central_widget.setLayout(layout)


    def solve_game(self, board):
        print(self.current_mode)
        if self.current_mode == 2:
            self.ai = True
        start_time = time.time()
        csp = SudokuCSP(board)
        solver = Backtracking(csp)
        solution_dict = Backtracking.backtrackingSearch(solver)

        if solution_dict:
            solution = [[0 for _ in range(9)] for _ in range(9)]
            for (row, col), value in solution_dict.items():
                solution[row][col] = value

            # update the ui with the solved board
            for row in range(9):
                for col in range(9):
                    cell = self.cells[row][col]
                    cell.setText(str(solution[row][col]))
                    if cell.isReadOnly(): 
                        continue 

                    cell.setReadOnly(True)  
                    self.change_color(cell)
            self.show_completion_message()
            
            end_time = time.time()
            time_taken = end_time - start_time
            self.time_label.setText(f"⏰ Time taken: {time_taken:.2f} seconds")
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("The Sudoku puzzle is unsolvable. Please check the inputs.")
            msg.setWindowTitle("Unsolvable Puzzle")
            msg.exec_()
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Time taken to solve is {time_taken:f} seconds")
        self.ai = False

            

    def change_color(cell, color):
        new_style = f"QLineEdit {{ color: #00A300; }}"
        cell.setStyleSheet(new_style)

    def set_board(self,difficulty):
        filled_cells_count = 0
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].text():
                    filled_cells_count += 1
        
        if self.remaining_cells != 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(
                f"You need to fill {get_input_limit(difficulty)} cells to proceed.\n"
                f"Currently, you have filled {filled_cells_count} cells."
            )
            msg.setWindowTitle("Insufficient Cells Filled")
            msg.exec_()
            return
        
        for row in range(9):
            for col in range(9):
                cell = self.cells[row][col]
                border_style = get_border_style(row, col)
                if cell.text(): 
                    cell.setReadOnly(True)
                    cell.setStyleSheet(f"""
                        QLineEdit {{
                            background-color: #E6E6FA;  
                            color: #333333;
                            {border_style}
                            border-radius: 0px;
                            font-weight: bold;
                        }}
                    """)

        self.solve_btn.setEnabled(True) 
    def is_puzzle_complete(self):
        """Check if the board matches the correct solution."""
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].text() != str(self.correct_solution[row][col]):
                    return False
        return True

    def show_completion_message(self):
        """Show a success message when the puzzle is solved."""
        from PyQt5.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Congratulations🎉! Sudoku puzzle is solved!")
        msg.setWindowTitle("Puzzle Solved")
        msg.exec_()

    def clear_board(self,difficulty):
        self.start_user_input_game(difficulty)


    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if isinstance(obj, QLineEdit):
                row, col = self.current_cell
                new_row, new_col = row, col
                found = False

                if event.key() == Qt.Key_Up:
                    while new_row > 0:
                        new_row -= 1
                        if not self.cells[new_row][new_col].isReadOnly():
                            found = True
                            break

                elif event.key() == Qt.Key_Down:
                    while new_row < 8:
                        new_row += 1
                        if not self.cells[new_row][new_col].isReadOnly():
                            found = True
                            break

                elif event.key() == Qt.Key_Left:
                    while new_col > 0:
                        new_col -= 1
                        if not self.cells[new_row][new_col].isReadOnly():
                            found = True
                            break

                elif event.key() == Qt.Key_Right:
                    while new_col < 8:
                        new_col += 1
                        if not self.cells[new_row][new_col].isReadOnly():
                            found = True
                            break
                if found and (new_row, new_col) != (row, col):
                    self.current_cell = (new_row, new_col)
                    new_cell = self.cells[new_row][new_col]
                    new_cell.setFocus()
                    highlight_related_cells(self,new_row, new_col) 

        return super().eventFilter(obj, event)

