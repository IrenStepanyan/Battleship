from Board import Board
from Ship import Battleship, Cruiser, Submarine, Destroyer

COLUMNS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

class Player:
    def __init__(self, name, board: Board, opponent_board: Board):
        self.name = name
        self.board = board
        self.opponent_board = opponent_board

        self.ships_to_place = {
            1: ('Battleship', Battleship, 1, 4),
            2: ('Cruiser', Cruiser, 2, 3),
            3: ('Submarine', Submarine, 3, 2),
            4: ('Destroyer', Destroyer, 4, 1),
        }

    def place_ships(self):
        while any(count > 0 for (_, _, count, _) in self.ships_to_place.values()):
            print("\nShips left to place:")
            for key, (name, _, count, size) in self.ships_to_place.items():
                if count > 0:
                    print(f"{key}. {name} (size {size}) - {count} left")

            choice = input("Choose ship number to place: ").strip()
            if not choice.isdigit() or int(choice) not in self.ships_to_place:
                print("Invalid choice, try again.")
                continue

            choice = int(choice)
            name, ship_class, count, size = self.ships_to_place[choice]
            if count == 0:
                print(f"No {name}s left to place. Choose another ship.")
                continue

            try:
                pos = input(f"Enter start position for {name} (e.g., A5): ").upper().strip()
                orientation = input("Orientation (H for Horizontal, V for Vertical): ").upper().strip()
                row = int(pos[1:]) 
                col = ord(pos[0]) - ord('A')

                ship = ship_class()
                placed = ship.place_ship(row, col, orientation, self.board)
                if placed:
                    print(f"{name} placed successfully!")
                    self.ships_to_place[choice] = (name, ship_class, count - 1, size)
                    self.board.display(hide_ships=False)
                else:
                    print("Invalid position. Try again.")
            except Exception as e:
                print(f"Error: {e}. Try again.")



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
                return result

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
        self.hits = 0
        self.misses = 0
        self.total_moves = 0
        self.ships_to_place = {
            1: ('Battleship', Battleship, 1, 4),
            2: ('Cruiser', Cruiser, 2, 3),
            3: ('Submarine', Submarine, 3, 2),
            4: ('Destroyer', Destroyer, 4, 1),
        }
