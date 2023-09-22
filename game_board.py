from une_ai.models import GridMap
from card import PathCard, GoalCard, StartingCard, ActionCard
import random

class GameBoard():

    def __init__(self, start_x=6, start_y=10):
        self._board = GridMap(20, 20, None)
        
        start_card = PathCard.cross_road(special_card='start')
        goal_cards = []
        gold_idx = random.choice([0,1,2])
        for i in range(3):
            if gold_idx == i:
              label = 'gold'
            else:
                label = 'goal'
            goal_cards.append(PathCard.cross_road(special_card=label))
       
        self._board.set_item_value(start_x, start_y, start_card)
        goal_locations = [(14,8),(14,10), (14,12)]
        
        for i, goal in enumerate(goal_cards):
            self._board.set_item_value(goal_locations[i][0], goal_locations[i][1], goal)
    
   
    def get_board(self):
        return self._board.get_map()

    # TODO
    # This method does not check if there is a valid path from
    # the starting card to the new placed card
    def add_path_card(self, x, y, path_card):
        # need to return an invalid path card if the card is not valid
        assert isinstance(path_card, PathCard), "The parameter path_card must be an instance of the class PathCard"
        assert x >= 0 and x < 20, "The x coordinate must be 0 <= x < 20"
        assert y >= 0 and y < 20, "The y coordinate must be 0 <= y < 20"
        assert self._board.get_item_value(x, y) is None, "There is already another card on the board at coordinates ({0}, {1})".format(x, y)

        self._board.set_item_value(x, y, path_card)
      
    def remove_path_card(self, x, y):
        assert x >= 0 and x < 20, "The x coordinate must be 0 <= x < 20"
        assert y >= 0 and y < 20, "The y coordinate must be 0 <= y < 20"
        assert self._board.get_item_value(x, y) is not None and not self._board.get_item_value(x, y).is_special_card(), "There is no valid card to remove at coordinates ({0}, {1})".format(x, y)

        self._board.set_item_value(x, y, None)



    def get_grid_map(self):
        return self._board
    
    def get_item_value(x, y):
        if x < 0 or y < 0 or x >= 20 or y >= 20:
            return None
        return GameBoard.get_item_value(x, y)
    

    def is_valid_path(self, x, y, visited):
        if x < 0 or x >= 20 or y < 0 or y >= 20:
            return False
        if visited[x][y]:
            return False
        card = self._board.get_item_value(x, y)
        if card is None:
            return False
        return True
    
    
    
    
    
    
    
    
 
    def can_connect(self, pathcard, neighbor_card, relative_position):
        """
    Check if two cards can connect based on their tunnel openings.

    Args:
        pathcard: The first PathCard object.
        neighbor_card: The second PathCard object.
        relative_position: A string indicating the relative position of neighbor_card to pathcard (e.g., "north", "south", "east", "west").
        
    Returns:
        bool: True if the cards can connect, False otherwise.
    """

        if relative_position == 'north':
            return pathcard.is_open('north') and neighbor_card.is_open('south')
        elif relative_position == 'south':
            return pathcard.is_open('south') and neighbor_card.is_open('north')
        elif relative_position == 'east':
            return pathcard.is_open('east') and neighbor_card.is_open('west')
        elif relative_position == 'west':
            return pathcard.is_open('west') and neighbor_card.is_open('east')
        else:
            return False  # Invalid relative_position

    def apply_action_to_game_board(self, player, action):
            action_type = action['type']
            current_player = self.sabenv.current_player  # Assuming this is how you get the current player
            game_state = self.sabenv.get_game_state()  # And this is how you get the current game state

            if action_type == 'place-path-card':
                card = action['card']
                position = action.get('position', None)  # Get position from action, if it exists

                if isinstance(card, PathCard):  # Assuming PathCard is the name of your path card class
                    position = self.choose_position(card)
                    if position is not None:
                        x, y = position
                        # Add the path card to the game board
                        success = self.sabenv.game_board.add_path_card(x, y, card, current_player, game_state)
                        
                        if not success:
                        # Handle invalid placement
                            print("Invalid placement. Trying again.")
                        new_action = self.handle_invalid_placement(current_player, game_state)
                        if new_action is not None:
                            self.apply_action_to_game_board(new_action)
                        return
                        
                        # Remove the card from the player's hand
                        self.sabenv.discard_card(current_player, card)
                        
                    else:
                        print("No valid position found for card.")
                else:
                    print("Error: Expected a PathCard for placing on the board.")

            elif action_type == 'use-action-card':
                card = action['card']
                if isinstance(card, ActionCard):  # Make sure it's an ActionCard
                    target = action.get('target', None)
                    self.sabenv.use_action_card(current_player, self.sabenv.game_board, card, target)
                    self.sabenv.discard_card(current_player, card)
                else:
                    print("Error: Expected an ActionCard for action.")
                    

            elif action_type == 'pass-turn':
                self.sabenv.pass_turn(current_player)

            else:
                print("Invalid action type.")

            self.sabenv.draw_card(current_player)
            self.sabenv.next_player()
 
    
    
    
    
    
    def add_path_card(self, x, y, path_card, skip_validation=False, current_player=None, game_state=None):
        if not self.validate_card_placement(x, y, path_card):
          return self.handle_invalid_placement(current_player, game_state)
        
        self._board.set_item_value(x, y, path_card)
        
        if not self.validate_card_connection(x, y, path_card, current_player, game_state):
            return self.handle_invalid_placement(current_player, game_state)
        
        if not skip_validation and not self.dfs(self.start_x, self.start_y, x, y, [[False]*20 for _ in range(20)]):
            self._board.set_item_value(x, y, None)
            return self.handle_invalid_placement(current_player, game_state)
        
        return True

    def validate_card_placement(self, x, y, path_card):
        assert isinstance(path_card, PathCard), "The parameter path_card must be an instance of the class PathCard"
        if self._board.get_item_value(x, y) is not None:
            print(f"There is already another card on the board at coordinates ({x}, {y}).")
            return False
        return True

    def validate_card_connection(self, x, y, path_card, current_player, game_state):
        for dx, dy, current_exit, next_exit in [(-1, 0, 'north', 'south'), (1, 0, 'south', 'north'), (0, -1, 'west', 'east'), (0, 1, 'east', 'west')]:
            neighbor_x, neighbor_y = x + dx, y + dy
            neighbor_card = self._board.get_item_value(neighbor_x, neighbor_y)
            if neighbor_card is not None and not self.can_connect(path_card, neighbor_card, current_exit):
                print("Invalid placement. The new card does not connect with an adjacent card.")
                return False
        return True
    
    
    
    
    def handle_invalid_placement(self, current_player, game_state):
        while True:
            choice = int(input("Invalid placement. Options:\n1. Retry with a different card or position\n2. Use an action card\n3. Pass the turn\nEnter your choice: "))
            
            if choice == 1:
                # Retry with a different card or position
                chosen_action = self.action_chooser(current_player, game_state)
                print(chosen_action)

                if chosen_action['type'] == 'place-path-card':
                    #print the chosen action
                    print(chosen_action)
                
                    x, y = chosen_action['position']  
                    path_card = chosen_action['card']
                    result = self.add_path_card(x, y, path_card, current_player=current_player, game_state=game_state)
            
                    if result:
                        print("Successfully placed the card.")
                        return {'type': 'success'}
                    else:
                        print("Failed to place the card.")
                        continue  # Let the player choose again
                else:
                    print("You selected an action other than placing a path card. Please select option 1 if you want to place a path card.")

            elif choice == 2:
                # Use an action card
                chosen_action = self.action_chooser(current_player, game_state)
                print(chosen_action)

                if chosen_action['type'] == 'use-action-card':
                    return chosen_action  # If the user chooses to use an action card, return the new action details.
                else:
                    print("You selected an action other than using an action card. Please select option 2 if you want to use an action card.")
            
            elif choice == 3:
                # Pass the turn
                return {'type': 'pass-turn'}
            
            else:
                print("Invalid choice. Please select again.")
   
    # def action_chooser(self, agent, current_player, game_state):
    #     legal_actions = self.sabenv.get_legal_actions(current_player, game_state)

    #     print("Legal actions available:")
    #     for idx, action in enumerate(legal_actions):
    #         print(f"{idx + 1}. {action}")
        
        
    #     choice = agent.choose_action(game_state, current_player, legal_actions)
    #     chosen_type = legal_actions[choice]

    #     action_details = {}

    #     if chosen_type == 'place-path-card':
    #         # Get the chosen card from the player
    #         chosen_card = self.choose_card(current_player)
    #         if chosen_card is None:
    #             print("No card was chosen. Returning None.")
    #             return None
    #         # Get the position where the player wants to place the card
    #         chosen_position = self.choose_position(chosen_card)
    #         if chosen_position is None:
    #             print("No valid position found for card. Returning None.")
    #             return None
    #         action_details = {'type': chosen_type, 'card': chosen_card, 'position': chosen_position}

    #     elif chosen_type == 'use-action-card':
    #         # Get the chosen card from the player
    #         chosen_card = self.choose_card(current_player)
    #         if chosen_card is None:
    #             print("No card was chosen. Returning None.")
    #             return None
    #         # Get the target player if any
    #         chosen_target = self.choose_target_player()
    #         action_details = {'type': chosen_type, 'card': chosen_card, 'target': chosen_target}

    #     else:
    #         # For 'pass-turn' or any other action type that doesn't require further details
    #         action_details = {'type': chosen_type}

    #     return action_details



    def dfs(self, start_x, start_y, target_x, target_y, visited):
        stack = [(start_x, start_y)]

        while stack:
            x, y = stack.pop()
            visited[x][y] = True  # Mark the current node as visited

            if (x, y) == (target_x, target_y):
                return True  # Found a valid path

            current_card = self._board.get_item_value(x, y)
            open_directions = self.get_open_directions(current_card)

            for dx, dy, current_exit, next_exit in open_directions:
                new_x, new_y = x + dx, y + dy

                if new_x < 0 or new_x >= 20 or new_y < 0 or new_y >= 20:
                    continue

                if visited[new_x][new_y]:
                    continue

                next_card = self._board.get_item_value(new_x, new_y)

                if next_card is None:
                    continue

                if isinstance(next_card, GoalCard):
                    if next_card.is_revealed() and self.tunnels_align(current_card, next_card, current_exit, next_exit):
                        stack.append((new_x, new_y))
                elif self.tunnels_align(current_card, next_card, current_exit, next_exit):
                    stack.append((new_x, new_y))

        return False  # No valid path found


    def dfs_gold_found():
        stack = [(6,10)]
        visited = set()
        
        while stack:
            x, y = stack.pop()
            visited.add((x, y))
            
            current_card = GameBoard.get_item_value(x, y)
            
            # Assuming you have a method is_gold_card() that returns True if the card is a gold card
            if current_card and PathCard.is_gold(current_card):
                return True  # The gold card is found
            
            # Fetch the valid neighbor cells (cards that the tunnel from the current card leads to)
            neighbors = GameBoard.get_valid_neighbors(x, y, current_card)
            
            for neighbor_x, neighbor_y in neighbors:
                if (neighbor_x, neighbor_y) not in visited:
                    stack.append((neighbor_x, neighbor_y))
                    
        return False  # The gold card was not found


    @staticmethod
    def get_exit_direction(card, direction):
        """Returns the exit direction from a tunnel in a card."""
        for tunnel in card.get_tunnels():
            if direction in tunnel:
                return tunnel[0] if tunnel[1] == direction else tunnel[1]
        return None
    
    @staticmethod
    def are_opposite_directions(direction1, direction2):
        """Checks if two directions are opposite."""
        opposite = {
            'north': 'south',
            'south': 'north',
            'east': 'west',
            'west': 'east'
        }
        return opposite[direction1] == direction2

    def get_open_directions(self, current_card):
        """Returns a list of open directions for a given card."""
        open_directions = []
        for tunnel in current_card.get_tunnels():
            for direction in tunnel:
                if direction == 'north':
                    open_directions.append((-1, 0, 'north', 'south'))
                elif direction == 'south':
                    open_directions.append((1, 0, 'south', 'north'))
                elif direction == 'east':
                    open_directions.append((0, 1, 'east', 'west'))
                elif direction == 'west':
                    open_directions.append((0, -1, 'west', 'east'))
        return open_directions
    
    def get_valid_neighbors(self, x, y, current_card):
        valid_neighbors = []
        open_directions = self.get_open_directions(current_card)
        
        for dx, dy, current_exit, next_exit in open_directions:  # Assuming open_directions provides these
            new_x, new_y = x + dx, y + dy
            next_card = self._board.get_item_value(new_x, new_y)
            
            # Additional check to ensure the next card is not None and tunnels align
            if next_card and self.tunnels_align(current_card, next_card, current_exit, next_exit):
                valid_neighbors.append((new_x, new_y))
                
        return valid_neighbors


    def tunnels_align(self, current_card, next_card, current_exit, next_exit):
        """Checks if the tunnels between two cards align."""
        print(f"Checking tunnel alignment between \n {current_card} and \n {next_card}")

        # if not next_card.reveal_card():
        #     print(f"Next card is not revealed. Alignment failed.")
        #     return False

        self_exit = self.get_exit_direction(current_card, current_exit)
        other_exit = self.get_exit_direction(next_card, next_exit)
        
        print(f"Self exit: {self_exit}, Other exit: {other_exit}")

        if self_exit and other_exit and self.are_opposite_directions(self_exit, other_exit):
            print("Tunnels align.")
            return True
        else:
            print("Tunnels do not align.")
            return False
        
        
    def print_board_with_tunnels(self):
            board_map = self._board.get_map()

            for row in board_map:
                row_str = []
                for cell in row:
                    if cell is None:
                        row_str.append("None")
                    elif isinstance(cell, PathCard):
                        tunnels = cell.get_tunnels()
                        tunnels_str = "".join([f"{key[0]}{val[0]}" for key, val in tunnels])
                        row_str.append(f"Path({tunnels_str})")
                    elif isinstance(cell, GoalCard):
                        row_str.append(f"Goal({cell.get_type()})")
                    elif isinstance(cell, self.StartCard):
                        row_str.append("Start")
                print("\t".join(row_str))


    def __str__(self):
        no_card = '   \n   \n   '
        board_map = self._board.get_map()
        board_str = ''
        for row in board_map:
            for i in range(3):
                for card in row:
                    if card is None:
                        board_str += no_card.split('\n')[i]
                    else:
                        board_str += str(card).split('\n')[i]
                    board_str += ' '  # Add a space between cards in the same row
                board_str += '\n'  # Add a newline at the end of each row
            
        return board_str

