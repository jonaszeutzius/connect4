import numpy as np
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class Connect4Board:
    def __init__(self, rows=6, columns=7):
        self.rows = rows
        self.columns = columns
        self.board = np.zeros((rows, columns), dtype=int)
        self.current_player = 1  # 1 for Player 1, -1 for Player 2
    
    def display_board(self, debug=True):
        p1 = ' 1' if debug else ' O'
        p2 = ' 2' if debug else ' O'
        empty = ' 0' if debug else '  '
        # Flip to show the bottom row at the bottom
        visual = np.flip(self.board, 0)
        total = ""
        for i in range(12):
            row = ""
            for j in range(15):
                char = '+'
                if i%2 and j%2:
                    char = '--'
                elif not (i%2 or j%2):
                    char = '|'
                elif i%2 == 0 and j%2 == 1:
                    num = visual[i//2, j//2]
                    if num == 2:
                        char = Fore.YELLOW + p2 + Style.RESET_ALL
                    elif num == 1:
                        char = Fore.RED + p1 + Style.RESET_ALL
                    else:
                        char = empty
                row += char
            total += row + '\n'
        print(total)
   
    def drop_piece(self, column):
        if column not in [0,1,2,3,4,5,6]:
            raise ValueError("Invalid Column")
        
        # Check if column is full
        if self.board[self.rows - 1, column] != 0:
            raise ValueError("Column is full")
        
        # Find the next open row in the specified column
        for row in range(self.rows):
            if self.board[row, column] == 0:
                self.board[row, column] = self.current_player
                break

    def check_for_win(self, player):
        # Check horizontal locations for win
        for row in range(self.rows):
            for col in range(self.columns - 3):
                if (self.board[row, col] == player and
                    self.board[row, col + 1] == player and
                    self.board[row, col + 2] == player and
                    self.board[row, col + 3] == player):
                    return (True, [(row, col), (row, col + 1), (row, col + 2), (row, col + 3)])

        # Check vertical locations for win
        for row in range(self.rows - 3):
            for col in range(self.columns):
                if (self.board[row, col] == player and
                    self.board[row + 1, col] == player and
                    self.board[row + 2, col] == player and
                    self.board[row + 3, col] == player):
                    return (True, [(row, col), (row + 1, col), (row + 2, col), (row + 3, col)])

        # Check positively sloped diagonals for win
        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                if (self.board[row, col] == player and
                    self.board[row + 1, col + 1] == player and
                    self.board[row + 2, col + 2] == player and
                    self.board[row + 3, col + 3] == player):
                    return (True, [(row, col), (row + 1, col + 1), (row + 2, col + 2), (row + 3, col + 3)])

        # Check negatively sloped diagonals for win
        for row in range(3, self.rows):
            for col in range(self.columns - 3):
                if (self.board[row, col] == player and
                    self.board[row - 1, col + 1] == player and
                    self.board[row - 2, col + 2] == player and
                    self.board[row - 3, col + 3] == player):
                    return (True, [(row, col), (row - 1, col + 1), (row - 2, col + 2), (row - 3, col + 3)])

        return (False, None)  # Return False and None if there is no win

    def switch_player(self):
        # Switch between Player 1 and Player 2
        self.current_player = self.current_player % 2 + 1


# board = Connect4Board()
# board.display_board()
# board.drop_piece(0)
# board.switch_player()
# board.drop_piece(3)
# board.switch_player()
# board.drop_piece(3)
# board.display_board(debug=False)