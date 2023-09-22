from une_ai.models.MCTS_graph_node import MCTSGraphNode
import MCTS_functions
import time
from saboteur_base_environment import SaboteurBaseEnvironment
from game_board import GameBoard

def mcts_agent_program(percepts, actuators, time_limit=5):
    
    start_time = time.time()  # Record the start time
    # Extract game state from percepts
    env = SaboteurBaseEnvironment()
    board = env.get_percepts()['game-board-sensor']
    role = env.get_percepts()['role-sensor']
    turn = env.get_percepts()['turn-taking-indicator']
 
    
    game_data = {
        'game-board': board,
        'role': role,
        'player-turn': turn
    }
    
    optimal_move = None 
    
    try:
        if not SaboteurBaseEnvironment.is_terminal(game_data['game-board']):
            root = MCTSGraphNode(game_data, None, None)
            try:
                # Original line
                optimal_move = MCTS_functions.new_mcts(root, turn, time_limit)
            except TypeError as e:
                print(f"TypeError occurred: {e}")
                optimal_move = None 
            # optimal_move = MCTS_functions.new_mcts(root, turn, time_limit)
            
            # result = MCTS_random_playout(initial_node=some_node, max_iterations=2000)
            # result = MCTS_random_playout(env=some_environment, max_iterations=2000)
            
            elapsed_time = time.time() - start_time  # Calculate elapsed time
            print(f"Debug: MCTS completed in {elapsed_time:.2f} seconds.")
            
        if optimal_move:
            return [optimal_move]
        else:
            print("Debug: No optimal move found.")
            # Here you can return a fail-safe action, if you have one
            
    except Exception as e:
        print(f"Error: An exception occurred - {e}")
        raise e

    return []  # Return an empty list if no action is chosen

