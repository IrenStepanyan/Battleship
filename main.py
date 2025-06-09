from game import BattleShipGame

def main():
    try:
        battleship = BattleShipGame()
        battleship.run()
    except ImportError as e:
        print(f"Error importing game modules: {e}")
        print("\nMake sure all game files are in the same directory.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
