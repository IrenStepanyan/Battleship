import tkinter as tk
from gui_test import BattleshipGUI

def main():
    root = tk.Tk()
    game = BattleshipGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

