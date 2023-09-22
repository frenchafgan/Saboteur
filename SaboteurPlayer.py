from une_ai.models import Agent, GridMap
from card import Card


class SaboteurPlayer(Agent):
    
    def __init__(self, agent_name, agent_program=None, role=None):
        super().__init__(agent_name, agent_program)
        self.role = role 
        self.hand = [] 
        self.roles = ['Gold-Digger', 'Saboteur']
        self.add_all_sensors()
        self.add_all_actuators()
        self.add_all_actions()
        
        


    def add_all_sensors(self):
        # game-board-sensor
        default_game_board = GridMap(20, 20, None)

        self._sensors['game-board-sensor'] = {
            'sensor-name': 'game-board-sensor',
            'value': default_game_board,
            'validation-function': lambda board: isinstance(board, GridMap) and board.width == 20 and board.height == 20
        }
                
        self._sensors['role-sensor'] = {
            'sensor-name': 'role-sensor',
            'value': 'None',
            'validation-function': lambda role: role in ['Gold-Digger', 'Saboteur']
        }

        def validate_turn_indicator(x):
            return isinstance(x, int) and x >= 0 and x < len(self.players)

        # turn-taking-indicator
        self._sensors['turn-taking-indicator'] = {
            'sensor-name': 'turn-taking-indicator',
            'value': None,  # ID of the player whose turn it is
            'validation-function': validate_turn_indicator
        }

        # hand-sensor
        self._sensors['hand-sensor'] = {
            'sensor-name': 'hand-sensor',
            'value': [],  # The cards in the player's hand
            'validation-function': lambda hand: isinstance(hand, list) and all(isinstance(card, Card) for card in hand)
        }

    def add_all_actuators(self):
        # 'path-card-handler' actuator
        self._actuators['path-card-handler'] = {
            'actuator-name': 'path-card-handler',
            'value': None,
            'validation-function': lambda x: True  # You can define more specific validation here
        }

        # 'action-card-handler' actuator
        self._actuators['action-card-handler'] = {
            'actuator-name': 'action-card-handler',
            'value': None,
            'validation-function': lambda x: True  # You can define more specific validation here
        }

        # 'pass-handler' actuator
        self._actuators['pass-handler'] = {
            'actuator-name': 'pass-handler',
            'value': False,
            'validation-function': lambda x: isinstance(x, bool)
        }

    def add_all_actions(self):
        # Add actions for placing path cards
        self._actions['place-path-card'] = {
            'path-card-handler': 'place',
            'action-card-handler': None,
            'pass-handler': False
        }

        # Add actions for using action cards
        self._actions['use-action-card'] = {
            'path-card-handler': None,
            'action-card-handler': 'use',
            'pass-handler': False
        }

        # Add action for passing the turn
        self._actions['pass-turn'] = {
            'path-card-handler': None,
            'action-card-handler': None,
            'pass-handler': True
        }
    
  
    def __str__(self):
        
        return f"{self._agent_name} ({self.role})"
