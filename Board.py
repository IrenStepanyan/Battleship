class Board:
    def __init__(self, size=10):
        self.size = size
        self.grid = [["~" for _ in range(size)] for _ in range(size)]

    def display(self, hide_ships=True):
        
        columns = "A B C D E F G H I J"
        print("  " + columns)
        for i, row in enumerate(self.grid):
            row_display = []
            for cell in row:
                if hide_ships and cell == "S":
                    row_display.append("~")
                else:
                    row_display.append(cell)
            print(f"{i} " + " ".join(row_display))

    def place_ships(self, ship, positions):
       
        for row, col in positions:
            self.grid[row][col] = "S"
        ship.is_placed = True
        ship.positions = positions

    def receive_attack(self, row, col):
       
        current = self.grid[row][col]
        if current in ["X", "O"]:
            return "repeat"
        elif current == "S":
            self.grid[row][col] = "X"
            return "hit"
        else:
            self.grid[row][col] = "O"
            return "miss"
