import tkinter as tk
from gui_test import BattleshipGUI

def main():
    root = tk.Tk()
    root.configure(bg='#F4A460')  # Sand-colored background
    app = BattleshipGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
