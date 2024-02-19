import hashlib
import random


class ZeroKnowledgeProof:
    def __init__(self, puzzle, solution):
        self.puzzle = puzzle  # The original puzzle (2D list)
        self.solution = solution  # The solved puzzle (2D list)
        self.nonces = self.generate_nonces()  # Generate nonces
        self.cards = self.place_cards()  # Initialize cards based on the solution
        self.commitments = self.generate_commitments()  # Generate commitments using nonces and solution values

    def hash_packet(self, packet, nonce):
        # Concatenate all packet values with nonce for hashing
        combined = '-'.join(map(str, packet)) + f"-{nonce}"
        return hashlib.sha256(combined.encode()).hexdigest()

    """def place_cards(self):
        # Initialize cards with solution values; could be adjusted for puzzle setup
        return [[self.solution[i][j] for j in range(9)] for i in range(9)]"""


    def place_cards(self):
        # For each cell, create a 'card' with the solution value (simulating faced down placement)
        # For filled cells in the original puzzle, we simulate faced up placement by not hiding the value
        cards = [[None for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                cards[i][j] = [self.solution[i][j]] * 3 if self.puzzle[i][j] == 0 else [self.puzzle[i][j]] * 3
        return cards
    def generate_nonces(self):
        # Generate a nonce for each cell in a 2D list structure
        return [[random.getrandbits(256) for _ in range(9)] for _ in range(9)]

    def generate_commitments(self):
        # Generate commitments based on solution values and nonces
        commitments = {}
        for i in range(9):
            for j in range(9):
                val = self.cards[i][j]
                nonce = self.nonces[i][j]
                commitments[(i, j)] = self.hash_packet([val], nonce)
        return commitments

    def select_cards_for_selection(self, selection_type, index):
        """
        Selects cards (values) and their corresponding nonces for a specific row, column, or grid.

        Args:
        - selection_type: The type of selection ('row', 'column', or 'grid').
        - index: The index of the row, column, or grid.

        Returns:
        - A list of tuples, where each tuple contains the card value, its corresponding nonce,
          and its position (row, column) for the selected selection.
        """
        selected_cards = []
        if selection_type == 'row':
            for j in range(9):  # Iterate through each column in the row
                card = self.cards[index][j]
                nonce = self.nonces[index][j]
                position = (index, j)
                selected_cards.append((card, nonce, position))

        elif selection_type == 'column':
            for i in range(9):  # Iterate through each row in the column
                card = self.cards[i][index]
                nonce = self.nonces[i][index]
                position = (i, index)
                selected_cards.append((card, nonce, position))

        elif selection_type == 'grid':
            start_row = (index // 3) * 3
            start_col = (index % 3) * 3
            for i in range(3):
                for j in range(3):
                    row = start_row + i
                    col = start_col + j
                    card = self.cards[row][col]
                    nonce = self.nonces[row][col]
                    position = (row, col)
                    selected_cards.append((card, nonce, position))

        return selected_cards

    def verify_complete_selection(self, selection_type, index):
        # Gather all selected cards for the specified selection
        selected_cards = self.select_cards_for_selection(selection_type, index)

        # Extract just the card values for completeness check
        card_values = [card[0] for card, _, _ in selected_cards]

        # Check if all numbers from 1 to 9 are present
        if sorted(card_values) != list(range(1, 10)):
            print(f"Verification Failed: Not all numbers from 1 to 9 are present in the {selection_type} {index}.")
            return False

        # Verify each card's commitment
        for selection in selected_cards:
            if not self.verify_selection(selection):
                print(f"Verification Failed: Commitment mismatch for card in {selection_type} {index}.")
                return False

        print(f"Verification Successful: All numbers from 1 to 9 are present in the {selection_type} {index}.")
        print(f"Verification Successful: All commitments for the {selection_type} {index} are valid.")
        return True

    def verify_selection(self, selection):
        # Verify a single selection; this can be adapted for batch verification
        card, nonce, position = selection
        i, j = position
        expected_commitment = self.commitments[(i, j)]
        print(f"Expected Commitment: {expected_commitment}")
        actual_commitment = self.hash_packet([card], nonce)
        print(f"Actual Commitment: {actual_commitment}")
        return expected_commitment == actual_commitment

    def run_zkp(self):
        # Randomly choose a row for the demonstration of ZKP
        row_index = random.randint(0, 8)
        selected_row = self.solution[row_index]
        # Adjust nonce collection to match the 2D structure, collecting nonces for the entire row
        selected_row_nonces = self.nonces[row_index]
        verified = self.verify_complete_selection('row', row_index)

        # Perform the verification process for the selected row
        # verified = all(self.verify_selection(selection) for selection in selections)

        # Construct the commitments for the selected row to be used in verification
        # This mimics sending specific commitments relevant to the verification process
        selected_row_commitments = {(row_index, j): self.commitments[(row_index, j)] for j in range(9)}

        # Populate zkp_results with relevant information
        self.zkp_results = {
            "all_commitments": self.commitments,  # Include all commitments for full transparency
            "selected_type": 'row',  # Indicate whether a row, column, or grid was selected
            "selected_index": row_index,  # The index of the selected row/column/grid
            "selected_values": selected_row,  # Actual values of the selected row/column/grid from the solution
            "selected_nonces": selected_row_nonces,  # Nonces corresponding to the selected values
            "selected_commitments": selected_row_commitments,
            # Commitments specifically for the selected row/column/grid
            "verification_process": "Verification Successful" if verified else "Verification Failed",
            # Result of the verification
            # You can add more fields as necessary for debugging or verification purposes
            # "selections": self.select_cards(),  # Include the selections made (cards chosen for verification)
            # all nonces
            "all_nonces": self.nonces
        }

        return self.zkp_results

    def flatten(self, two_dimensional_list):
        # Utility method to flatten a 2D list into a 1D list
        return [item for sublist in two_dimensional_list for item in sublist]
