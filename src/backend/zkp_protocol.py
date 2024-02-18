import hashlib
import random


class ZeroKnowledgeProof:
    def __init__(self, puzzle, solution):
        self.puzzle = puzzle  # The original puzzle (2D list)
        self.solution = solution  # The solved puzzle (2D list)
        self.packets = []  # To store packets for each row, column, and 3x3 grid
        self.cards = self.place_cards()  # To keep track of verifier's card selections
        self.nonces = self.generate_nonces()
        self.commitments = self.generate_commitments()

    def hash_packet(self, packet):
        # Convert packet to string and hash using SHA256
        packet_str = ''.join(map(str, packet))
        return hashlib.sha256(packet_str.encode()).hexdigest()

    def place_cards(self):
        # For each cell, create a 'card' with the solution value (simulating faced down placement)
        # For filled cells in the original puzzle, we simulate faced up placement by not hiding the value
        cards = [[None for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                cards[i][j] = [self.solution[i][j]] * 3 if self.puzzle[i][j] == 0 else [self.puzzle[i][j]] * 3
        return cards

    def select_cards(self):
        # Verifier selects one card from each cell randomly for rows, columns, and grids
        selections = []
        for i in range(9):
            row_packet, col_packet = [], []
            for j in range(9):
                row_packet.append(random.choice(self.cards[i][j]))
                col_packet.append(random.choice(self.cards[j][i]))
            selections.append((self.hash_packet(row_packet), 'row', i))
            selections.append((self.hash_packet(col_packet), 'column', i))
        # Add selections for 3x3 grids
        for x in range(0, 9, 3):
            for y in range(0, 9, 3):
                grid_packet = []
                for i in range(3):
                    for j in range(3):
                        grid_packet.append(random.choice(self.cards[x + i][y + j]))
                selections.append((self.hash_packet(grid_packet), 'grid', x // 3 * 3 + y // 3))
        return selections

    def verify_selection(self, selection):
        # Placeholder for actual verification logic
        # print(f"Verifying {selection[1]} {selection[2]}: {selection[0]}")
        return True

    def generate_nonces(self):
        # Mockup: Generate a nonce for each cell
        return [random.getrandbits(256) for _ in range(81)]

    def generate_commitments(self):
        # Mockup: Generate commitments for each value in the permuted solution using nonces
        # You'll need to adapt this logic based on how you're permuting and hashing solution values
        commitments = [hashlib.sha256((str(nonce) + str(val)).encode('utf-8')).hexdigest()
                       for nonce, val in zip(self.nonces, self.flatten(self.solution))]
        return commitments

    def run_zkp(self):
        selections = self.select_cards()

        # Example: Selecting the row dynamically with random
        row_index = random.randint(0, 8)
        selected_row = self.solution[row_index]
        selected_row_nonces = self.nonces[row_index * 9:(row_index + 1) * 9]  # Assuming nonces are flat

        # Mock verification process, replace with your actual logic
        verified = True  # Placeholder for actual verification result

        # Populate zkp_results correctly
        self.zkp_results = {
            "commitments": self.commitments,  # Ensure this is populated elsewhere in your class
            "row_index": row_index,
            "selected_row": selected_row,
            "selected_row_nonces": selected_row_nonces,
            "verification_process": "Verification Successful" if verified else "Verification Failed",
        }
        return self.zkp_results

    def flatten(self, two_dimensional_list):
        # Utility method to flatten a 2D list into a 1D list
        return [item for sublist in two_dimensional_list for item in sublist]
