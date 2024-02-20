import random


class PuzzleGenerator:
    def __init__(self):
        self._grid = [[0 for _ in range(9)] for _ in range(9)]

    @property
    def grid(self):
        return self._grid

    @grid.setter
    def grid(self, value):
        self._grid = value

    def generate_full_solution(self):
        number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in range(0, 81):
            row = i // 9
            col = i % 9
            if self.grid[row][col] == 0:
                random.shuffle(number_list)
                for number in number_list:
                    if not (number in self.grid[row]) and \
                            all(number != self.grid[x][col] for x in range(9)):
                        square = self.get_square(row, col)
                        if number not in (square[0] + square[1] + square[2]):
                            self.grid[row][col] = number
                            if self.check_grid():
                                return True
                            else:
                                if self.generate_full_solution():
                                    return True
                break
        self.grid[row][col] = 0

    def get_square(self, row, col):
        square = []
        if row < 3:
            if col < 3:
                square = [self.grid[i][0:3] for i in range(0, 3)]
            elif col < 6:
                square = [self.grid[i][3:6] for i in range(0, 3)]
            else:
                square = [self.grid[i][6:9] for i in range(0, 3)]
        elif row < 6:
            if col < 3:
                square = [self.grid[i][0:3] for i in range(3, 6)]
            elif col < 6:
                square = [self.grid[i][3:6] for i in range(3, 6)]
            else:
                square = [self.grid[i][6:9] for i in range(3, 6)]
        else:
            if col < 3:
                square = [self.grid[i][0:3] for i in range(6, 9)]
            elif col < 6:
                square = [self.grid[i][3:6] for i in range(6, 9)]
            else:
                square = [self.grid[i][6:9] for i in range(6, 9)]
        return square

    def check_grid(self):
        for row in self.grid:
            if 0 in row:
                return False
        return True

    def generate(self, level='medium'):
        self.generate_full_solution()
        # Simplification for demo: Remove a set number of cells based on difficulty
        empties = {'easy': 20, 'medium': 35, 'hard': 50}.get(level, 35)
        while empties > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.grid[row][col] != 0:
                self.grid[row][col] = 0
                empties -= 1
        return self.grid
