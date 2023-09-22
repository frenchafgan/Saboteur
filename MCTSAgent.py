from une_ai.models import MCTSGraphNode, Agent
from card import PathCard, ActionCard
import random
import math

class MCTSAgent(Agent):
    def __init__(self, role, agent_program, num_simulations=1000, ucb1_const=2):
        super().__init__(role, agent_program)
        self.root = None
        self.num_simulations = num_simulations
        self.ucb1_const = ucb1_const
        self.add_all_sensors()
        self.add_all_actuators()
        self.add_all_actions()
        self._percepts = None
        self.role = role
        self._players = []
        for i in range(0, len(self._players)):
                self.current_player = self._players[i]        
        self.hand = []
        self._sensors = {
            'role-sensor': {'value': role},
            'hand-sensor': {'value': []},  # Initialize hand-sensor here
            'sabotaged': {'value': False},
            'game-board-sensor': {'value': None},
            'turn-taking-indicator': {'value': None}
        }
        
                
    
    # # function to get the hand of each player from intialization
    # def get_player_hand(self, player):
        
    #     return player.hand 
        

    def ucb1(self, parent_node):
        parent_visits = parent_node.n()
        return max(
            parent_node.get_successors(),
            key=lambda child_node: (child_node.wins(self.role) / child_node.n()) +
                                    math.sqrt(self.ucb1_const * math.log(parent_visits) / child_node.n()),
        )
  
    
    def get_action_list(self, current_player, saboteur_env):
        self.root = MCTSGraphNode(saboteur_env, None, None)

        for _ in range(self.num_simulations):
            current_node = self.root
            current_env = saboteur_env.copy()

            while not current_node.is_leaf_node():
                current_node = self.ucb1(current_node)
                current_env.apply_action(current_player, current_node.get_action())

            available_actions = current_env.get_available_actions(current_player)
            if not available_actions:
                print("Debug: No available actions.")
                return None  # No available actions, return None

            for action in available_actions:
                new_env = current_env.copy()
                game_state = current_env.get_game_state()
                player = current_player._sensors
                new_env.apply_action(game_state, player, action)
                current_node.add_successor(new_env, action)

           
            child_node = random.choice(current_node.get_successors())
            while not current_env.is_terminal():
                available_actions = current_env.get_available_actions(current_player)
                if not available_actions:
                    print("Debug: No available actions during rollout.")
                    break  # Break out of the loop if no available actions

                action = random.choice(available_actions)
                current_env.apply_action(current_player, action)

            # Backpropagation
            winner = current_env.get_winner()
            child_node.backpropagate(winner)

        best_child = self.ucb1(self.root)
        if best_child:
            return best_child.get_action()
        else:
            print("Debug: No best child found.")
            return None
        

    
    def get_name(self):
        return "MCTS Agent"
    
    def add_all_actions(self):
        return super().add_all_actions()
    
    def add_all_sensors(self):
        return super().add_all_sensors()
    
    def add_all_actuators(self):
        return super().add_all_actuators()
    
