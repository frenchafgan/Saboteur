from une_ai.models.game_environment import GameEnvironment
from card import PathCard, ActionCard, GoalCard
from SaboteurPlayer import SaboteurPlayer
from game_board import GameBoard
from deck import Deck

from copy import deepcopy, copy
import random
from MCTSAgent import MCTSAgent
import sys



class SaboteurBaseEnvironment(GameEnvironment):
    def __init__(self, num_players=8):  # Number of players is always 8
        from agent_programs import mcts_agent_program
        sys.setrecursionlimit(10000)

       # Initialize game board and deck
        self._board = GameBoard()
        self.deck = Deck()
        self.discard_pile = []      

        # Get the grid map from the game board
        self.board = GameBoard.get_grid_map(self)
        
        # Create a pool of roles and randomly select 8 roles from the pool
        role_pool = ['Gold-Digger'] * 6 + ['Saboteur'] * 3
        num_players = 8

        selected_roles = random.sample(role_pool, num_players)

        # Initialize players
        self.players = []
        self.current_player_index = 0

        for index, role in enumerate(selected_roles):
            # mcts_agent_instance = MCTSAgent(role, mcts_agent_program, num_simulations=1000, ucb1_const=2)
            player_instance = SaboteurPlayer(f'Player {index + 1}',  role) #mcts_agent_program,
            # Distribute cards and set initial game state
         # Distribute cards and set initial game state
            for giveCard in range(0, 4):
                self.draw_card(player_instance)
            self.players.append(player_instance)
        
        self.rounds = 0
        self.scores = {}
        
        self._sensors = {
            'game-board-sensor' : { 'value':[] }, 
            'role-sensor' : { 'value':[] }, 
            'turn-taking-indicator' : { 'value':[] }, 
            'hand-sensor' : { 'value':[] }, 
        }
        
        # Initialize the current player and update sensors
        self.current_player = self.players[self.current_player_index]
        
    def is_terminal(self):
        #check to see if players have cards in their hands
        for player in self.players:
            if len(player._sensors['hand-sensor']) == 0:
                return True
       
        # Check if the gold goal card is revealed
        for x, y in [(14, 8), (14, 10), (14, 12)]:
            card = (x, y)
            if isinstance(card, GoalCard) and card.is_gold and card.reveal_card():
                return True

        # Check if the deck is empty
        if len([Deck.get_deck]) == 0:
            return True
        return False

    def draw_card(self, player):
        # print(f"Type of player object: {type(player)}")
        # print(f"Value of player object: {player}")
        # Safety Check: If 'hand-sensor' doesn't exist, create it
        if 'hand-sensor' not in player._sensors:
            player._sensors['hand-sensor'] = {'type': 'list', 'value': []}
            
        if not self.deck.is_empty():
            new_card = self.deck.draw()
            player.hand.append(new_card)
    
    
    def get_legal_actions():

        cards = SaboteurBaseEnvironment.get_player.hand

        validCardPlacements = {}

        for card in cards:
            for x in range(0, 20):
                for y in range(0,20):
                    if SaboteurBaseEnvironment._board.check_path_card(x,y, card):
                        if card not in validCardPlacements:
                            validCardPlacements[card] = []
                        validCardPlacements[card].append((x,y,0))
                    
                    #Rotate and do the same
                    card.turn_card()
                    if SaboteurBaseEnvironment._board.check_path_card(x,y, card):
                        if card not in validCardPlacements:
                            validCardPlacements[card] = []
                        validCardPlacements[card].append((x,y,1))
                    
                    #Rotate it back, so we know that position 0, is this position
                    card.turn_card()



        return validCardPlacements 
    
    
    
    
    
    


    def get_game_state(self):
        # Initialize an empty list to hold player information
        player_info = []
        
        # Loop through each player in self._players to collect their information
        for player in self.players:
            player_dict = {
                'name': player._agent_name,
                'role': player.role,
                'hand': player.hand
            }
            player_info.append(player_dict)
        
        # Construct the game_state dictionary
        game_state = {
            'game-board-sensor': {'value': ['game-board'], 'validation-function': lambda x: True},
            'deck': self.deck,
            'rounds': self.rounds,
            'scores': self.scores,
            'current_player_index': self.current_player_index,  # Added this line to include current_player_index in game_state
            'players': player_info
        }
        
        return game_state



    def get_player_hand(self):
        current_player = self.current_player
        # print(f"Debug: _sensors = {self._sensors}")  # Debug statement
        hand = self._sensors.get('hand-sensor', {}).get('value', [])

        # print("Debug: Inside get_player_hand with current_player = ", current_player)
        if current_player is None:
            print("No current player found.")
            return None
        
        if not hasattr(current_player, '_sensors'):
            print("The current player object does not have an attribute '_sensors'")
            return None

        if 'hand-sensor' not in current_player._sensors:
            print("The '_sensors' attribute does not contain 'hand-sensor'")
            return None
        
        print("Debug: hand = ", hand)
        return hand









    # def get_legal_actions(self, current_player):
    #     # try:
    #     #     # Extract current player's dictionary from game_state
    #     # current_player_dict = self.game_state.players
    #     # except KeyError as e:
    #     #     print(f"KeyError: {e} not found in game_state")
    #     #     return []
            
    #     # Extract agent programa
    #     agent = self.current_player._agent_program
        
    #     # Create a SaboteurPlayer object from the dictionary (if necessary)
    #     current_player = SaboteurPlayer(
    #         agent_name=current_player,
    #         agent_program=agent,
    #         role=current_player
    #     )
        
    #     # Update the hand sensor for the current player
    #     current_player.hand = current_player._sensors['hand-sensor']['value']
        
    #     # Get available actions
    #     available_actions = current_player._actions
        
    #     return available_actions  # Changed from self.available_actions


    def find_legal_positions(self, path_card):
        # print ("Debug: Inside find_legal_positions with path_card = ", path_card)
        legal_positions = []
        for x in range(0, 20):
            for y in range(0, 20):
                existing_card = self.board.get_grid_map().get_item_value(x, y)
                if existing_card:  # check if there is an existing card at (x, y)
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        new_x, new_y = x + dx, y + dy
                        # Check if the new coordinates are within the board limits
                        if 0 <= new_x < 20 and 0 <= new_y < 20:
                            # Check if the new position is empty
                            if self.board.get_grid_map().get_item_value(new_x, new_y) is None:
                                # Check if the new card can connect to the existing card
                                if self.is_legal_position(new_x, new_y, path_card, existing_card):
                                    legal_positions.append((new_x, new_y))
        return legal_positions

    def get_available_actions(self, player):
        #initialize role
        #initialize hand
        # print(self.get_player_hand())
        


        role = self._sensors['role-sensor']['value']
        hand = self._sensors['hand-sensor']['value']
        # print("Debug: Inside get_available_actions with player = ", player)
        path_cards_in_hand = [card for card in hand if isinstance(card, PathCard)]
        # print ("Debug: path_cards_in_hand = ", path_cards_in_hand)
        action_cards_in_hand = [card for card in hand if isinstance(card, ActionCard)]
        
        # print ("Debug: action_cards_in_hand = ", action_cards_in_hand)
        # print(f"Debug: Role is {role}")
        # print(f"Debug: Hand is {hand}")
        
   
        legal_positions = []
        available_actions = []
        

        for card in path_cards_in_hand:
            legal_positions.extend(self.find_legal_positions(card))

        if legal_positions:
            available_actions.append('place-path-card')
        if action_cards_in_hand:
            available_actions.append('use-action-card')
        #print list of legal positions
        # print(f"Debug: Legal positions are {legal_positions}")
        

        if not available_actions:
            available_actions.append('discard-card')
        else:
            available_actions.append('pass-turn')

        # print(f"Debug: Available actions are {available_actions}")
        
        
        return self.available_actions





    def apply_action(self, game_state, player, agent, action):
        # print(f"Debug: Inside apply_action with action = {action}")
        card_to_discard = self.choose_card_to_discard(game_state, player)

        if action == 'place-path-card':
            if not self.place_path_card(agent, player):
                GameBoard.handle_invalid_placement(player, game_state)
            else:
                self.discard_card(player, card_to_discard)
                self.draw_card(player)
                    
        elif action == 'use-action-card':
            if not self.use_action_card(player, game_state):
                GameBoard.handle_invalid_placement(player, game_state)
            else:
                self.discard_card(player)
                self.draw_card(player)
                    
        elif action == 'pass-turn':
            card_to_discard = self.choose_card_to_discard(game_state, player)
            self.pass_turn(player)
            self.discard_card(player)
            self.draw_card(player)
                
        else:
            print("Invalid action.")




    def calculate_card_value(self, card, role, game_board_state):
        print ("Debug: Inside calculate_card_value with card = ", card, "role = ", role, "game_board_state = ", game_board_state)
        if role == 'Gold-Digger':
            if isinstance(card, PathCard):
                # Heuristic: A PathCard is more valuable if it extends a path towards the goal
                return self.evaluate_path_extension(card, game_board_state)
            elif isinstance(card, ActionCard):
                # Heuristic: An ActionCard might be valuable based on its action type
                return self.evaluate_action_card_for_gold_digger(card)
        elif role == 'Saboteur':
            if isinstance(card, PathCard):
                # Heuristic: A PathCard is valuable if it blocks a path towards the goal
                return self.evaluate_path_blockage(card, game_board_state)
            elif isinstance(card, ActionCard):
                # Heuristic: An ActionCard might be valuable based on its action type
                return self.evaluate_action_card_for_saboteur(card)
        return 0  # Default case or for unknown card types
    
    
    def discard_card(self, player, card_to_discard):
        # print ("Debug: Inside discard_card with card_to_discard = ", card_to_discard)
        # print("Player's hand before removal:", self._sensors['hand-sensor']['value'])
        print("Card to discard:", card_to_discard)
        #print gameboard to see what cards are in the players hand
        print("Gameboard:", self.game_board)
        
        if card_to_discard in self._sensors['hand-sensor']['value']:
            player['hand-sensor']['value'].remove(card_to_discard)
        else:
            print("Card not found in player's hand.")
        
    def use_action_card(self, current_player, game_board, card, target):
        # print ("Debug: Inside use_action_card with card = ", card, "target = ", target)
        # Get the action cards in the player's hand
        action_cards = [card for card in current_player._sensors['hand-sensor']['value'] if isinstance(card, ActionCard)]
        
        if not action_cards:
            print(f"{current_player._agent_name} has no Action Cards to use.")
            return False

        card_to_use = action_cards[0]  # You might want to extend this logic to allow the player to choose which action card to use.
        current_player._sensors['hand-sensor']['value'].remove(card_to_use)

        card_action = card_to_use._action  # I'm assuming _action holds the type of action ('map', 'dynamite', 'sabotage', 'mend')

        if card_action == 'map':
            # Implement logic for the Map card.
            chosen_goal_position = self.choose_goal_card(game_board)  # New function
            print(f"Chosen Goal Position: {chosen_goal_position}")

        elif card_action == 'dynamite':
            # Implement logic for the Dynamite card.
            x, y = self.choose_path_card_to_remove(game_board)  # New function
            game_board.remove_path_card(x, y)

        elif card_action == 'sabotage':
            # Implement logic for the Sabotage card.
            target_player = self.choose_target_player()  # New function
            target_player._sensors['sabotaged']['value'] = True

        elif card_action == 'mend':
            # Implement logic for the Mend card.
            target_player = self.choose_target_player()  # New function
            target_player._sensors['sabotaged']['value'] = False
        else:
            print("Invalid action card.")
            return False
        return True
    
    
    
            
    def update_to_next_player(self):
        
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.current_player = self.players[self.current_player_index]
        
    def get_next_player(self):
        # current_player_index = self.players.index(self.current_player)
        next_player_index = (self.current_player_index + 1) % len(self.players)
        return self.players[next_player_index]
    
    def add_player(self, player):
        self.players.append(player)
        self.scores[player] = 0
           
    def get_players(self):
        return self.players

    def get_winner(self):
        # if GameBoard.dfs_gold_found():
        if PathCard.reveal_card(self):
            return "Gold-Digger"
        else:
            return "Saboteur"

    def choose_goal_card(self, game_board):
        goal_positions = [(14, 8), (14, 10), (14, 12)] 
        chosen_goal_position = random.choice(goal_positions)
        return chosen_goal_position

    def choose_path_card_to_remove(self, game_board):
        # print ("Debug: Inside choose_path_card_to_remove with game_board = ", game_board)
        # Randomly choose a path card to remove (excluding special cards)
        x, y = random.randint(0, 19), random.randint(0, 19)
        while game_board.get_grid_map().get_item_value(x, y) is None or game_board.get_grid_map().get_item_value(x, y).is_special_card():
            x, y = random.randint(0, 19), random.randint(0, 19)
        return (x, y)
        
        
        
    def choose_card_to_discard(self, game_state, current_player_index):
        hand = self.get_player_hand()
        if hand is None:
            print("No hand found for the current player.")
            return None
        
        # Evaluate the value of each card in the hand
        hand_values = [(card, self.calculate_card_value(card, self.role, game_state)) for card in hand]

        # Sort by value
        hand_values.sort(key=lambda x: x[1])

        # Choose the card with the lowest value to discard
        card_to_discard = hand_values[0][0]

        return card_to_discard

    def choose_target_player(self):
        # Assuming you have a list of players, randomly choose one to be the target
        target_player = random.choice(self.players)
        return target_player


    def place_path_card(self, player, agent):
        # Step 1: Check if the player has any PathCards in their hand
        path_cards = [card for card in player['hand-sensor']['value'] if isinstance(card, PathCard)]
        if not path_cards:
            print("No PathCards in hand to place.")
            return False

        # Step 2: Find legal positions for all PathCards in hand
        legal_positions_dict = {}
        for card_idx, path_card in enumerate(path_cards):
            legal_positions = self.find_legal_positions(path_card)
            legal_positions_dict[card_idx] = legal_positions
        
        # Step 3: Prompt the user to select one of the legal positions and cards to place
        for card_idx, positions in legal_positions_dict.items():
            print(f"For card {card_idx}:")
            if not positions:
                print("  No legal positions to place this PathCard.")
            else:
                print("  Legal positions:")
                for i, pos in enumerate(positions):
                    print(f"  {i}. {pos}")

        chosen_card_index = int(input("Choose the index of the card you want: "))
        chosen_position_index = int(input("Choose the index of the position you want: "))
        
        # Check if the chosen indexes are valid
        if chosen_card_index not in legal_positions_dict or chosen_position_index >= len(legal_positions_dict[chosen_card_index]):
            print("Invalid choice. Please choose again.")
            return False

        # Step 4: Place the chosen card at the chosen position
        chosen_card = path_cards[chosen_card_index]
        chosen_x, chosen_y = legal_positions_dict[chosen_card_index][chosen_position_index]
        self.game_board.add_path_card(chosen_x, chosen_y, chosen_card)
        
        # Step 5: Update the game state (if needed)
        print(f"{player} placed a Path Card at coordinates ({chosen_x}, {chosen_y}).")
        print("Board after placing the card:")
        print(self.game_board)
        
        return True



    def is_legal_position(self, x, y, new_card, existing_card):
        # Mapping opposite directions to be checked for alignment
        opposite_directions = {
            'north': 'south',
            'south': 'north',
            'east': 'west',
            'west': 'east'
        }
        
        # Check if tunnels in existing_card align with tunnels in new_card
        for direction, opposite in opposite_directions.items():
            for tunnel in existing_card.get_tunnels():
                if direction in tunnel:
                    for new_tunnel in new_card.get_tunnels():
                        if opposite in new_tunnel:
                            return True
        return False


    def pass_turn(self, player):
        print(f"{player} passed their turn.")

    def copy(self):
        # Create a new environment object
        new_env = SaboteurBaseEnvironment()
        
        # Deep copy the game board and deck
        new_env.game_board = deepcopy(self._board)
        new_env.deck = deepcopy(self.deck)
        
        # Deep copy players if they have a copy method, otherwise just reference them
        new_env.players = [player.copy() if hasattr(player, "copy") else deepcopy(player) for player in self._players]
        
        # Copy other attributes
        new_env.current_player_index = self.current_player_index
        new_env.rounds = self.rounds
        new_env.scores = deepcopy(self.scores)
        
        return new_env

    # def transition_result(self,game_state):
    #     current_player = self.current_player_index
    #     game_board = self.board
    #     deck = self.deck
        

    #     # Draw a new card for the player if the deck is not empty
    #     if not Deck.is_empty(self):
    #         new_card = deck.draw()
    #         current_player.hand.append(new_card)
            
    #     new_game_state = game_state.copy()
      
        
    #     # Update scores if the game is terminal
    #     if self.is_terminal():
    #         winners = SaboteurBaseEnvironment.get_winner(new_game_state)
    #         for winner in winners:
    #             new_game_state['scores'][winner] += 1
        
    #     return new_game_state
            
    # def transition_result(self, game_state):
    # #     # Check if 'current_player_index' and 'players' are in game_state
    # #     # 'current_player_index' not in self.game_state or 'players' not in self.game_state

    # #     current_player_index = game_state['current_player_index']
    # #     current_player = game_state['players'][current_player_index]

    # #     game_board = self.board
    # #     deck = self.deck

    # #     # Draw a new card for the player if the deck is not empty
    # #     if not Deck.is_empty(self):
    # #         new_card = deck.draw()
    # #         current_player['hand'].append(new_card)  # Append new card to the current player's hand

    # #     new_game_state = game_state.copy()

    # #     # Update scores if the game is terminal
    # #     if self.is_terminal():
    # #         winners = SaboteurBaseEnvironment.get_winner(new_game_state)
    # #         for winner in winners:
    # #             new_game_state['scores'][winner] += 1

    # #     return new_game_state
    #     pass

    def transition_result(current_state, action):
            """
            Takes the current game state and an action, and returns the new game state after applying the action.
            """
            # Make a deep copy of the current state to avoid modifying it directly
            new_state = deepcopy(current_state)

            # Extract relevant information from the current state
            board = new_state.board
            deck = new_state.deck
            rounds = new_state.rounds
            scores = new_state.scores
            current_player_index = new_state.current_player_index
            players = new_state.players

            # Validate that all necessary keys exist
            if board is None or deck is None or rounds is None or scores is None:
                # raise Exception("Missing current_player_index or players in game_state")
                pass

            # Apply the action to update the game state
            action_type = []
             
            if action_type == 'place_card':
                x, y = action[1], action[2]
                card_to_place = deck.pop()  # Assuming the top card in the deck is the one to be placed
                board[x][y] = card_to_place  # Place the card on the board

            elif action_type == 'draw_card':
                # Draw a card from the deck and give it to the current player
                drawn_card = deck.pop()
                players[current_player_index]['hand'].append(drawn_card)

            # Update other state variables as necessary
            rounds += 1
            current_player_index = (current_player_index + 1)

            # Update the new_state dictionary
            new_state._sensors['game-board-sensor']['value'] = board
            new_state.deck = deck
            new_state.rounds = rounds
            new_state.scores = scores  # Update if necessary
            new_state.current_player_index = current_player_index
            new_state.players = players

            return new_state

    
    
    @staticmethod
    def turn(game_state):
        return game_state['players'][game_state['current_player_index']].name
    
    @staticmethod
    def payoff(game_state, player_name):
        player = next(player for player in game_state['players'] if player.name == player_name)
        if player.role == 'Gold-Digger' and game_state['game_board'].gold_found():
            return 1  # Gold-Diggers win when gold is found
        elif player.role == 'Saboteur' and not game_state['game_board'].gold_found():
            return 1  # Saboteurs win when gold is not found
        else:
            return 0  # Otherwise, this player did not achieve their objective
                    
    def get_percepts(self):
        self.get_game_state()
        return {
            'game-board-sensor' : self._sensors['game-board-sensor']['value'], 
            'role-sensor': self._sensors['role-sensor']['value'],
            'turn-taking-indicator': self._sensors['turn-taking-indicator']['value'],
            'hand-sensor': self._sensors['hand-sensor']['value']
        }

    def state_transition(self):
        # Your implementation here
       pass
    
    def get_board(self):
            return self.grid
        
