
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox


CELL_SIZE = 50
GRID_SIZE = 10
SHIPS = {
    'Battleship': {'size': 4, 'image': 'Battleship.png', 'count': 1},
    'Cruiser': {'size': 3, 'image': 'Cruiser.png', 'count': 2},
    'Submarine': {'size': 2, 'image': 'Submarine.png', 'count': 3},
    'Destroyer': {'size': 1, 'image': 'Destroyer.png', 'count': 4}
}

class BattleshipGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Battleship Game")
        self.selected_ship = None
        self.orientation = 'horizontal'
        self.placed_ships = []
        self.available_ships = {name: info['count'] for name, info in SHIPS.items()}
        self.images = {}
        
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.player_frame = tk.Frame(self.main_frame)
        self.player_frame.pack(side=tk.LEFT, padx=20, pady=20)
        
        self.opponent_frame = tk.Frame(self.main_frame)
        self.opponent_frame.pack(side=tk.RIGHT, padx=20, pady=20)
        
        self.create_canvases()
        
        self.load_images()
        
        self.draw_boards()
        self.draw_ship_selection()
        
        self.player_canvas.bind("<Button-1>", self.handle_click)
        self.root.bind("<r>", self.rotate_ship)
        
        self.status_label = tk.Label(root, text="Select a ship below, then click on grid to place. Press 'R' to rotate.", 
                                   font=('Arial', 10))
        self.status_label.pack()
    
    def create_canvases(self):
        self.player_canvas = tk.Canvas(
            self.player_frame, 
            width=CELL_SIZE*GRID_SIZE, 
            height=CELL_SIZE*GRID_SIZE + 120,
            bg="white"
        )
        self.player_canvas.pack()
        
        self.opponent_canvas = tk.Canvas(
            self.opponent_frame,
            width=CELL_SIZE*GRID_SIZE,
            height=CELL_SIZE*GRID_SIZE,
            bg="white"
        )
        self.opponent_canvas.pack()
        
        tk.Label(self.player_frame, text="Your Fleet", font=('Arial', 12)).pack()
        tk.Label(self.opponent_frame, text="Enemy Waters", font=('Arial', 12)).pack()
    
    def load_images(self):
        try:
            water_img = Image.open("water.png")
            self.images['water'] = ImageTk.PhotoImage(water_img.resize(
                (CELL_SIZE*GRID_SIZE, CELL_SIZE*GRID_SIZE)))
            
            for name, info in SHIPS.items():
                img = Image.open(info['image'])
                
                if info['size'] > 1: 
                    width = CELL_SIZE * info['size']
                    height = CELL_SIZE
                    
                    img = img.resize((width, height), Image.LANCZOS)
                    self.images[name] = ImageTk.PhotoImage(img)
                   
                    vertical_img = img.rotate(90, expand=True)
                    self.images[f"{name}_vertical"] = ImageTk.PhotoImage(vertical_img)
                else:  
                    img = img.resize((CELL_SIZE, CELL_SIZE), Image.LANCZOS)
                    self.images[name] = ImageTk.PhotoImage(img)
                    
        except Exception as e:
            print(f"Error loading images: {e}")
            messagebox.showerror("Image Error", "Could not load game images!")
            self.root.destroy()
    
    def draw_boards(self):
        self.player_canvas.create_image(0, 0, image=self.images['water'], anchor='nw', tags="background")
        self.draw_grid(self.player_canvas)
        
        self.opponent_canvas.create_image(0, 0, image=self.images['water'], anchor='nw', tags="background")
        self.draw_grid(self.opponent_canvas)
    
    def draw_grid(self, canvas):
        for row in range(GRID_SIZE + 1):
            canvas.create_line(0, row * CELL_SIZE, GRID_SIZE * CELL_SIZE, row * CELL_SIZE, fill="black")
        for col in range(GRID_SIZE + 1):
            canvas.create_line(col * CELL_SIZE, 0, col * CELL_SIZE, GRID_SIZE * CELL_SIZE, fill="black")
    
    def draw_ship_selection(self):
        self.player_canvas.delete("ship_selection")
        start_y = GRID_SIZE * CELL_SIZE + 10
        
        for i, (name, info) in enumerate(SHIPS.items()):
            x = 10 + i * 120
            y = start_y
            
            outline = "yellow" if self.selected_ship == name else "black"
            width = 3 if self.selected_ship == name else 1
            
            if self.orientation == 'horizontal':
                self.player_canvas.create_image(x, y, image=self.images[name], anchor='nw', tags=("ship_selection", f"ship_{name}"))
                self.player_canvas.create_rectangle(x, y, x + info['size']*30, y + 30, 
                                          outline=outline, width=width, tags="ship_selection")
            else:
                img = self.images.get(f"{name}_vertical", self.images[name])
                self.player_canvas.create_image(x, y, image=img, anchor='nw', tags=("ship_selection", f"ship_{name}"))
                self.player_canvas.create_rectangle(x, y, x + 30, y + info['size']*30, 
                                          outline=outline, width=width, tags="ship_selection")
            
            self.player_canvas.create_text(x + 50, y + (info['size']*30 if self.orientation == 'vertical' else 30) + 15, 
                                  text=f"{name} ({self.available_ships[name]} left)",
                                  font=('Arial', 8), tags="ship_selection")
    
    def handle_click(self, event):
        if event.y > GRID_SIZE * CELL_SIZE:
            self.select_ship(event.x, event.y)
        elif self.selected_ship and self.available_ships[self.selected_ship] > 0:
            self.place_ship(event.x, event.y)
    
    def select_ship(self, x, y):
        start_y = GRID_SIZE * CELL_SIZE + 10
        
        for name, info in SHIPS.items():
            ship_x = 10 + list(SHIPS.keys()).index(name) * 120
            ship_y = start_y
            
            if self.orientation == 'horizontal':
                if (ship_x <= x <= ship_x + info['size']*30) and (ship_y <= y <= ship_y + 30):
                    if self.available_ships[name] > 0:
                        self.selected_ship = name
                    else:
                        messagebox.showinfo("No Ships Left", f"You've placed all available {name}s")
                    break
            else:
                if (ship_x <= x <= ship_x + 30) and (ship_y <= y <= ship_y + info['size']*30):
                    if self.available_ships[name] > 0:
                        self.selected_ship = name
                    else:
                        messagebox.showinfo("No Ships Left", f"You've placed all available {name}s")
                    break
        else:
            self.selected_ship = None
        
        self.draw_ship_selection()
    
    def place_ship(self, x, y):
        col = x // CELL_SIZE
        row = y // CELL_SIZE
        ship_info = SHIPS[self.selected_ship]
        ship_size = ship_info['size']
        
        if (self.orientation == 'horizontal' and col + ship_size > GRID_SIZE) or \
           (self.orientation == 'vertical' and row + ship_size > GRID_SIZE):
            messagebox.showwarning("Invalid Position", "Ship doesn't fit there!")
            return
        
        for ship in self.placed_ships:
            s_name, s_row, s_col, s_size, s_orient = ship
            
            if self.orientation == 'horizontal' and s_orient == 'horizontal':
                if row == s_row and not (col + ship_size <= s_col or col >= s_col + s_size):
                    messagebox.showwarning("Invalid Position", "Ships overlap!")
                    return
            elif self.orientation == 'horizontal' and s_orient == 'vertical':
                if (s_col <= col < s_col + 1) and (row <= s_row + s_size - 1) and (row >= s_row):
                    messagebox.showwarning("Invalid Position", "Ships overlap!")
                    return
            elif self.orientation == 'vertical' and s_orient == 'horizontal':
                if (col <= s_col + s_size - 1) and (col >= s_col) and (s_row <= row < s_row + 1):
                    messagebox.showwarning("Invalid Position", "Ships overlap!")
                    return
            elif self.orientation == 'vertical' and s_orient == 'vertical':
                if col == s_col and not (row + ship_size <= s_row or row >= s_row + s_size):
                    messagebox.showwarning("Invalid Position", "Ships overlap!")
                    return
        
        self.placed_ships.append((self.selected_ship, row, col, ship_size, self.orientation))
        self.available_ships[self.selected_ship] -= 1
        
        self.draw_ship_on_grid()
        
        self.update_status()
        
        self.selected_ship = None
        self.draw_ship_selection()
    
    def draw_ship_on_grid(self):
        self.player_canvas.delete("ship")
        for ship in self.placed_ships:
            name, row, col, size, orientation = ship
            
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            
            if orientation == 'horizontal':
                self.player_canvas.create_image(x, y, image=self.images[name], anchor='nw', tags="ship")
            else:
                vertical_img_name = f"{name}_vertical"
                if vertical_img_name in self.images:
                    self.player_canvas.create_image(x, y, image=self.images[vertical_img_name], anchor='nw', tags="ship")
                else:
                    self.player_canvas.create_rectangle(x, y, x + CELL_SIZE, y + size * CELL_SIZE, 
                                              fill="gray", outline="black", tags="ship")
    
    def rotate_ship(self, event):
        if self.selected_ship:
            self.orientation = 'vertical' if self.orientation == 'horizontal' else 'horizontal'
            self.draw_ship_selection()
    
    def update_status(self):
        remaining = sum(self.available_ships.values())
        if remaining == 0:
            self.status_label.config(text="All ships placed! Ready to play.")
        else:
            self.status_label.config(text=f"Place your ships ({remaining} remaining). Select ship, click grid. Press 'R' to rotate.")

if __name__ == "__main__":
    root = tk.Tk()
    game = BattleshipGame(root)
    root.mainloop()