from player import Player, Position
import random

class Team:
    def __init__(self, name, tier, is_youth_team=False, game=None):
        self.name = name
        self.tier = tier
        self.players = []
        self.is_youth_team = is_youth_team
        self.game = game  # Reference to the game instance
        self.formation = "4-3-3"  # Default formation
        
        # Team quality modifiers based on league tier
        self.rating_modifiers = {
            1: {"ceiling": 91, "average": 86, "floor": 60},
            2: {"ceiling": 94, "average": 83, "floor": 62},
            3: {"ceiling": 90, "average": 81, "floor": 65},
            4: {"ceiling": 88, "average": 84, "floor": 69},
            5: {"ceiling": 92, "average": 78, "floor": 67},
            6: {"ceiling": 87, "average": 74, "floor": 57},
            7: {"ceiling": 80, "average": 71, "floor": 53}
        }
        
        # Initialize squad
        if not is_youth_team:
            self.generate_squad()
        else:
            self.generate_youth_squad()

    def generate_squad(self):
        """Generates a full squad of players"""
        # Generate goalkeepers
        for _ in range(3):
            self.players.append(Player(Position.GK, league_tier=self.tier))
        
        # Generate defenders
        for _ in range(4):
            self.players.append(Player(Position.CB, league_tier=self.tier))
        for _ in range(4):
            self.players.append(Player(Position.WB, league_tier=self.tier))
            
        # Generate midfielders
        for _ in range(3):
            self.players.append(Player(Position.CDM, league_tier=self.tier))
        for _ in range(3):
            self.players.append(Player(Position.CM, league_tier=self.tier))
        for _ in range(3):
            self.players.append(Player(Position.CAM, league_tier=self.tier))
            
        # Generate forwards
        for _ in range(2):
            self.players.append(Player(Position.LW, league_tier=self.tier))
        for _ in range(2):
            self.players.append(Player(Position.RW, league_tier=self.tier))
        for _ in range(3):
            self.players.append(Player(Position.ST, league_tier=self.tier))

    def generate_youth_squad(self):
        """Generates a smaller youth squad"""
        # Generate 1-2 players for each position
        self.players.append(Player(Position.GK, youth=True, league_tier=self.tier))
        
        for position in [Position.CB, Position.WB, Position.CDM, Position.CM, 
                        Position.CAM, Position.LW, Position.RW, Position.ST]:
            for _ in range(random.randint(1, 2)):
                self.players.append(Player(position, youth=True, league_tier=self.tier))

    def get_starting_eleven(self):
        """Returns the best eleven players based on current formation and form"""
        formation_map = {
            "4-3-3": {
                Position.GK: 1,
                Position.CB: 2,
                Position.WB: 2,
                Position.CM: 2,
                Position.CAM: 1,
                Position.LW: 1,
                Position.RW: 1,
                Position.ST: 1
            },
            "4-4-2": {
                Position.GK: 1,
                Position.CB: 2,
                Position.WB: 2,
                Position.CM: 1,
                Position.CAM: 1,
                Position.LW: 1,
                Position.RW: 1,
                Position.ST: 2
            },
            # Add more formations as needed
        }
        
        required_positions = formation_map[self.formation]
        starting_eleven = []
        
        # Sort players by combined rating within their position
        for position, count in required_positions.items():
            position_players = [p for p in self.players if p.position == position]
            
            # Calculate combined rating (50% overall, 50% average match rating)
            def get_combined_rating(player):
                overall = player.overall_rating
                match_form = player.get_average_rating("last5")  # Use last 5 matches for form
                # Convert match rating (1-10 scale) to same scale as overall (1-99)
                match_form_scaled = (match_form - 1) * (99 - 1) / (10 - 1) + 1
                return (overall + match_form_scaled) / 2
            
            position_players.sort(key=get_combined_rating, reverse=True)
            
            # For each required position
            for _ in range(count):
                if not position_players:
                    continue
                    
                # Get the top rated players for this position
                top_players = []
                top_rating = get_combined_rating(position_players[0])
                
                # Consider players within 10 points of the best player
                for player in position_players:
                    if top_rating - get_combined_rating(player) <= 10:
                        top_players.append(player)
                    else:
                        break
                
                # Give lower rated players a chance based on how close they are to the top
                weights = []
                for player in top_players:
                    rating_diff = top_rating - get_combined_rating(player)
                    # Weight calculation: higher weight for smaller differences
                    weight = 1.0 - (rating_diff / 10)  # 1.0 to 0.5 weight range
                    weights.append(weight)
                
                # Select a player using weighted random choice
                selected_player = random.choices(top_players, weights=weights, k=1)[0]
                starting_eleven.append(selected_player)
                position_players.remove(selected_player)
            
        return starting_eleven

    def get_squad_rating(self):
        """Returns the average rating of the starting eleven"""
        starting_eleven = self.get_starting_eleven()
        return sum(player.overall_rating for player in starting_eleven) / len(starting_eleven)

    def get_youth_prospects(self):
        """Returns youth players who might be ready for promotion"""
        if not self.is_youth_team:
            return []
            
        # Get the senior team (parent team)
        senior_team_name = self.name.replace(" Youth", "")
        senior_team = None
        for league in self.game.leagues.values():
            for team in league.teams:
                if team.name == senior_team_name:
                    senior_team = team
                    break
            if senior_team:
                break
                
        if not senior_team:
            return []
            
        prospects = []
        
        for player in self.players:
            # Get average rating of senior players in the same position
            senior_players = senior_team.get_players_by_position(player.position)
            
            # Calculate player's form rating (last 5 matches)
            form_rating = player.get_average_rating("last5")
            # Convert form rating (1-10 scale) to overall rating scale (1-99)
            form_rating_scaled = (form_rating - 1) * (99 - 1) / (10 - 1) + 1
            
            # Combined rating is 70% overall rating, 30% form rating
            combined_rating = (player.overall_rating * 0.7) + (form_rating_scaled * 0.3)
            
            if not senior_players:
                # If no senior players in this position, use a default threshold of 65
                position_threshold = 65
            else:
                avg_rating = sum(p.overall_rating for p in senior_players) / len(senior_players)
                position_threshold = avg_rating - 5  # Player should be within 5 points of position average
            
            # Player is eligible if their combined rating meets the threshold
            if combined_rating >= position_threshold:
                prospects.append(player)
                
        return prospects

    def promote_youth_player(self, player):
        """Removes a player from youth squad (should be added to senior team)"""
        if player in self.players:
            self.players.remove(player)
            return True
        return False

    def add_player(self, player):
        """Adds a player to the squad"""
        self.players.append(player)

    def remove_player(self, player):
        """Removes a player from the squad"""
        if player in self.players:
            self.players.remove(player)
            return True
        return False

    def get_players_by_position(self, position):
        """Returns all players in a specific position"""
        return [p for p in self.players if p.position == position]

    def __str__(self):
        return f"{self.name} - Squad Size: {len(self.players)} - Average Rating: {self.get_squad_rating():.1f}" 