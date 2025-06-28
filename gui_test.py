import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from Board import Board
from Player import Player
from Ship import Battleship, Cruiser, Submarine, Destroyer, Ship

CELL_SIZE = 50
GRID_SIZE = 10
MARGIN = 30  # for labels like A–J and 0–9

# Updated SHIP_CLASSES with 4 values per ship: (Class, count, size, image filename)
SHIP_CLASSES = {
    'Battleship': (Battleship, 1, 4, 'Battleship.png'),
    'Cruiser': (Cruiser, 2, 3, 'Cruiser.png'),
    'Submarine': (Submarine, 3, 2, 'Submarine.png'),
    'Destroyer': (Destroyer, 4, 1, 'Destroyer.png')
}

class BattleshipGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Battleship 2-Player")
        self.images = {}
        self.selected_ship = None
        self.orientation = 'H'
        self.phase = "placement_p1"
        self.player1 = Player("Player 1", Board(), Board())
        self.player2 = Player("Player 2", Board(), Board())
        self.current_player = self.player1
        self.opponent = self.player2
        self.remaining_ships = self.init_remaining_ships()

        self.load_images()
        self.setup_gui()

    def init_remaining_ships(self):
        return {name: count for name, (_, count, _, _) in SHIP_CLASSES.items()}

    def load_images(self):
        try:
            water_img = Image.open("assets/water.png")
            self.images['water'] = ImageTk.PhotoImage(water_img.resize(
                (CELL_SIZE * GRID_SIZE, CELL_SIZE * GRID_SIZE)))

            for name, (_, _, size, image_file) in SHIP_CLASSES.items():
                img = Image.open(f"assets/{image_file}")

                if size > 1:
                    width = CELL_SIZE * size
                    height = CELL_SIZE

                    img = img.resize((width, height), Image.LANCZOS)
                    self.images[name] = ImageTk.PhotoImage(img)

                    vertical_img = img.rotate(90, expand=True)
                    self.images[f"{name}_V"] = ImageTk.PhotoImage(vertical_img)
                else:
                    img = img.resize((CELL_SIZE, CELL_SIZE), Image.LANCZOS)
                    self.images[name] = ImageTk.PhotoImage(img)

        except Exception as e:
            print(f"Error loading images: {e}")
            messagebox.showerror("Image Error", "Could not load game images!")
            self.root.destroy()

    def setup_gui(self):
        self.status_label = tk.Label(self.root, text="Player 1: Place your ships (click to place, press 'R' or click Rotate to turn)", font=("Arial", 12))
        self.status_label.pack()

        total_width = MARGIN + 2 * (CELL_SIZE * GRID_SIZE) + 40
        total_height = MARGIN + CELL_SIZE * GRID_SIZE
        self.canvas = tk.Canvas(self.root, width=total_width, height=total_height + 80)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.handle_click)
        self.root.bind("r", self.toggle_orientation)

        self.ship_frame = tk.Frame(self.root)
        self.ship_frame.pack(pady=10)

        for name in SHIP_CLASSES.keys():
            btn = tk.Button(self.ship_frame, text=name, command=lambda n=name: self.select_ship(n))
            btn.pack(side="left", padx=5)

        rotate_btn = tk.Button(self.ship_frame, text="Rotate (R)", command=self.toggle_orientation)
        rotate_btn.pack(side="left", padx=5)

        self.draw_boards()

    def draw_boards(self):
        self.canvas.delete("all")
        px1 = MARGIN
        px2 = MARGIN + GRID_SIZE * CELL_SIZE + 40

        # Backgrounds
        self.canvas.create_image(px1, MARGIN, image=self.images['water'], anchor="nw")
        self.canvas.create_image(px2, MARGIN, image=self.images['water'], anchor="nw")

        # Grid + Labels
        for i in range(GRID_SIZE):
            letter = chr(ord('A') + i)
            number = str(i)

            self.canvas.create_text(px1 + i * CELL_SIZE + CELL_SIZE / 2, MARGIN / 2, text=letter)
            self.canvas.create_text(px2 + i * CELL_SIZE + CELL_SIZE / 2, MARGIN / 2, text=letter)

            self.canvas.create_text(MARGIN / 2, MARGIN + i * CELL_SIZE + CELL_SIZE / 2, text=number)
            self.canvas.create_text(px2 - 20, MARGIN + i * CELL_SIZE + CELL_SIZE / 2, text=number)

            for j in range(GRID_SIZE):
                x1 = px1 + j * CELL_SIZE
                y1 = MARGIN + i * CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x1 + CELL_SIZE, y1 + CELL_SIZE, outline="black")

                x2 = px2 + j * CELL_SIZE
                self.canvas.create_rectangle(x2, y1, x2 + CELL_SIZE, y1 + CELL_SIZE, outline="black")

        self.draw_ships()
        self.draw_attacks()

    def draw_ships(self):
        board = self.current_player.board if self.phase != "battle" else self.player1.board
        px = MARGIN

        for ship in getattr(board, "ships", []):
            if not ship.is_placed:
                continue
            row, col = ship.position[0]
            x = px + col * CELL_SIZE
            y = MARGIN + row * CELL_SIZE
            name = ship.__class__.__name__
            orientation_suffix = "" if ship.orientation.value == "H" else "_V"
            img = self.images.get(name + orientation_suffix)
            if img:
                self.canvas.create_image(x, y, image=img, anchor="nw")

    def draw_attacks(self):
        for player, px in [(self.player1, MARGIN + GRID_SIZE * CELL_SIZE + 40), (self.player2, MARGIN)]:
            board = player.opponent_board
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    mark = board.grid[r][c]
                    x = px + c * CELL_SIZE
                    y = MARGIN + r * CELL_SIZE
                    if mark == "X":
                        self.canvas.create_oval(x+10, y+10, x+40, y+40, fill="red")
                    elif mark == "O":
                        self.canvas.create_oval(x+15, y+15, x+35, y+35, outline="blue")

    def select_ship(self, ship_name):
        if self.remaining_ships[ship_name] > 0:
            self.selected_ship = ship_name
            self.status_label.config(text=f"{self.current_player.name}: selected {ship_name} ({self.orientation})")
        else:
            messagebox.showinfo("Unavailable", f"No {ship_name}s left to place.")

    def toggle_orientation(self, event=None):
        self.orientation = "V" if self.orientation == "H" else "H"
        self.status_label.config(text=f"{self.current_player.name} orientation: {self.orientation}")

    def handle_click(self, event):
        x, y = event.x, event.y
        col = (x - MARGIN) // CELL_SIZE
        row = (y - MARGIN) // CELL_SIZE

        if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
            return

        if self.phase.startswith("placement"):
            self.place_ship_on_board(row, col)
        elif self.phase == "battle":
            if x < MARGIN + GRID_SIZE * CELL_SIZE:
                return
            self.attack_cell(row, col)

    def place_ship_on_board(self, row, col):
        if not self.selected_ship:
            messagebox.showinfo("Select Ship", "Please select a ship first.")
            return

        ShipClass, _, _, _ = SHIP_CLASSES[self.selected_ship]
        ship = ShipClass()

        try:
            placed = ship.place_ship(row, col, self.orientation, self.current_player.board)
            if placed:
                self.remaining_ships[self.selected_ship] -= 1
                if not hasattr(self.current_player.board, "ships"):
                    self.current_player.board.ships = []
                self.current_player.board.ships.append(ship)
                self.selected_ship = None

                if sum(self.remaining_ships.values()) == 0:
                    if self.phase == "placement_p1":
                        Ship.reset_counters()
                        self.phase = "placement_p2"
                        self.current_player = self.player2
                        self.opponent = self.player1
                        self.remaining_ships = self.init_remaining_ships()
                        self.status_label.config(text="Player 2: Place your ships")
                    else:
                        self.phase = "battle"
                        self.current_player = self.player1
                        self.opponent = self.player2
                        self.status_label.config(text="Battle begins! Player 1's turn")

                self.draw_boards()
        except ValueError as e:
            messagebox.showwarning("Invalid Placement", str(e))

    def attack_cell(self, row, col):
        result = self.opponent.board.receive_attack(row, col)

        if result == "repeat":
            messagebox.showinfo("Repeated", "You already attacked this cell.")
            return

        if result == "hit":
            self.current_player.opponent_board.grid[row][col] = "X"
            self.status_label.config(text=f"{self.current_player.name} hit! Go again.")
        else:
            self.current_player.opponent_board.grid[row][col] = "O"
            self.status_label.config(text=f"{self.current_player.name} missed. Switching turns.")
            self.current_player, self.opponent = self.opponent, self.current_player

        self.draw_boards()

        if self.opponent.board.all_ships_sunk():
            self.status_label.config(text=f"{self.current_player.name} wins!")
            messagebox.showinfo("Victory", f"{self.current_player.name} wins!")
            self.canvas.unbind("<Button-1>")


if __name__ == "__main__":
    root = tk.Tk()
    app = BattleshipGUI(root)
    root.mainloop()

