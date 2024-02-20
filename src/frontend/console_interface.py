import time

from rich.console import Console
from rich.text import Text
from rich.panel import Panel
import keyboard
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

    # --------------------------------------- Menu ---------------------------------------

    # Display a menu which allows the user to select in which mode to run the zkp protocol.
    # 1. interactive mode - User is "Veronica" and the PC is "Pole". they start a conversation and the user is asked to provide the nonce and the value for each cell. and the PC will verify the user's input.
    # 1.1 User can choose which type of selection to provide (row, column, block)
    # 1.2 User can choose to provide all the selections at once or one by one.
    # 2. semi automatic mode - PC will shw to user that there are a proof that puzzle is solved and he can show the proof for each type of selection (row, column, block). and the PC will ask the user to provide the type he want to see

    # 3. automatic mode - PC will show to user that there are a proof that puzzle is solved and he can show the proof for each type of selection (row, column, block).

    # 4. exit - exit the program

    # the menu will interact as a prompt selection so user can choose by arrow keys and press enter to select the option.

    def wait_for_input(self, message="Press any key to continue..."):
        self.console.print(message, style="bold blue")
        while True:
            if keyboard.read_event():
                break

        time.sleep(0.1)

    def interactive_mode(self):
        # Implement your interactive mode logic here
        self.console.print("Interactive mode selected: ", style="bold green")

    def semi_automatic_mode(self):
        # Prompt for difficulty level
        self.console.print("Semi-automatic mode selected: ", style="bold green")
        difficulty = self.console.input("Enter the difficulty level (e.g., Easy, Medium, Hard): ")
        self.console.print(f"Difficulty level set to: [bold]{difficulty}[/]", style="bold green")
        # ---
        # Generate puzzle based on the chosen difficulty level
        puzzle = PuzzleGenerator.generate(level=difficulty)
        self.console.print("Generated Sudoku Puzzle:", style="bold blue")
        self.display_puzzle(puzzle)
        # ---
        # # You can now use the difficulty variable as needed for your logic
        # self.wait_for_input()

    def automatic_mode(self):
        # Implement your automatic mode logic here
        self.console.print("Automatic mode selected: ", style="bold green")


    def show_menu(self, options, index):
        self.console.clear()
        for i, option in enumerate(options):
            if i == index:
                self.console.print(Panel(f"[bold white on green]{option}[/]", expand=False))
            else:
                self.console.print(option)

    def menu(self):
        # self.console.print("Solved Sudoku Puzzle:", style="bold green")
        header = Panel("ZKP Sudoku Game Menu Puzzle", style="bold white on blue", expand=False)
        self.console.print(header)

        self.console.print("ZKP Sudoku Game Menu", style="bold underline green")

        options = ["Interactive mode", "Semi-automatic mode", "Automatic mode", "Exit"]
        index = 0

        self.show_menu(options, index)

        while True:

            if keyboard.is_pressed('up') and index > 0:
                index -= 1
                self.show_menu(options, index)
                while keyboard.is_pressed('up'):
                    pass  # Wait until key release
            elif keyboard.is_pressed('down') and index < len(options) - 1:
                index += 1
                self.show_menu(options, index)
                while keyboard.is_pressed('down'):
                    pass  # Wait until key release
            elif keyboard.is_pressed('enter'):
                if index == 0:
                    self.interactive_mode()
                elif index == 1:
                    self.semi_automatic_mode()
                elif index == 2:
                    self.automatic_mode()
                elif index == 3:
                    self.console.print("Exiting the program...", style="bold blue")
                    sys.exit(0)
                break

    def run(self):
        self.menu()
        # self.run_auto_mode()

    def run_auto_mode(self):
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
