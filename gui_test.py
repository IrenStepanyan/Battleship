import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from Board import Board
from Player import Player
from Ship import Battleship, Cruiser, Submarine, Destroyer, Ship

CELL_SIZE = 50
GRID_SIZE = 10  # Explicit 10x10 grid
MARGIN = 30
BG_COLOR = '#B3CDE0'  # Pastel blue to complement ocean theme

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
        self.root.configure(bg=BG_COLOR)
        self.images = {}
        self.selected_ship = None
        self.orientation = 'H'
        self.phase = "start"
        self.player1 = None
        self.player2 = None
        self.current_player = None
        self.opponent = None
        self.remaining_ships = None
        self.preview_positions = []
        self.preview_valid = False
        self.ship_buttons = {}
        self.game_frame = None
        self.canvas = None
        self.status_label = None
        self.ship_frame = None
        self.load_images()
        self.setup_start_screen()

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
                    img_h = img.resize((width, height), Image.LANCZOS)
                    self.images[name] = ImageTk.PhotoImage(img_h)
                    img_v = img_h.rotate(90, expand=True)
                    self.images[f"{name}_V"] = ImageTk.PhotoImage(img_v)
                else:
                    img = img.resize((CELL_SIZE, CELL_SIZE), Image.LANCZOS)
                    self.images[name] = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading images: {e}")
            messagebox.showwarning("Image Warning", "Could not load some game images.")

    def setup_start_screen(self):
        self.start_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.start_frame.pack(expand=True, fill='both')
        tk.Label(self.start_frame, text="⚓ Battleship ⚓", font=("Arial", 24, "bold"), fg='#1E3A5F', bg=BG_COLOR).pack(pady=20)
        tk.Label(self.start_frame, text="Enter Player Names", font=("Arial", 16), fg='#1E3A5F', bg=BG_COLOR).pack(pady=10)
        self.p1_entry = tk.Entry(self.start_frame, font=("Arial", 12))
        self.p1_entry.insert(0, "Player 1")
        self.p1_entry.pack(pady=5)
        self.p2_entry = tk.Entry(self.start_frame, font=("Arial", 12))
        self.p2_entry.insert(0, "Player 2")
        self.p2_entry.pack(pady=5)
        tk.Button(self.start_frame, text="Start Game", font=("Arial", 12), bg='#22C55E', fg='white', command=self.start_game).pack(pady=20)

    def start_game(self):
        p1_name = self.p1_entry.get().strip() or "Player 1"
        p2_name = self.p2_entry.get().strip() or "Player 2"
        self.player1 = Player(p1_name, Board(), Board())
        self.player2 = Player(p2_name, Board(), Board())
        self.current_player = self.player1
        self.opponent = self.player2
        self.remaining_ships = self.init_remaining_ships()
        self.phase = "placement_p1"
        self.start_frame.destroy()
        self.setup_game_gui()

    def init_remaining_ships(self):
        return {name: count for name, (_, count, _, _) in SHIP_CLASSES.items()}

    def setup_game_gui(self):
        self.game_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        self.status_label = tk.Label(self.game_frame, text=f"{self.current_player.name}: Place your ships (click to place, press 'R' to rotate, move mouse to preview)", font=("Arial", 14), fg='#1E3A5F', bg=BG_COLOR)
        self.status_label.pack(pady=10)
        total_width = MARGIN + 2 * (CELL_SIZE * GRID_SIZE) + 60
        total_height = MARGIN + CELL_SIZE * GRID_SIZE + 100
        self.canvas = tk.Canvas(self.game_frame, width=total_width, height=total_height, bg=BG_COLOR)
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<Motion>", self.handle_mouse_move)
        self.root.bind("<Key>", self.handle_keypress)
        self.ship_frame = tk.Frame(self.game_frame, bg=BG_COLOR)
        self.ship_frame.pack(pady=10)
        self.ship_buttons = {}
        for name, (_, count, size, _) in SHIP_CLASSES.items():
            btn = tk.Button(self.ship_frame, text=f"{name}\n(Size: {size})", font=("Arial", 10), width=10, height=2, command=lambda n=name: self.select_ship(n))
            btn.pack(side="left", padx=5)
            self.ship_buttons[name] = btn
        tk.Button(self.ship_frame, text="🔄 Rotate (R)", font=("Arial", 11), bg='#3B82F6', fg='white', command=self.toggle_orientation).pack(side="left", padx=5)
        tk.Button(self.ship_frame, text="🏠 Main Menu", font=("Arial", 11), bg='#6B7280', fg='white', command=self.show_main_menu).pack(side="left", padx=5)
        self.update_ship_buttons()
        self.draw_boards()

    def show_turn_transition(self):
        # Hide game UI
        if self.game_frame:
            self.game_frame.destroy()
        self.transition_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.transition_frame.pack(expand=True, fill='both')
        tk.Label(self.transition_frame, text=f"⚔️ {self.current_player.name}'s Turn ⚔️", font=("Arial", 24, "bold"), fg='#1E3A5F', bg=BG_COLOR).pack(pady=50)
        tk.Button(self.transition_frame, text="Continue", font=("Arial", 12), bg='#22C55E', fg='white', command=self.resume_game).pack(pady=20)

    def resume_game(self):
        self.transition_frame.destroy()
        self.setup_game_gui()
        self.status_label.config(text=f"⚔️ {self.current_player.name}'s turn to attack! Click opponent's grid.")
        self.draw_boards()

    def handle_mouse_move(self, event):
        if not self.phase.startswith("placement") or not self.selected_ship:
            self.clear_ship_preview()
            return
        x, y = event.x, event.y
        if MARGIN <= x < MARGIN + GRID_SIZE * CELL_SIZE and MARGIN <= y < MARGIN + GRID_SIZE * CELL_SIZE:
            col = (x - MARGIN) // CELL_SIZE
            row = (y - MARGIN) // CELL_SIZE
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                self.update_ship_preview(row, col)
        else:
            self.clear_ship_preview()

    def update_ship_preview(self, row, col):
        _, _, size, _ = SHIP_CLASSES[self.selected_ship]
        positions = []
        valid = True
        if self.orientation == 'H':
            for i in range(size):
                new_col = col + i
                if new_col >= GRID_SIZE:
                    valid = False
                    break
                positions.append((row, new_col))
        else:
            for i in range(size):
                new_row = row + i
                if new_row >= GRID_SIZE:
                    valid = False
                    break
                positions.append((new_row, col))
        if valid and hasattr(self.current_player.board, 'grid'):
            for pos_row, pos_col in positions:
                if self.current_player.board.grid[pos_row][pos_col] == 'S':
                    valid = False
                    break
            if valid:
                for pos_row, pos_col in positions:
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            adj_row, adj_col = pos_row + dr, pos_col + dc
                            if 0 <= adj_row < GRID_SIZE and 0 <= adj_col < GRID_SIZE:
                                if self.current_player.board.grid[adj_row][adj_col] == 'S':
                                    valid = False
                                    break
                        if not valid:
                            break
                    if not valid:
                        break
        self.preview_positions = positions
        self.preview_valid = valid
        self.draw_boards()

    def clear_ship_preview(self):
        if self.preview_positions:
            self.preview_positions = []
            self.preview_valid = False
            self.draw_boards()

    def update_ship_buttons(self):
        for name, btn in self.ship_buttons.items():
            remaining = self.remaining_ships.get(name, 0)
            if remaining > 0:
                btn.config(state=tk.NORMAL, bg='#22C55E', text=f"{name}\n({remaining} left)")
            else:
                btn.config(state=tk.DISABLED, bg='#6B7280', text=f"{name}\n(Placed)")

    def draw_boards(self):
        self.canvas.delete("all")
        px1 = MARGIN  # Left board: player's fleet
        px2 = MARGIN + GRID_SIZE * CELL_SIZE + 60  # Right board: opponent's waters/attack grid
        left_title = f"{self.current_player.name}'s Fleet" if self.phase.startswith("placement") else f"{self.current_player.name}'s Fleet"
        right_title = "Opponent's Waters" if self.phase.startswith("placement") else f"{self.opponent.name}'s Attack Grid"
        self.canvas.create_text(px1 + GRID_SIZE * CELL_SIZE // 2, 10, text=left_title, font=("Arial", 12, "bold"), fill='#1E3A5F')
        self.canvas.create_text(px2 + GRID_SIZE * CELL_SIZE // 2, 10, text=right_title, font=("Arial", 12, "bold"), fill='#1E3A5F')
        if 'water' in self.images:
            self.canvas.create_image(px1, MARGIN, image=self.images['water'], anchor="nw")
            self.canvas.create_image(px2, MARGIN, image=self.images['water'], anchor="nw")
        for i in range(GRID_SIZE):  # 10x10 grid
            letter = chr(ord('A') + i)
            number = str(i)
            self.canvas.create_text(px1 + i * CELL_SIZE + CELL_SIZE // 2, MARGIN - 10, text=letter, font=("Arial", 10, "bold"), fill='#1E3A5F')
            self.canvas.create_text(px2 + i * CELL_SIZE + CELL_SIZE // 2, MARGIN - 10, text=letter, font=("Arial", 10, "bold"), fill='#1E3A5F')
            self.canvas.create_text(MARGIN - 15, MARGIN + i * CELL_SIZE + CELL_SIZE // 2, text=number, font=("Arial", 10, "bold"), fill='#1E3A5F')
            self.canvas.create_text(px2 - 15, MARGIN + i * CELL_SIZE + CELL_SIZE // 2, text=number, font=("Arial", 10, "bold"), fill='#1E3A5F')
            for j in range(GRID_SIZE):  # 10x10 grid
                x1, y1 = px1 + j * CELL_SIZE, MARGIN + i * CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x1 + CELL_SIZE, y1 + CELL_SIZE, outline="#1E3A5F", width=1)
                x2, y2 = px2 + j * CELL_SIZE, MARGIN + i * CELL_SIZE
                self.canvas.create_rectangle(x2, y2, x2 + CELL_SIZE, y2 + CELL_SIZE, outline="#1E3A5F", width=1)
        self.draw_ships()
        if self.phase.startswith("placement") and self.preview_positions:
            self.draw_ship_preview()
        self.draw_attacks()

    def draw_ship_preview(self):
        px = MARGIN
        color = "#90EE90" if self.preview_valid else "#FF6B6B"
        for row, col in self.preview_positions:
            x = px + col * CELL_SIZE + 2
            y = MARGIN + row * CELL_SIZE + 2
            self.canvas.create_rectangle(x, y, x + CELL_SIZE - 4, y + CELL_SIZE - 4, fill=color, outline="black", width=2, stipple="gray50")

    def draw_ships(self):
        board = self.current_player.board if self.phase.startswith("placement") else self.current_player.board
        px = MARGIN
        if hasattr(board, 'ships'):
            for ship in board.ships:
                if ship.is_placed:
                    row, col = ship.position[0]
                    x = px + col * CELL_SIZE
                    y = MARGIN + row * CELL_SIZE
                    name = ship.__class__.__name__
                    orientation_suffix = "" if ship.orientation.value == "H" else "_V"
                    img_key = name + orientation_suffix
                    if img_key in self.images:
                        self.canvas.create_image(x, y, image=self.images[img_key], anchor="nw")
                    else:
                        for pos_row, pos_col in ship.position:
                            x = px + pos_col * CELL_SIZE + 2
                            y = MARGIN + pos_row * CELL_SIZE + 2
                            self.canvas.create_rectangle(x, y, x + CELL_SIZE - 4, y + CELL_SIZE - 4, fill="#8B4513", outline="black", width=2)

    def draw_attacks(self):
        if self.phase != "battle":
            return
        px1 = MARGIN  # Current player's board
        px2 = MARGIN + GRID_SIZE * CELL_SIZE + 60  # Opponent's attack grid
        # Draw attacks on opponent's attack grid (right)
        board = self.current_player.opponent_board
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                mark = board.grid[r][c]
                x = px2 + c * CELL_SIZE + CELL_SIZE // 2
                y = MARGIN + r * CELL_SIZE + CELL_SIZE // 2
                if mark == "X":
                    self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="red", outline="darkred", width=3)
                    self.canvas.create_text(x, y, text="💥", font=("Arial", 16))
                elif mark == "O":
                    self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="white", outline="blue", width=2)
        # Draw hits on current player's board (left)
        board = self.current_player.board
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                mark = board.grid[r][c]
                x = px1 + c * CELL_SIZE + CELL_SIZE // 2
                y = MARGIN + r * CELL_SIZE + CELL_SIZE // 2
                if mark == "X":
                    self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="red", outline="darkred", width=3)
                    self.canvas.create_text(x, y, text="💥", font=("Arial", 16))
                elif mark == "O":
                    self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="white", outline="blue", width=2)

    def select_ship(self, ship_name):
        if self.remaining_ships.get(ship_name, 0) > 0:
            self.selected_ship = ship_name
            self.status_label.config(text=f"{self.current_player.name}: Selected {ship_name} ({self.orientation}, press 'R' to rotate, move mouse to preview)")
        else:
            messagebox.showinfo("Ship Unavailable", f"No {ship_name}s left to place.")

    def toggle_orientation(self, event=None):
        self.orientation = "V" if self.orientation == "H" else "H"
        self.status_label.config(text=f"{self.current_player.name}: Selected {self.selected_ship or 'None'} ({self.orientation}, press 'R' to rotate, move mouse to preview)")

    def handle_keypress(self, event):
        if event.keysym.lower() == 'r':
            self.toggle_orientation()

    def handle_click(self, event):
        x, y = event.x, event.y
        if x < MARGIN or y < MARGIN:
            return
        if x < MARGIN + GRID_SIZE * CELL_SIZE:
            col = (x - MARGIN) // CELL_SIZE
            row = (y - MARGIN) // CELL_SIZE
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and self.phase.startswith("placement"):
                self.place_ship_on_board(row, col)
        elif x >= MARGIN + GRID_SIZE * CELL_SIZE + 60 and self.phase == "battle":
            col = (x - MARGIN - GRID_SIZE * CELL_SIZE - 60) // CELL_SIZE
            row = (y - MARGIN) // CELL_SIZE
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                self.attack_cell(row, col)

    def place_ship_on_board(self, row, col):
        if not self.selected_ship:
            messagebox.showinfo("No Ship Selected", "Please select a ship first.")
            return
        if not self.preview_valid:
            messagebox.showwarning("Invalid Placement", "Cannot place ship at this location.")
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
                self.clear_ship_preview()
                self.update_ship_buttons()
                if sum(self.remaining_ships.values()) == 0:
                    if self.phase == "placement_p1":
                        messagebox.showinfo("Player Switch", f"{self.player1.name}'s ships placed!\n\n{self.player2.name}, get ready to place your ships!")
                        Ship.reset_counters()
                        self.phase = "placement_p2"
                        self.current_player = self.player2
                        self.opponent = self.player1
                        self.remaining_ships = self.init_remaining_ships()
                        self.selected_ship = None
                        self.orientation = 'H'
                        self.clear_ship_preview()
                        self.update_ship_buttons()
                        self.status_label.config(text=f"{self.current_player.name}: Place your ships (click to place, press 'R' to rotate, move mouse to preview)")
                    else:
                        messagebox.showinfo("Battle Begins!", f"All ships placed!\n\n{self.player1.name} attacks first!")
                        self.phase = "battle"
                        self.current_player = self.player1
                        self.opponent = self.player2
                        self.ship_frame.destroy()
                        self.show_turn_transition()
                    self.draw_boards()
                else:
                    self.status_label.config(text=f"{self.current_player.name}: Select next ship to place (click to place, press 'R' to rotate, move mouse to preview)")
                    self.draw_boards()
        except ValueError as e:
            messagebox.showwarning("Invalid Placement", str(e))

    def attack_cell(self, row, col):
        result = self.opponent.board.receive_attack(row, col)
        if result == "repeat":
            messagebox.showinfo("Already Attacked", "You already attacked this position!")
            return
        if result == "hit":
            self.current_player.opponent_board.grid[row][col] = "X"
            hit_ship = None
            for ship in self.opponent.board.ships:
                for pos_row, pos_col in ship.position:
                    if pos_row == row and pos_col == col:
                        ship.hit()
                        hit_ship = ship
                        break
                if hit_ship:
                    break
            if hit_ship and hit_ship.is_sunk():
                messagebox.showinfo("Ship Sunk!", f"💥 {self.current_player.name} sunk {self.opponent.name}'s {hit_ship.__class__.__name__}!")
            else:
                messagebox.showinfo("Hit!", f"💥 {self.current_player.name} scored a hit!")
            self.status_label.config(text=f"🎯 {self.current_player.name} hit! Attack again!")
        else:
            self.current_player.opponent_board.grid[row][col] = "O"
            messagebox.showinfo("Miss!", f"💧 {self.current_player.name} missed!")
            self.current_player, self.opponent = self.opponent, self.current_player
            self.show_turn_transition()
            return
        self.draw_boards()
        if self.opponent.board.all_ships_sunk():
            self.phase = "game_over"
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<Motion>")
            self.show_game_over()

    def show_main_menu(self):
        self.clear_screen()
        self.phase = "start"
        self.setup_start_screen()

    def show_game_over(self):
        self.canvas.delete("all")
        self.game_frame.destroy()
        self.end_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.end_frame.pack(expand=True, fill='both')
        tk.Label(self.end_frame, text=f"🏆 {self.current_player.name} Wins! 🏆", font=("Arial", 24, "bold"), fg='#1E3A5F', bg=BG_COLOR).pack(pady=20)
        tk.Button(self.end_frame, text="Play Again", font=("Arial", 12), bg='#22C55E', fg='white', command=self.restart_game).pack(pady=10)
        tk.Button(self.end_frame, text="Quit", font=("Arial", 12), bg='#EF4444', fg='white', command=self.root.destroy).pack(pady=10)

    def restart_game(self):
        self.end_frame.destroy()
        Ship.reset_counters()
        self.player1.restart()
        self.player2.restart()
        self.current_player = self.player1
        self.opponent = self.player2
        self.remaining_ships = self.init_remaining_ships()
        self.selected_ship = None
        self.orientation = 'H'
        self.clear_ship_preview()
        self.phase = "placement_p1"
        self.setup_game_gui()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BattleshipGUI(root)
    root.mainloop()
