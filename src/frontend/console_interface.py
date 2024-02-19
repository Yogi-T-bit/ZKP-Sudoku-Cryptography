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

        # Display all commitments for full transparency
        # self.display_all_commitments(zkp_results["all_commitments"])

        # Display details of the selection made for verification
        self.console.print(f"\nVerification Selection:", style="bold blue")
        self.console.print(f"Selected Type: {zkp_results['selected_type']}")
        self.console.print(f"Selected Index: {zkp_results['selected_index']}")
        self.console.print(f"Selected Values: {zkp_results['selected_values']}")
        self.console.print(f"Selected Nonces: {zkp_results['selected_nonces']}")
        self.console.print(f"Selected Commitments: {zkp_results['selected_commitments']}")
        # self.console.print(f"All Nonces: {zkp_results['all_nonces']}")

        # Optionally display the selections made if relevant to your context
        # self.console.print("\nSelections Made:", style="bold blue")
        # for selection in zkp_results["selections"]:
        #     self.console.print(f"{selection}")

        # Display the verification process result
        self.console.print("\nVerification Process:", style="bold blue")
        self.console.print(zkp_results["verification_process"])

    def display_all_commitments(self, commitments):
        self.console.print("All Commitments:", style="bold blue")
        for (row, col), commitment in commitments.items():
            self.console.print(f"({row}, {col}): {commitment}")

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