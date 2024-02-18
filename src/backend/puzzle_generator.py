import random


class PuzzleGenerator:
    @staticmethod
    def generate_full_solution(grid):
        number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in range(0, 81):
            row = i // 9
            col = i % 9
            if grid[row][col] == 0:
                random.shuffle(number_list)
                for number in number_list:
                    if not (number in grid[row]):
                        if not number in [grid[x][col] for x in range(9)]:
                            square = []
                            if row < 3:
                                if col < 3:
                                    square = [grid[i][0:3] for i in range(0, 3)]
                                elif col < 6:
                                    square = [grid[i][3:6] for i in range(0, 3)]
                                else:
                                    square = [grid[i][6:9] for i in range(0, 3)]
                            elif row < 6:
                                if col < 3:
                                    square = [grid[i][0:3] for i in range(3, 6)]
                                elif col < 6:
                                    square = [grid[i][3:6] for i in range(3, 6)]
                                else:
                                    square = [grid[i][6:9] for i in range(3, 6)]
                            else:
                                if col < 3:
                                    square = [grid[i][0:3] for i in range(6, 9)]
                                elif col < 6:
                                    square = [grid[i][3:6] for i in range(6, 9)]
                                else:
                                    square = [grid[i][6:9] for i in range(6, 9)]
                            if not number in (square[0] + square[1] + square[2]):
                                grid[row][col] = number
                                if PuzzleGenerator.check_grid(grid):
                                    return True
                                else:
                                    if PuzzleGenerator.generate_full_solution(grid):
                                        return True
                break
        grid[row][col] = 0

    @staticmethod
    def check_grid(grid):
        for row in grid:
            if 0 in row:
                return False
        return True

    @staticmethod
    def generate(level='medium'):
        base_grid = [[0 for _ in range(9)] for _ in range(9)]
        PuzzleGenerator.generate_full_solution(base_grid)
        # Simplification for demo: Remove a set number of cells based on difficulty
        if level == 'easy':
            empties = 20
        elif level == 'medium':
            empties = 35
        else:
            empties = 50
        while empties > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if base_grid[row][col] != 0:
                base_grid[row][col] = 0
                empties -= 1
        return base_grid
