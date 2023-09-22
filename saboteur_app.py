# """
# This module contains the implementation of a game called "Saboteur". 
# The game is initialized by creating a game board, a deck of cards, and a list of players.
# Each player has a name, a role, and a hand of cards.
# The game loop consists of each player taking a turn, where they choose to place a path card, use an action card, or pass their turn.
# The game ends when a game-ending condition is met, such as the deck being empty. 
# """

from saboteur_base_environment import SaboteurBaseEnvironment
from agent_programs import mcts_agent_program
from game_logic import GameLogic
from MCTSAgent import MCTSAgent


def main():
    # Initialization
    env = SaboteurBaseEnvironment()

    game_logic = GameLogic(env)
    game_logic.initialize_game()
    
    # Initialize Players using the game_logic method
    players = game_logic.initialize_players()
    
    # Draw initial cards for players
    env.draw_initial_cards(players)
    
    # Create an instance of MCTSAgent
    current_player = env.current_player
    percepts = env.get_percepts()

    mcts_agent = mcts_agent_program(current_player._actuators, current_player._sensors)
    
    # Main Game Loop
    while not env.is_terminal():
        
        # Update role for MCTSAgent
        # role = env.current_player.role  # Update if role can change
        
        # Get current player and available actions
        # current_player = env.current_player
        
        # Choose and validate action
        chosen_action = game_logic.choose_card(current_player)
        print(f"Chosen action by MCTS: {chosen_action}")  # Logging
        
        if not env.validate_action(chosen_action, current_player):
            print("Invalid action.")
            continue  # Skip to the next iteration of the loop

        # Apply chosen action
        env.apply_action(chosen_action, current_player)
        game_logic.apply_action_to_game_board(chosen_action)
        
        # Update game state and player's hand
        game_state = env.get_game_state()
        
        # Draw a card if no available actions and deck is not empty
        if not chosen_action and not env.deck.is_empty():
            env.draw_card(current_player)
        
        # Move to the next player
        env.update_to_next_player()
        
    # End of Game
    winners = env.get_winner()
    print(f"Game Over. Winners: {winners}")

if __name__ == "__main__":
    main()



