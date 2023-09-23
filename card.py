class Card():
    pass

class ActionCard(Card):

    def __init__(self, action):
        assert action in ['map', 'sabotage', 'mend', 'dynamite'], "The parameter action must be either map, sabotage, mend or dynamite"

        self._action = action
    
    def get_action(self):
        self._action
        return True
   
    def __str__(self):
        return f"ActionCard({self._action})"

class InvalidTunnel(Exception):
    pass



class PathCard(Card):
    
    def __init__(self, tunnels, special_card=None, exits = [0,0,0,0] ):
        assert isinstance(tunnels, list), "The parameter tunnels must be a list of tuples"
        assert special_card in ['start', 'goal', 'gold', None], "The parameter special_card must be either None, start, goal or gold"

        self._special_card = special_card
        self._revealed = True
        self._exits = exits

        if special_card:
            # special cards are all cross roads
            cross_road = PathCard.cross_road()
            self._tunnels = cross_road.get_tunnels()
            if special_card in ['goal', 'gold']:
                self._revealed = False
        else:
            self._tunnels = tunnels
        
        
        for tunnel in tunnels:
            if not self._is_valid_tunnel(tunnel):
                raise InvalidTunnel("The tunnel '{0}' is an invalid one for this card.".format(tunnel))
        
            
    def cross_road(special_card=None):
        return PathCard(
            [
                ('north', 'south'),
                ('north', 'east'),
                ('north', 'west'),
                ('south', 'east'),
                ('south', 'west'),
                ('east', 'west')
            ], special_card=special_card,
            exits = [1,1,1,1] #N E S W
        )
    
    def vertical_tunnel():
        return PathCard(
            [
                ('north', 'south')
            ],
            exits = [1,0,1,0]
        )
    
    def horizontal_tunnel():
        return PathCard(
            [
                ('east', 'west')
            ], 
            exits = [0,1,0,1]
        )
    
    def vertical_junction():
        return PathCard(
            [
                ('north', 'south'),
                ('north', 'east'),
                ('south', 'east')
            ],
            exits = [1,1,1,0]
        )
    
    def horizontal_junction():
        return PathCard(
            [
                ('east', 'north'),
                ('west', 'north'),
                ('east', 'west')
            ],
            exits = [1,1,0,1]
        )
    
    def turn():
        return PathCard(
            [
                ('south', 'east')
            ],
            exits = [0,1,1,0]
        )
    
    def reversed_turn():
        return PathCard(
            [
                ('south', 'west')
            ],
            exits = [0,0,1,1]
        )
    
    def dead_end(directions):
        tunnels = []
        for direction in directions:
            tunnels.append((direction, None))
        return PathCard(tunnels)
    
    
    def _is_valid_tunnel(self, tunnel):
        if not isinstance(tunnel, tuple):
            return False
        if len(tunnel) != 2:
            return False
        for direction in tunnel:
            if direction not in ['north', 'east', 'south', 'west', None]:
                return False
        if tunnel[0] is None:
            return False
        if tunnel[0] is None and tunnel[1] is None:
            return False
        if tunnel[0] == tunnel[1]:
            return False
                
        return True
    
    def is_special_card(self):
        return self._special_card is not None
    
    def is_gold(self):
        return self._special_card == 'gold'
    
    def reveal_card(self):
        self._revealed = True
        
    def is_open(self, direction):
        for tunnel in self._tunnels:
            if direction in tunnel and None not in tunnel:
                return True
        return False

    def turn_card(self):
        tunnels = []
        opposite = {
            'north': 'south',
            'east': 'west',
            'west': 'east',
            'south': 'north',
        }
        for tunnel in self._tunnels:
            new_tunnel = (
                opposite[tunnel[0]] if tunnel[0] is not None else None,
                opposite[tunnel[1]] if tunnel[1] is not None else None
            )
            tunnels.append(new_tunnel)
        
        self._exits = self._exits[2:] + self._exits[:2] #rotate by 2
        self._tunnels = tunnels
        
    def get_tunnels(self):
        return self._tunnels.copy()
    
    # def __str__(self):
    #     card_rep = ['   ', '   ', '   ']
    #     if self._revealed:
    #         for tunnel in self._tunnels:
    #             directions = [(tunnel[0], tunnel[1]), (tunnel[1], tunnel[0])]
    #             for direction in directions:
    #                 tunnel_from = direction[0]
    #                 tunnel_to = direction[1]
    #                 if tunnel_from == 'north':
    #                     card_rep[0] = card_rep[0][:1] + '|' + card_rep[0][2:]
    #                     if tunnel_to is not None:
    #                         card_rep[1] = card_rep[1][:1] + '┼' + card_rep[1][2:]
    #                 elif tunnel_from == 'south':
    #                     card_rep[2] = card_rep[2][:1] + '|' + card_rep[2][2:]
    #                     if tunnel_to is not None:
    #                         card_rep[1] = card_rep[1][:1] + '┼' + card_rep[1][2:]
    #                 elif tunnel_from == 'east':
    #                     card_rep[1] = card_rep[1][:2] + '—'
    #                     if tunnel_to is not None:
    #                         card_rep[1] = card_rep[1][:1] + '┼' + card_rep[1][2:]
    #                 elif tunnel_from == 'west':
    #                     card_rep[1] = '—' + card_rep[1][1:]
    #                     if tunnel_to is not None:
    #                         card_rep[1] = card_rep[1][:1] + '┼' + card_rep[1][2:]
    #     else:
    #         return '   \n ? \n   '
    #     return '\n'.join(card_rep)

    def __str__(self):
        if self._revealed:
            directionHashset = set()
            for tunnels in self._tunnels:
                directionHashset.add(tunnels[0])
                directionHashset.add(tunnels[1])
            
            top = '░' + ('█' if 'north' in directionHashset else '░') + '░'
            middle = ('█' if 'west' in directionHashset else '░') + ('░' if None in directionHashset else '█') + ('█' if 'east' in directionHashset else '░')
            bottom = '░' + ('█' if 'south' in directionHashset else '░') + '░'
        return [top,middle,bottom]

class StartingCard(PathCard):
    def __init__(self):
        # Initialize with all exits open
        super().__init__(tunnels=[('north', 'south'), ('east', 'west')], special_card='start')

class GoalCard(PathCard):
    def __init__(self, has_gold):
        super().__init__(tunnels=[('north', 'south'), ('east', 'west')], special_card='goal' if not has_gold else 'gold')
        self.has_gold = has_gold  # Whether this card has gold