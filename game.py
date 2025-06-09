import os
from Board import Board
from Player import Player
from Ship import Ship, Battleship, Cruiser, Submarine, Destroyer

class BattleShipGame:

    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.current_player = None
        self.opponent = None
        self.game_over = False
        self.winner = None

    def clean_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def create_fleet(self):
        fleet = []
        try:
            fleet.append(Battleship())
            for _ in range(2):
                fleet.append(Cruiser())
            for _ in range(3):
                fleet.append(Submarine())
            for _ in range(4):
                fleet.append(Destroyer())
        except ValueError as e:
            print(f"Error creating fleet: {e}")
            return None
        return fleet

    def welcome(self):
        print("=" * 50)
        print("Welcome to BattleShip Game") 
        print("=" * 50)
        print("Rules:")
        print("1. Each player places 10 ships: 1 Battleship(4), 2 Cruiser(3), 3 Submarine(2), 4 Destroyer(1)")
        print("2. Players take turns to attack the opponent's board")
        print("3. If you hit, you opponent skips the move") 
        print("4. First to sink all enemy ships wins")
        print("Good luck!")
        print("=" * 50)

    def name_player(self):
        print("\nRegister the Players")
        player1_name = input("Enter Player1's name: ").strip()
        player2_name = input("Enter Player2's name: ").strip()

        if not player1_name:
            player1_name = "Player 1"
        if not player2_name:
            player2_name = "Player 2"
        
        return player1_name, player2_name

    def setup_players(self):
        Ship.reset_counters()

        player1_name, player2_name = self.name_player()

        player1_board = Board()
        player1_opponent_board = Board()
        player2_board = Board()
        player2_opponent_board = Board()

        player1_fleet = self.create_fleet()
        if player1_fleet is None:
            return False
        
        Ship.reset_counters()
        player2_fleet = self.create_fleet()
        if player2_fleet is None:
            return False

        self.player1 = Player(player1_name, player1_board, player1_opponent_board, player1_fleet)
        self.player2 = Player(player2_name, player2_board, player2_opponent_board, player2_fleet)
        return True

    def ship_placement_phase(self):
        print(f"\n{self.player1.name} place your ships")
        input("Press Enter when ready")
        self.clean_screen()
        self.player1.place_ships()

        input(f"\n{self.player1.name}'s ships are placed.\nPress Enter to continue")
        self.clean_screen()

        print(f"\n{self.player2.name} place your ships")
        input("Press Enter when ready")
        self.clean_screen()
        self.player2.place_ships()

        input(f"\n{self.player2.name}'s ships are placed\nPress Enter to start the game")
        self.clean_screen()
        
    def battle_phase(self):
        print("Let the Battle begin!")
        self.current_player = self.player1
        self.opponent = self.player2

        while not self.game_over:
            print(f"\n{'='*20} {self.current_player.name}'s Turn {'=' * 20}")
            result = self.current_player.make_attack(self.opponent)

            if self.opponent.board.all_ships_sunk():
                self.game_over = True
                self.winner = self.current_player
                break
                
            if result == 'hit':
                print(f"\n{self.current_player.name} gets another move")
                input("Press Enter to continue")
            else:
                self.current_player, self.opponent = self.opponent, self.current_player
                input(f"\n{self.current_player.name} takes the turn.\nPress Enter when ready.")
                self.clean_screen()

    def display_game_over(self):
        print(f"\nGame Over!!!")
        print(f"\nCongrats {self.winner.name}! You WIN!")
        loser = self.player1 if self.winner == self.player2 else self.player2
        print(f"\nGood luck for the next one {loser.name}! You LOST!")

    def play_again(self):
        while True:
            choice = input("\nAnother round? (y/n): ").lower().strip()
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no")

    def reset_game(self):
        self.player1 = None
        self.player2 = None
        self.current_player = None
        self.opponent = None
        self.game_over = False
        self.winner = None
        
    def start_game(self):
        if not self.setup_players():
            print("Error setting up players.")
            return False
        try:
            self.ship_placement_phase()
            self.battle_phase()
            self.display_game_over()
            return True

        except KeyboardInterrupt:
            print("\n\nGame interrupted.")
            return False
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            return False

    def run(self):
        self.welcome()
        
        while True:
            if self.start_game():
                if not self.play_again():
                    print("\nThanks for playing")
                    break
                else:
                    self.clean_screen()
                    print("Starting new game..")
                    self.reset_game()
            else:  # failed to start
                if not self.play_again():	
                    break
                else:
                    self.reset_game()

    def get_game_status(self):
        if not self.player1 or not self.player2:
            return None

        return {
            'player1_name': self.player1.name,
            'player2_name': self.player2.name, 
            'current_player': self.current_player.name if self.current_player else None,
            'game_over': self.game_over,
            'winner': self.winner.name if self.winner else None
        }
