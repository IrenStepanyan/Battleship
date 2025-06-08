from enum import Enum
from board import Board
from ship import Ship


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
            print(f"\nPlacing ship: {ship.name} (size {ship.size})")
            valid = False
            while not valid:
                try:
                    start = input("Enter starting position (row: 0-9, col: A-J, e.g. 3 C): ").split()
                    if len(start) != 2:
                        print("Please enter row and column separated by a space.")
                        continue
                    try:
                        row = int(start[0])
                    except ValueError:
                        print("Row must be a number between 0 and 9.")
                        continue

                    orientation_input = input("Enter orientation (H or V): ").upper()

                    if orientation_input not in [o.value for o in Orientation]:
                        print("Invalid orientation. Use 'H' or 'V'.")
                        continue

                    orientation = Orientation(orientation_input)

                    columns = "ABCDEFGHIJ"
                    row = int(start[0])
                    col = columns.index(start[1].upper())

                    positions = []

                    if orientation == Orientation.HORIZONTAL:
                        if col + ship.size > self.board.size:
                            print("Ship doesn't fit horizontally. Try again!")
                            continue
                        positions = [(row, col + i) for i in range(ship.size)]

                    elif orientation == Orientation.VERTICAL:
                        if row + ship.size > self.board.size:
                            print("Ship doesn't fit vertically. Try again!")
                            continue
                        positions = [(row + i, col) for i in range(ship.size)]

                    overlap = False
                    for r, c in positions:
                        if self.board.grid[r][c] != "~":
                            overlap = True
                            break

                    if overlap:
                        print("Overlap with another ship. Try again!")
                        continue

                    self.board.place_ships(ship, positions)
                    print(f"{ship.name} placed.")
                    self.board.display(hide_ships=False)
                    valid = True

                except Exception as e:
                    print("Invalid input or error occurred:", e)
                    continue

        self.ships_placed = True
        print(f"\nAll ships placed for {self.name}.")

    def make_attack(self, opponent):
        print(f"\n{self.name}, it's your turn to attack!")

        while True:
            try:
                row = int(input("Enter row to attack (0-9): "))

                col_input = input("Enter column to attack (A-J): ").upper()
                columns = "ABCDEFGHIJ"

                if not (0 <= row <= 9):
                    print("Row must be between 0 and 9.")
                    continue

                if col_input not in columns:
                    print("Column must be a letter between A and J.")
                    continue

                col = columns.index(col_input)

                result = opponent.board.receive_attack(row, col)

                if result == "hit":
                    print("Hit!")
                    self.opponent_board.grid[row][col] = "X"
                    break
                elif result == "miss":
                    print("Miss")
                    self.opponent_board.grid[row][col] = "O"
                    break
                elif result == "repeat":
                    print("Already attacked this spot.")
            except ValueError:
                print("Please enter a valid integer for the row.")

    def display_opponent_board(self):
        print(f"{self.name}'s view of the opponent's board:")
        self.opponent_board.display()

    def restart(self):
        self.board = Board()
        self.opponent_board = Board()
        self.ships_placed = False
        for ship in self.ships_to_place:
            ship.hits.clear()
            ship.is_placed = False


