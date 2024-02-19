from rich.console import Console
from rich.text import Text
import os
import sys

# Adjust sys.path as previously described to ensure imports work correctly
current_script_path = os.path.abspath(__file__)
project_root_path = os.path.dirname(os.path.dirname(os.path.dirname(current_script_path)))
src_path = os.path.join(project_root_path, 'src')
if src_path not in sys.path:
    sys.path.append(src_path)

from backend.puzzle_generator import PuzzleGenerator  # Ensure PuzzleGenerator is correctly implemented
from backend.sudoku_solver import SudokuSolver  # Ensure PuzzleGenerator is correctly implemented
from backend.zkp_protocol import ZeroKnowledgeProof  # Ensure ZKPSudoku is correctly implemented


class ConsoleInterface:
    def __init__(self):
        self.console = Console()

    def display_puzzle(self, puzzle):
        # Construct a visual representation of the puzzle.
        board_text = Text()
        for row_index, row in enumerate(puzzle):
            if row_index % 3 == 0 and row_index != 0:
                # Add a horizontal divider
                board_text.append("-" * 31 + "\n")
            for col_index, cell in enumerate(row):
                if col_index % 3 == 0 and col_index != 0:
                    # Add a vertical divider
                    board_text.append(" |")
                cell_text = f" {cell} " if cell != 0 else " . "
                if cell == 0:
                    board_text.append(cell_text, style="red")
                else:
                    board_text.append(cell_text, style="green")
            board_text.append("\n")
        self.console.print(board_text)

    def run_zkp_verification(self, puzzle, solution):
        zkp = ZeroKnowledgeProof(puzzle, solution)
        zkp_results = zkp.run_zkp()

        self.console.print(f"\nVerification Selection:", style="bold blue")
        self.print_nested_dict(zkp_results)

        self.console.print("\nVerification Process:", style="bold blue")

    def print_nested_dict(self, dictionary):
        for selection_type, selection_results in dictionary.items():
            self.console.print(f"{selection_type.capitalize()} Selections:", style="bold blue")
            for index, results in selection_results.items():
                self.console.print(f"Index: {index}")
                self.console.print(f"Selected Values: {results['selected_values']}")
                self.console.print(f"Selected Nonces:")
                for nonce in results["selected_nonces"]:
                    self.console.print(f"  - {nonce}")
                self.print_dict("Selected Commitments", results["selected_commitments"])
                self.console.print(f"Verification Process: {results['verification_process']}")
                self.console.print("\n")

    def print_dict(self, description, dictionary):
        self.console.print(f"{description}:", style="bold blue")
        for (row, col), dic in dictionary.items():
            self.console.print(f"({row}, {col}): {dic}")

    def run(self):
        level = self.console.input("Select difficulty [easy/medium/hard]: ").strip().lower()
        puzzle = PuzzleGenerator.generate(level)
        self.console.print("Generated Sudoku Puzzle:", style="bold blue")
        self.display_puzzle(puzzle)

        solver = SudokuSolver(puzzle)
        solved_board = solver.get_solved_board()
        if solved_board:
            self.console.print("Solved Sudoku Puzzle:", style="bold green")
            self.display_puzzle(solved_board)
            # Run Zero Knowledge Proof verification
            self.run_zkp_verification(puzzle, solved_board)
        else:
            self.console.print("Failed to solve the puzzle.", style="bold red")


if __name__ == "__main__":
    interface = ConsoleInterface()
    interface.run()
