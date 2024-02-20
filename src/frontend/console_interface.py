import time
import random

from prompt_toolkit.shortcuts import radiolist_dialog
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
import keyboard
import os
import sys

import sys
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.text import Text

from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import VSplit, HSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import RadioList, Button
from prompt_toolkit.application.current import get_app
from prompt_toolkit.layout.controls import FormattedTextControl

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
        self.puzzle_generator = PuzzleGenerator()
        self.sudoku_solver = SudokuSolver()
        self.running = True  # To manage the application's running state

    # region Puzzle and ZKP Verification Display
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

    def run_zkp_verification(self, puzzle, solution, proof_type=None):
        zkp = ZeroKnowledgeProof(puzzle, solution)
        zkp_results = zkp.run_zkp()

        self.console.print("\nVerification of 8/9 Random Selections", style="bold salmon1")

        if proof_type:
            proof_data = zkp_results.get(proof_type, {})  # Get the specified proof_type data or empty dict if not found
            self.print_nested_dict({proof_type: proof_data})
        else:
            self.print_nested_dict(zkp_results)

        self.console.print("\nVerification Process:", style="bold salmon1")

    def print_nested_dict(self, dictionary):
        for selection_type, selection_results in dictionary.items():
            self.console.print(f"{selection_type.capitalize()} Selections:", style="bold salmon1")
            for index, results in selection_results.items():
                # highlight the self.console.print(f"Index: {index}")
                self.console.print(f"Index: {index}", highlight=True)

                self.console.print(f"Selected Values: {results['selected_values']}")
                self.console.print(f"Selected Nonces:", style="bold salmon1")
                for nonce in results["selected_nonces"]:
                    self.console.print(f"  - {nonce}")
                self.print_dict("Selected Commitments", results["selected_commitments"], index)
                if results['verification_process'] == "Verification Successful":
                    color = "green"
                else:
                    color = "red"

                self.console.print(f"Verification Process: {results['verification_process']}", style=color)
                self.console.print("\n")

    def print_dict(self, description, dictionary, index=None):
        self.console.print(f"{description}:", style="bold salmon1")
        for (row, col), dic in dictionary.items():
            # index += 1
            col += 1
            self.console.print(f"({index}, {col}): {dic}")

    # endregion

    def interactive_mode(self):
        self.console.print("Interactive mode selected.", style="bold green")
        self.console.print("We do like to implement in future an interactive mode so:\nVeronica are Verifier and Pole "
                           "are the Proover.", style="bold green")
        self.return_to_menu()

    def semi_automatic_mode(self):
        try:
            self.console.print("Semi-automatic mode selected.", style="bold green")
            difficulty = Prompt.ask("Enter the difficulty level (Easy, Medium, Hard)")
            puzzle = self.puzzle_generator.generate(difficulty.lower())
            # notify user that the puzzle is ready
            self.display_puzzle(puzzle)

            self.sudoku_solver.board = puzzle
            self.sudoku_solver.solve()
            solution = self.sudoku_solver.get_solved_board()
            sol = Confirm.ask("Do you want to see the solution?")
            if sol:
                self.display_puzzle(solution)

            proof = Confirm.ask("Do you want to show the proof?")
            if proof:
                proof_types = ['row', 'column', 'grid']
                flag = 0
                while True:
                    proof_type = Prompt.ask("Please enter the type of proof you want to see (row, column, grid)")
                    if proof_type.lower() in proof_types:
                        flag += 1
                        self.run_zkp_verification(puzzle, solution, proof_type.lower())
                        if flag == 3:
                            break
                        continue
                    else:
                        self.console.print("Invalid input. Please enter a valid proof type (row, column, grid)",
                                           style="bold red")

            self.return_to_menu()

        except ValueError:
            self.console.print("Invalid input. Please enter a valid difficulty level (Easy, Medium, Hard)",
                               style="bold red")

    def return_to_menu(self):
        poop = Confirm.ask("Do you want to return to the main menu?")

        if poop:
            self.menu()  # Call the menu method to show the menu again
        else:
            self.exit_program()  # Exit the program if the user doesn't want to return to the menu

    def automatic_mode(self):
        self.console.print("Automatic mode selected.", style="bold green")
        # difficulty random from Easy, Medium, Hard
        difficulty = random.choice(["easy", "medium", "hard"])
        puzzle = self.puzzle_generator.generate(difficulty.lower())
        self.sudoku_solver.board = puzzle
        self.sudoku_solver.solve()

        solution = self.sudoku_solver.get_solved_board()
        self.display_puzzle(puzzle)
        self.run_zkp_verification(puzzle, solution)
        self.return_to_menu()

    def exit_program(self):
        self.running = False
        self.console.print("Exiting the program...", style="bold blue")
        sys.exit()

    def menu(self):
        options = [
            ('interactive', 'Interactive mode'),
            ('semi-auto', 'Semi-automatic mode'),
            ('auto', 'Automatic mode'),
            ('exit', 'Exit')
        ]

        while self.running:
            result = radiolist_dialog(
                title="Menu",
                text="Welcome to Sudoku Zero-Knowledge Proof (ZKP) Protocol\nPlease select an option:",
                values=options,
            ).run()

            if result == 'interactive':
                self.interactive_mode()
            elif result == 'semi-auto':
                self.semi_automatic_mode()
            elif result == 'auto':
                self.automatic_mode()
            elif result == 'exit':
                self.exit_program()
            elif result is None:
                self.exit_program()

    def run(self):
        try:
            self.menu()

        except KeyboardInterrupt:
            self.console.print("Program interrupted by user.", style="bold red")
            self.exit_program()


if __name__ == "__main__":
    interface = ConsoleInterface()
    interface.run()
