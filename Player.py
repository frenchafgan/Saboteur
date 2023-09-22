# Player class definition
from une_ai.models import Agent

class Player(Agent):
    def __init__(self, player_id, role):
        super().__init__(f"Player {player_id}", None)  # Call parent constructor
        self.player_id = player_id
        self.role = role
       
        self.hand = []
        
        # Add all necessary sensors, actuators, and actions
        self.add_all_sensors()
        self.add_all_actuators()
        self.add_all_actions()
        
