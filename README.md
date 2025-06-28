# Battleship Game in Python
A classic Battleship game implemented in Python using Object-Oriented Programming principles. This project offers both a terminal-based version and a graphical user interface (GUI) version built with Tkinter. Play against another player and try to sink all their ships!

## 📁 Project Structure
<pre>
<b>Battleship/</b>
├── assets/               # Contains image files for GUI (water.png, Battleship.png, etc.)
├── Board.py              # Manages the game board, hit/miss logic, and display
├── Ship.py               # Defines ship properties like size, position, and hits
├── Player.py             # Represents each player and their actions
├── game.py               # Main game loop for console version
├── main.py               # Entry point (GUI or console, configurable)
├── gui_test.py           # GUI implementation using Tkinter
├── requirements.txt      # Lists dependencies for the GUI version
└── README.md             # You're reading it!
</pre>

## Getting Started
### Prerequisites

- Python 3.6 or higher installed on your system.
- For the GUI version, install dependencies listed in requirements.txt <i>(see below)</i>

### Run the Game

1. Clone the repository:

```bash
git clone https://github.com/IrenStepanyan/Battleship.git
cd Battleship
````

2. Install dependencies for the GUI version:
```bash
sudo apt update
sudo apt install python3-tk
```

```bash
pip install -r requirements.txt
```

3. Ensure the assets/ folder contains the required images:

- water.png
- Battleship.png
- Cruiser.png
- Submarine.png
- Destroyer.png


4. Run the main script:
```bash
python main.py
```

<i>For the Console Version comment the main.py code and uncomment the part that is now commented.</i>

## 🎮 Gameplay Overview

* The game is played on a 10x10 grid.
* Each player places their ships on the board.
* Players take turns firing at coordinates (e.g.,5 A).
* The goal is to sink all enemy ships by guessing their positions.

## Main Components
### `Board.py`

* Handles:

  * Creating and displaying the board
  * Tracks hits, misses, and ship placements.
  * Validates ship placements

### `Ship.py`

* Handles:

  * Defines ship properties: size, coordinates, orientation (horizontal/vertical)
  * Tracks hits and checks if a ship is sunk.
  * Resets counters for new games or player switches.

### `Player.py`

* Handles:

  * Manages player data: name, board, and attack board.
  * Handles ship placement and attack coordinates.

### `game.py`

* Orchestrates the console version game flow:

  * Initializes players and boards
  * Controls turn logic
  * Declares the winner

### gui_test.py

* Implements the GUI version using Tkinter:

  * Displays two 10x10 grids side-by-side.
  * Supports ship placement with mouse-based preview and rotation.
  * Handles attacks with visual feedback and turn transitions.
  * Includes start screen, end screen, and main menu navigation.

### main.py
* Entry point for the game.
  * Configurable to run either the GUI or console version (see Console Version).
  * Default: Launches the GUI

## Features

* Two-Player Mode: Play against another player on the same device.
* 10x10 Grid: Standard Battleship grid with A–J and 0–9 coordinates.

* GUI Version:
  * Interactive ship placement with green/red preview.
  * Visual attack feedback (hits/misses).
  * Turn transition window for clear player switches.
  * User-friendly interface with start/end screens.

* Console Version:
  * Input validation for coordinates and ship placements.
  * Board visualization in the terminal.
  * Hit/miss feedback and win detection.

## Future Improvements

* [ ] Add sound effects for hits, misses, and ship sinking.
* [ ] Save game statistics (e.g., wins, total games played).
* [ ] Implement an AI opponent for single-player mode.
* [ ] Option to choose an element (e.g ship, airplane).
