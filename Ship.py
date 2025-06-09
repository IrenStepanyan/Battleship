class Ship:
    def __init__(self, size):
        self.size = size
        self.hits = 0
        self.position = []
        self.is_placed = False
        self.orientation = None

    def hit(self):
        self.hits += 1

    def is_sunk(self):
        return self.hits >= self.size

    def place_ship(self, start_row, start_col, orientation):
        if orientation not in ["horizontal", "vertical"]:
            raise ValueError("Orientation must be 'horizontal' or 'vertical'")

        positions = []
        for i in range(self.size):
            row = start_row + (i if orientation == "vertical" else 0)
            col = start_col + (i if orientation == "horizontal" else 0)

            if not (0 <= row <= 9 and 0 <= col <= 9):
                raise ValueError("Ship placement is out of board bounds")

            positions.append((row, col))

        self.position = positions
        self.orientation = orientation
        self.is_placed = True

    def get_positions(self):
        return self.position


class Battleship(Ship):
    max_allowed = 1
    placed_count = 0

    def __init__(self):
        if Battleship.placed_count >= Battleship.max_allowed:
            raise ValueError("Cannot create more than 1 Battleship")
        super().__init__(size=4)
        Battleship.placed_count += 1


class Cruiser(Ship):
    max_allowed = 2
    placed_count = 0

    def __init__(self):
        if Cruiser.placed_count >= Cruiser.max_allowed:
            raise ValueError("Cannot create more than 2 Cruisers")
        super().__init__(size=3)
        Cruiser.placed_count += 1


class Submarine(Ship):
    max_allowed = 3
    placed_count = 0

    def __init__(self):
        if Submarine.placed_count >= Submarine.max_allowed:
            raise ValueError("Cannot create more than 3 Submarines")
        super().__init__(size=2)
        Submarine.placed_count += 1


class Destroyer(Ship):
    max_allowed = 4
    placed_count = 0

    def __init__(self):
        if Destroyer.placed_count >= Destroyer.max_allowed:
            raise ValueError("Cannot create more than 4 Destroyers")
        super().__init__(size=1)
        Destroyer.placed_count += 1
