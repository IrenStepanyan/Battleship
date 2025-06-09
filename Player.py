from enum import Enum
from Board import Board
from Ship import Ship

COLUMNS = "ABCDEFGHIJ"

class Orientation(Enum):
    HORIZONTAL = 'H'
    VERTICAL = 'V'

class Player:
    def __init__(self, name, board, opponent_board, ships_to_place):
        self.name = name
        self.board = board
        self.opponent_board = opponent_board
        self.ships_to_place = ships_to_place
        self.ships_placed = False

    def place_ships(self):
        print(f"Dear {self.name}, please place your ships on the board.")
        for ship in self.ships_to_place:
            if ship.is_placed:
                continue

            print(f"\nPlacing ship: {ship.__class__.__name__} (size {ship.size})")
            while True:
                try:
                    start = input("Enter starting position (row 0–9, col A–J, e.g. 3 C): ").split()
                    if len(start) != 2:
                        print("Please enter row and column separated by space.")
                        continue

                    try:
                        row = int(start[0])
                    except ValueError:
                        print("Row must be a number.")
                        continue

                    if not (0 <= row <= 9):
                        print("Row must be between 0 and 9.")
                        continue

                    col_letter = start[1].upper()
                    if col_letter not in COLUMNS:
                        print("Column must be between A and J.")
                        continue

                    col = COLUMNS.index(col_letter)

                    orientation_input = input("Enter orientation (H or V): ").upper()
                    if orientation_input not in [o.value for o in Orientation]:
                        print("Invalid orientation. Use 'H' or 'V'.")
                        continue

                    orientation = Orientation(orientation_input)

                    if orientation == Orientation.HORIZONTAL:
                        if col + ship.size > self.board.size:
                            print("Ship doesn't fit horizontally. Try again.")
                            continue
                        positions = [(row, col + i) for i in range(ship.size)]
                    else:
                        if row + ship.size > self.board.size:
                            print("Ship doesn't fit vertically. Try again.")
                            continue
                        positions = [(row + i, col) for i in range(ship.size)]

                    if any(self.board.grid[r][c] != "~" for r, c in positions):
                        print("Overlap detected. Try again.")
                        continue

                    self.board.place_ships(ship, positions)
                    print(f"{ship.__class__.__name__} placed.")
                    self.board.display(hide_ships=False)
                    break

                except Exception as e:
                    print("Error:", e)

        self.ships_placed = True
        print(f"\nAll ships placed for {self.name}.")

    def make_attack(self, opponent):
        print(f"\n{self.name}, it's your turn to attack!")
        while True:
            try:
                row = int(input("Enter row to attack (0–9): "))
                if not (0 <= row <= 9):
                    print("Row must be between 0 and 9.")
                    continue

                col_input = input("Enter column to attack (A–J): ").upper()
                if col_input not in COLUMNS:
                    print("Column must be a letter between A and J.")
                    continue

                col = COLUMNS.index(col_input)
                result = opponent.board.receive_attack(row, col)

                if result == "repeat":
                    print("Already attacked this position. Try again.")
                    continue
                elif result == "hit":
                    print("Hit!")
                    self.opponent_board.grid[row][col] = "X"
                elif result == "miss":
                    print("Miss.")
                    self.opponent_board.grid[row][col] = "O"
                break

            except ValueError:
                print("Row must be an integer.")
            except Exception as e:
                print("Error during attack:", e)

    def display_opponent_board(self):
        print(f"\n{self.name}'s view of the opponent's board:")
        self.opponent_board.display()

    def restart(self):
        self.board = Board()
        self.opponent_board = Board()
        self.ships_placed = False
        for ship in self.ships_to_place:
            ship.hits = 0
            ship.position = []
            ship.is_placed = False
