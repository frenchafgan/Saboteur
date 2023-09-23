# """
# This module contains the implementation of a game called "Saboteur". 
# The game is initialized by creating a game board, a deck of cards, and a list of players.
# Each player has a name, a role, and a hand of cards.
# The game loop consists of each player taking a turn, where they choose to place a path card, use an action card, or pass their turn.
# The game ends when a game-ending condition is met, such as the deck being empty. 
# """

from saboteur_base_environment import SaboteurBaseEnvironment
from agent_programs import mcts_agent_program
from game_board import GameBoard
import random

def main():
    # Initialization
    env = SaboteurBaseEnvironment()

    # Create an instance of MCTSAgent
    # current_player = env.current_player

    # Main Game Loop
    while not env.is_terminal():
      
        # Get current player and available actions
        # percepts = env.get_percepts()
        current_player = env.current_player
        for current_player in env.players:
            
            print(f"Current player: {current_player}")

            # Choose and validate action
            available_actions = env.get_legal_actions(current_player)
            # print(f"Chosen action by MCTS: {chosen_action}")  # Logging
            print (f"Available actions: {available_actions}")
            
            #add the first available action to the gameboard
            # chosen_action = available_actions[0]
            if available_actions:
                chosen_card = random.choice(list(available_actions.keys()))
                chosen_action = available_actions[chosen_card]
                GameBoard.add_path_card(x=chosen_action[0], y=chosen_action[1], path_card=chosen_card)


            else:
                if not available_actions and not env.deck.is_empty():
                    
                    env.draw_card(current_player)
                
            env.get_next_player()
            
            
            # chosen_action = mcts_agent_program()
            
                  
        
            # print(f"Random action chosen: {chosen_action}")
            # print(f"Game board after random action: {env.game_board}")  
            
            # if not env.validate_action(available_actions, current_player):
            #     print("Invalid action.")
            #     continue  # Skip to the next iteration of the loop

            # # # Apply chosen action
            # # env.apply_action(chosen_action, current_player)
            # # game_logic.apply_action_to_game_board(chosen_action)
            
            # # Update game state and player's hand
            # game_state = env.get_game_state()
            
            # # Draw a card if no available actions and deck is not empty
         
            
            # Move to the next player
          
    # End of Game
    if env.get_winner(): 
        winners = env.get_winner()
    print(f"Game Over. Winners: {winners}")

if __name__ == "__main__":
    main()




