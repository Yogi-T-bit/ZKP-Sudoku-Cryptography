class SudokuSolver:
    def __init__(self, board=None):
        self._board = board

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, board):
        self._board = board

    def find_empty(self):
        """Find an empty cell in the Sudoku board. Empty cells are represented by 0."""
        for i in range(9):
            for j in range(9):
                if self._board[i][j] == 0:
                    return (i, j)  # row, col
        return None

    def valid(self, num, pos):
        """Check if a number is valid in the given position."""
        # Check row
        for i in range(9):
            if self._board[pos[0]][i] == num and pos[1] != i:
                return False

        # Check column
        for i in range(9):
            if self._board[i][pos[1]] == num and pos[0] != i:
                return False

        # Check 3x3 box
        box_x = pos[1] // 3
        box_y = pos[0] // 3
        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x*3, box_x*3 + 3):
                if self._board[i][j] == num and (i, j) != pos:
                    return False

        return True

    def solve(self):
        """Solve the Sudoku puzzle using backtracking."""
        find = self.find_empty()
        if not find:
            return True  # Puzzle solved
        else:
            row, col = find

        for i in range(1, 10):
            if self.valid(i, (row, col)):
                self._board[row][col] = i

                if self.solve():
                    return True

                self._board[row][col] = 0  # Backtrack

        return False  # Trigger backtracking

    def get_solved_board(self):
        """Returns the solved board."""
        if self.solve():
            return self._board
        else:
            return None
