from SaboteurPlayer import SaboteurPlayer
from card import PathCard, ActionCard, GoalCard, StartingCard
from agent_programs import mcts_agent_program
from saboteur_base_environment import SaboteurBaseEnvironment
from game_board import GameBoard
import random

class GameLogic:
    def __init__(self):
        self.sabenv = SaboteurBaseEnvironment(mcts_agent_program)  # Pass an instance of SaboteurBaseEnvironment
        self.players = self.initialize_players()
        self.current_player_index = 0
        self.game_board = self.sabenv._board  # Initialize from sabenv_instance

    def initialize_game(self):
        print ("Initializing game...")
        # print ("Setting up game board...")
        self.game_board = self.sabenv._board
        num_players = len(self.players)
        roles = ['Gold-Digger'] * (num_players - 2) + ['Saboteur'] * 2
        random.shuffle(roles)
        
        for i, player in enumerate(self.players):
            player.add_all_sensors()
            # print(f"Player {i + 1}'s sensors before setting role: {player._sensors}")
            
            if 'role-sensor' not in player._sensors:
                player._sensors['role-sensor'] = {'type': 'string', 'value': None}
            
            player._sensors['role-sensor']['value'] = roles[i]
            # print(f"Player {i + 1}'s role is {roles[i]}")
            # print(f"Player {i + 1}'s sensors after setting role: {player._sensors}")

            self.sabenv.draw_initial_cards(player)
            player._sensors['sabotaged'] = {'type': 'boolean', 'value': False}
            # print(f"Player {i + 1}'s sensors after drawing cards: {player._sensors}")
        
        # Place the three special goal cards at coordinates (14, 8), (14, 10), and (14, 12)
        goal_positions = [(14, 8), (14, 10), (14, 12)]
        goal_cards = [GoalCard("gold"), GoalCard("stone"), GoalCard("stone")]
        #draw on the board the cards on the board at the x and y locations listed in goal_positions
        random.shuffle(goal_cards)
        
        
        for position, card in zip(goal_positions, goal_cards):
            self.game_board.add_path_card(position[0], position[1], card, skip_validation=True)
                
                
    def initialize_players(self):
        num_saboteurs = random.choice([2, 3])
        role_pool = ['Gold-Digger'] * (8 - num_saboteurs) + ['Saboteur'] * num_saboteurs
        random.shuffle(role_pool)
        players = [SaboteurPlayer(f'Player {i + 1}', mcts_agent_program, role_pool[i]) for i in range(8)]
        return players

    # Initialize roles
    def initialize_roles(self, players):
        for player in players:
            player._sensors['role-sensor']['value'] = 'Some Role'

    # Initialize hands
    def initialize_hands(self, players):
        for player in players:
            player._sensors['hand-sensor']['value'] = 'Some Initial Cards'

    # Validate actions
    def validate_action(self, action, player):
        if action == 'discard-card' and not player._sensors['hand-sensor']['value']:
            print("Cannot discard from an empty hand.")
            return False
        return True



    
        
    def choose_position(self, chosen_card):
        """
        Asks the user to choose a position for the chosen card.
        
        Args:
            chosen_card: The chosen PathCard object.
            
        Returns:
            tuple: The chosen position (x, y) or None if no valid position is found.
        """
        
        legal_positions = self.sabenv.find_legal_positions(chosen_card)
        print(f"Debug: Legal positions are {legal_positions}")

        # Filter out positions that do not pass the tunnel validation
        valid_positions = []
        for pos in legal_positions:
            x, y = pos
            neighbors = self.sabenv.get_neighbors(x, y)
            is_valid = True
            for relative_position, neighbor_card in neighbors.items():
                if neighbor_card is not None:
                    print(f"Debug: Checking neighbor at {relative_position} with card {neighbor_card}")
                    if not GameBoard.can_connect(chosen_card, neighbor_card, relative_position):
                        print(f"Debug: Cannot connect with neighbor at {relative_position}")
                        is_valid = False
                        break
            if is_valid:
                valid_positions.append(pos)
                print(f"Debug: Valid positions are {valid_positions}")
       
        if not valid_positions:
            print("No valid positions found for this card.")
            return None
        
        print("Valid positions:")
        for idx, position in enumerate(valid_positions):
            print(f"{idx + 1}. {position}")
        
        choice = int(input("Please enter the number of your chosen position: ")) - 1
        
        return valid_positions[choice]

    
    def choose_target_player(self):
        # Assuming you have a list of players, randomly choose one to be the target
        target_player = random.choice(self.players)
        return target_player

    
    def choose_card(self, current_player):
        cards_in_hand = current_player._sensors['hand-sensor']['value']
        print("Cards in your hand:")
        for idx, card in enumerate(cards_in_hand):
            print(f"{idx + 1}. {card}")
            
        choice = mcts_agent_program(current_player, self.sabenv)
        # Check if the 'game-board-sensor' key exists in the game state
        if 'game-board-sensor' in self.sabenv.game_state:
            # Retrieve the game board value
            current_game_board = self.sabenv.game_state['game-board-sensor']['value']
            
            # Print the game board (you may need to implement a __str__ method in your game board class for this)
            print("Current game board:", current_game_board)
        else:
            # Print an error message if the key doesn't exist
            print("Error: 'game-board-sensor' key not found in game state.")
        chosen_card = cards_in_hand[choice]
        
        return chosen_card


