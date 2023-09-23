import math
import random
import time
from saboteur_base_environment import SaboteurBaseEnvironment



def uct_selection_policy(node, target_player, C=1.414):
    """
    This function implements the UCT (Upper Confidence Bound for Trees) selection policy for the Monte Carlo Tree Search algorithm.
    
    This selection_policy function has been implemented using the selection policy function discussed during the lectures and 
    in the tic-tac-toe workshops for week 4 for the unit COSC550.      
    
    Args:
    - node: the current node in the search tree
    - target_player: the player whose turn it is to move
    - C: the exploration constant, often set to sqrt(2)
    
    Returns:
    - the next node to explore, according to the UCT selection policy
    """
    successors = node.get_successors()
    unexplored_nodes = [s for s in successors if s.n() == 0]
    
    # If there are unexplored nodes, select one of them randomly
    if unexplored_nodes:
        return random.choice(unexplored_nodes)
    
    best_uct = -1
    best_node = None
    parent_plays = node.n()  # Number of plays in the parent node

    for s in successors:
        # Calculate UCT value for this node
        wins = s.wins(target_player)
        plays = s.n()
        uct_value = (wins / plays) + C * math.sqrt(math.log(parent_plays) / plays)

        # Update best node if this node's UCT value is greater
        if uct_value > best_uct:
            best_uct = uct_value
            best_node = s
            
    return best_node


def MCTS_random_playout(initial_node, max_iterations=2000):
    """
    Conducts a random playout from the given initial node until a terminal state is reached or the maximum number of iterations is exceeded.
    Returns the winner of the playout.

    This random_playout function has been implemented with the random_playout function as reference during the lectures and 
    in the tic-tac-toe workshops for week 4 for the unit COSC550.      

    Args:
    - initial_node: the node from which to start the playout (optional)
    - max_iterations: the maximum number of iterations to perform before stopping the playout
    - env: the environment object (optional)

    Returns:
    - the winner of the playout (either 1, -1, or 0)
    """
    
    # if env is None:
    #     env = SaboteurBaseEnvironment()
    
    # if initial_node is not None:
    # else:
    #     current_playout_state = env.get_game_state()
    
    
    current_playout_state = initial_node.get_state()

    iterations = 0
    
    while not SaboteurBaseEnvironment.is_terminal(current_playout_state):
        if iterations >= max_iterations:
            break
        
        possible_moves = SaboteurBaseEnvironment.get_legal_actions(current_playout_state)
  
        
        # Check if all available_actions are in possible_moves
        if 10 in possible_moves and random.random() < 0.2:
            action = 10
        else:
            action = random.choice(possible_moves)
        
        current_playout_state = SaboteurBaseEnvironment.transition_result(current_playout_state, action)
        iterations += 1
    
    return SaboteurBaseEnvironment.get_winner()



def new_mcts(root_node, target_player, max_time=20, env=None):
    """
    Runs the Monte Carlo Tree Search algorithm to select the best move for the given player.
    
    This random_playout function has been implemented with the random_playout function as reference discussed during the lectures and 
    in the tic-tac-toe workshops for week 4 for the unit COSC550.      

    Args:
        root_node (Node): The root node of the search tree.
        target_player (int): The player for whom the best move is to be selected.
        max_time (float): The maximum time (in seconds) to run the search.
        env (SaboteurBaseEnvironment): The environment object (optional).

    Returns:
        int: The best move selected by the algorithm.
    """
    start_time = time.time()
    

    while (time.time() - start_time) < max_time:
        current_node = root_node
        while not SaboteurBaseEnvironment.is_terminal(current_node.get_state()) and not current_node.is_leaf_node():
            current_node = uct_selection_policy(current_node, target_player)
        
        selected_node = current_node
        available_moves = SaboteurBaseEnvironment.get_legal_actions(selected_node.get_state())
        
        for a in available_moves:
            if not selected_node.was_action_expanded(a):
                successor_state = SaboteurBaseEnvironment.transition_result(current_node.get_state())
                selected_node.add_successor(successor_state, a)
        
        winner = MCTS_random_playout(selected_node)
        if winner is None:
            winner = target_player

        selected_node.backpropagate(winner)
        
    best_node = max(root_node.get_successors(), key=lambda x: x.wins(target_player) / x.n(), default=None)
    
    return best_node.get_action() if best_node else None


