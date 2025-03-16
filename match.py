import random
import time
from colorama import Fore, Style
from player import Player, Position, Personality

class MatchEvent:
    def __init__(self, minute, description, player=None, team=None, event_type=None):
        self.minute = minute
        self.description = description
        self.player = player
        self.team = team
        self.event_type = event_type

class Match:
    # Position distances from goal (0 = very close, 1 = very far)
    position_distances = {
        Position.ST: 0.1,
        Position.LW: 0.2,
        Position.RW: 0.2,
        Position.CAM: 0.4,
        Position.CM: 0.6,
        Position.CDM: 0.7,
        Position.WB: 0.8,
        Position.CB: 0.9,
        Position.GK: 1.0
    }

    def __init__(self, home_team, away_team, commentary_delay=2, action_frequency=1, silent=False):
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = 0
        self.away_score = 0
        self.minute = 0
        self.commentary_delay = commentary_delay
        self.action_frequency = action_frequency
        self.events = []
        self.silent = silent  # New flag for silent simulation
        
        # Team colors
        self.home_color = Fore.BLUE
        self.away_color = Fore.RED
        
        # Match state
        self.possession_team = None
        self.player_with_ball = None
        self.last_action = None
        
        # Initialize player positions and states
        self.home_players = home_team.get_starting_eleven()
        self.away_players = away_team.get_starting_eleven()
        
        # Reset match stats
        for player in self.home_players + self.away_players:
            for stat in player.stats:
                player.stats[stat] = 0

    def _get_player_display(self, player):
        """Returns player name with team name and position in team color"""
        is_home = player in self.home_players
        team_name = self.home_team.name if is_home else self.away_team.name
        team_color = self.home_color if is_home else self.away_color
        return f"{team_color}{player.name} ({player.position.abbreviation}, {team_name}){Style.RESET_ALL}"

    def simulate(self):
        """Simulates the entire match"""
        if not self.silent:
            print(f"\n{Fore.CYAN}Match Starting: {self.home_color}{self.home_team.name}{Style.RESET_ALL} vs {self.away_color}{self.away_team.name}{Style.RESET_ALL}")
            print("Press Enter at any time to skip to the end of the match...")
        
        # Determine initial possession
        self.possession_team = random.choice([self.home_team, self.away_team])
        self.player_with_ball = self._get_random_midfielder(self.possession_team)
        
        import select
        import sys
        
        # Simulate 90 minutes
        while self.minute < 90:
            self.minute += 1
            
            # Check for Enter key press (skip to end) only if not silent
            if not self.silent and sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                line = sys.stdin.readline()
                if line == '\n':
                    if not self.silent:
                        print(f"\n{Fore.YELLOW}Skipping to end of match...{Style.RESET_ALL}")
                    # Simulate remaining minutes without commentary
                    while self.minute < 90:
                        self.minute += 1
                        if self.minute % self.action_frequency == 0:
                            self._simulate_action(skip_commentary=True)
                        self._update_player_states()
                    break
            
            if self.minute % self.action_frequency == 0:  # Action frequency based on settings
                self._simulate_action()
                
            # Update player states
            self._update_player_states()
            
        # Print final score only if not silent
        if not self.silent:
            self._print_final_score()
        
    def _simulate_action(self, skip_commentary=False):
        """Simulates a single action in the match"""
        if not self.player_with_ball:
            return
            
        # Determine the defending player
        defender = self._get_closest_defender()
        
        # Calculate pressure on the player
        pressure = self._calculate_pressure(defender)
        
        # Player decides action based on personality and pressure
        action = self._decide_action(pressure)
        
        # Execute the action
        if action == "shoot":
            self._attempt_shot(skip_commentary)
        elif action == "pass":
            self._attempt_pass(skip_commentary)
        elif action == "dribble":
            self._attempt_dribble(defender, skip_commentary)
        elif action == "long_ball":
            self._attempt_long_ball(skip_commentary)

    def _decide_action(self, pressure):
        """Decides what action to take based on position, attributes, personality and situation"""
        player = self.player_with_ball
        
        # Base probabilities based on position
        position_probs = {
            Position.ST: {"shoot": 0.4, "pass": 0.3, "dribble": 0.2, "long_ball": 0.1},
            Position.LW: {"shoot": 0.3, "pass": 0.3, "dribble": 0.3, "long_ball": 0.1},
            Position.RW: {"shoot": 0.3, "pass": 0.3, "dribble": 0.3, "long_ball": 0.1},
            Position.CAM: {"shoot": 0.2, "pass": 0.4, "dribble": 0.3, "long_ball": 0.1},
            Position.CM: {"shoot": 0.1, "pass": 0.5, "dribble": 0.2, "long_ball": 0.2},
            Position.CDM: {"shoot": 0.05, "pass": 0.5, "dribble": 0.15, "long_ball": 0.3},
            Position.WB: {"shoot": 0.05, "pass": 0.5, "dribble": 0.25, "long_ball": 0.2},
            Position.CB: {"shoot": 0.02, "pass": 0.48, "dribble": 0.2, "long_ball": 0.3},
            Position.GK: {"shoot": 0.0, "pass": 0.6, "dribble": 0.1, "long_ball": 0.3}
        }
        
        # Get base probabilities for player's position
        probs = position_probs[player.position].copy()
        
        # Modify based on relevant attributes
        # Shooting probability affected by finishing and attacking_iq
        shoot_skill = (player.attributes["finishing"] * 0.6 + 
                      player.attributes["attacking_iq"] * 0.4) / 100.0
        probs["shoot"] *= (0.5 + shoot_skill)
        
        # Passing probability affected by passing and playmaking
        pass_skill = (player.attributes["passing"] * 0.5 + 
                     player.attributes["playmaking"] * 0.5) / 100.0
        probs["pass"] *= (0.5 + pass_skill)
        
        # Dribbling probability affected by dribbling and dribbling_skills
        dribble_skill = (player.attributes["dribbling"] * 0.5 + 
                        player.attributes["dribbling_skills"] * 0.5) / 100.0
        probs["dribble"] *= (0.5 + dribble_skill)
        
        # Long ball probability affected by long_balls and accuracy
        long_ball_skill = (player.attributes["long_balls"] * 0.6 + 
                          player.attributes["accuracy"] * 0.4) / 100.0
        probs["long_ball"] *= (0.5 + long_ball_skill)
        
        # Modify based on personality
        if player.personality == Personality.MAVERICK:
            probs["shoot"] *= 1.5
            probs["dribble"] *= 1.5
            probs["pass"] *= 0.7
            probs["long_ball"] *= 0.7
        elif player.personality == Personality.HEARTBEAT:
            probs["pass"] *= 1.5
            probs["long_ball"] *= 1.5
            probs["shoot"] *= 0.7
            probs["dribble"] *= 0.7
        elif player.personality == Personality.VITROSO:
            probs["pass"] *= 1.3
            probs["dribble"] *= 1.2
            probs["long_ball"] *= 0.7
            
        # Modify based on pressure and position
        if pressure > 0.7:  # High pressure
            probs["pass"] *= 1.5
            probs["long_ball"] *= 1.3
            probs["dribble"] *= 0.6
            probs["shoot"] *= 0.7
            
        # Modify based on distance to goal
        distance_to_goal = self._calculate_distance_to_goal()
        if distance_to_goal < 0.2:  # Close to goal
            probs["shoot"] *= 2.0
        elif distance_to_goal > 0.7:  # Far from goal
            probs["shoot"] *= 0.3
            
        # Normalize probabilities
        total = sum(probs.values())
        probs = {k: v/total for k, v in probs.items()}
        
        # Choose action
        return random.choices(list(probs.keys()), list(probs.values()))[0]

    def _attempt_shot(self, skip_commentary=False):
        """Attempts a shot on goal"""
        player = self.player_with_ball
        distance = self._calculate_distance_to_goal()
        
        # Base chance of scoring
        score_chance = (player.attributes["finishing"] * 0.5 + 
                       player.attributes["accuracy"] * 0.3 +
                       player.attributes["attacking_iq"] * 0.2) / 100.0
                       
        # Modify based on distance
        score_chance *= (1 - distance)
        
        # Attempt the shot
        player.stats["shots"] += 1
        
        if random.random() < score_chance:
            # Goal!
            if self.possession_team == self.home_team:
                self.home_score += 1
            else:
                self.away_score += 1
                
            player.stats["goals"] += 1
            player.stats["shots_on_target"] += 1
            
            self._add_event(f"{Fore.GREEN}GOAL! {self._get_player_display(player)} scores!{Style.RESET_ALL}", skip_commentary)
        else:
            # Miss or save
            if random.random() < 0.5:  # Shot on target but saved
                player.stats["shots_on_target"] += 1
                self._add_event(f"Shot on target by {self._get_player_display(player)}, but saved!", skip_commentary)
            else:  # Shot off target
                self._add_event(f"Shot by {self._get_player_display(player)} goes wide!", skip_commentary)
                
        # Reset possession
        self._switch_possession()

    def _attempt_pass(self, skip_commentary=False):
        """Attempts a pass to another player"""
        passer = self.player_with_ball
        
        # Find all potential receivers
        teammates = (self.home_players if self.possession_team == self.home_team 
                    else self.away_players)
        potential_receivers = [p for p in teammates if p != passer]
        
        if not potential_receivers:
            return
            
        # Calculate weights for each potential receiver
        receiver_weights = []
        for receiver in potential_receivers:
            weight = self._calculate_pass_weight(passer, receiver)
            receiver_weights.append(weight)
            
        # Normalize weights
        total_weight = sum(receiver_weights)
        if total_weight == 0:
            self._add_event(f"{self._get_player_display(passer)} can't find an open teammate", skip_commentary)
            return
            
        receiver_weights = [w/total_weight for w in receiver_weights]
        
        # Choose receiver based on weights
        receiver = random.choices(potential_receivers, weights=receiver_weights, k=1)[0]
        
        # Calculate pass success chance
        pass_chance = self._calculate_pass_success(passer, receiver)
                      
        # Attempt pass
        passer.stats["passes_attempted"] += 1
        
        if random.random() < pass_chance:
            # Successful pass
            passer.stats["passes_completed"] += 1
            self.player_with_ball = receiver
            
            # Different commentary based on pass type
            passer_pos = self._calculate_distance_to_goal()
            receiver_pos = self.position_distances[receiver.position]
            
            if abs(passer_pos - receiver_pos) > 0.4:  # Long pass
                self._add_event(f"Long pass from {self._get_player_display(passer)} finds {self._get_player_display(receiver)}", skip_commentary)
            elif receiver.on_run > 0:  # Through ball to running player
                self._add_event(f"Great through ball from {self._get_player_display(passer)} to {self._get_player_display(receiver)}", skip_commentary)
            else:  # Normal pass
                self._add_event(f"Nice pass from {self._get_player_display(passer)} to {self._get_player_display(receiver)}", skip_commentary)
        else:
            # Failed pass
            self._add_event(f"{self._get_player_display(passer)}'s pass is intercepted", skip_commentary)
            self._switch_possession()

    def _calculate_pass_weight(self, passer, receiver):
        """Calculates how likely a player is to pass to a specific teammate"""
        weight = 1.0
        
        # Position-based preferences
        position_preferences = {
            Position.GK: {
                Position.CB: 2.0, Position.WB: 1.5, Position.CDM: 1.2,
                Position.CM: 0.8, Position.CAM: 0.4, Position.LW: 0.3,
                Position.RW: 0.3, Position.ST: 0.2, Position.GK: 0.1
            },
            Position.CB: {
                Position.WB: 1.8, Position.CDM: 1.5, Position.CM: 1.2,
                Position.CAM: 0.8, Position.LW: 0.6, Position.RW: 0.6,
                Position.ST: 0.4, Position.GK: 0.3, Position.CB: 0.5
            },
            Position.WB: {
                Position.CM: 1.5, Position.CAM: 1.3, Position.LW: 1.3,
                Position.RW: 1.3, Position.CDM: 1.2, Position.ST: 1.0,
                Position.CB: 0.8, Position.GK: 0.3, Position.WB: 0.5
            },
            Position.CDM: {
                Position.CM: 1.8, Position.WB: 1.5, Position.CAM: 1.3,
                Position.LW: 1.0, Position.RW: 1.0, Position.ST: 0.8,
                Position.CB: 0.7, Position.GK: 0.2, Position.CDM: 0.6
            },
            Position.CM: {
                Position.CAM: 1.8, Position.LW: 1.5, Position.RW: 1.5,
                Position.ST: 1.3, Position.WB: 1.2, Position.CDM: 1.0,
                Position.CB: 0.6, Position.GK: 0.2, Position.CM: 0.8
            },
            Position.CAM: {
                Position.ST: 2.0, Position.LW: 1.8, Position.RW: 1.8,
                Position.CM: 1.2, Position.WB: 1.0, Position.CDM: 0.8,
                Position.CB: 0.4, Position.GK: 0.1, Position.CAM: 0.7
            },
            Position.LW: {
                Position.ST: 2.0, Position.CAM: 1.5, Position.CM: 1.2,
                Position.RW: 1.0, Position.WB: 0.8, Position.CDM: 0.6,
                Position.CB: 0.4, Position.GK: 0.1, Position.LW: 0.5
            },
            Position.RW: {
                Position.ST: 2.0, Position.CAM: 1.5, Position.CM: 1.2,
                Position.LW: 1.0, Position.WB: 0.8, Position.CDM: 0.6,
                Position.CB: 0.4, Position.GK: 0.1, Position.RW: 0.5
            },
            Position.ST: {
                Position.CAM: 1.5, Position.LW: 1.3, Position.RW: 1.3,
                Position.CM: 1.0, Position.WB: 0.7, Position.CDM: 0.5,
                Position.CB: 0.3, Position.GK: 0.1, Position.ST: 0.4
            }
        }
        
        # Apply position preference multiplier
        try:
            weight *= position_preferences[passer.position][receiver.position]
        except KeyError:
            # Fallback weight if position combination is not found
            weight *= 0.5
        
        # Consider how open the receiver is
        weight *= (1.0 + receiver.open)
        
        # Consider if receiver is making a run
        if receiver.on_run > 0:
            # Forwards and attacking midfielders prefer passing to running players
            if passer.position in [Position.CAM, Position.CM, Position.LW, Position.RW]:
                weight *= (1.5 + receiver.on_run)
        
        # Consider passing range based on long_balls attribute
        passer_pos = self._calculate_distance_to_goal()
        receiver_pos = self.position_distances[receiver.position]
        pass_distance = abs(passer_pos - receiver_pos)
        
        if pass_distance > 0.4:  # Long pass
            # Reduce weight if player has poor long passing
            long_pass_ability = (passer.attributes["long_balls"] + passer.attributes["accuracy"]) / 200.0
            weight *= long_pass_ability
        
        # Consider forward progression
        # Reward passes that move the ball forward (except for forwards who might need to pass back)
        if passer.position not in [Position.ST, Position.LW, Position.RW]:
            if receiver_pos < passer_pos:  # Ball moving forward
                weight *= 1.3
        
        return max(0.1, weight)  # Ensure weight is never zero

    def _calculate_pass_success(self, passer, receiver):
        """Calculates the chance of a successful pass"""
        # Base pass chance from passer's attributes
        pass_chance = (passer.attributes["passing"] * 0.4 + 
                      passer.attributes["accuracy"] * 0.3 +
                      passer.attributes["playmaking"] * 0.3) / 100.0
        
        # Modify based on pass distance
        passer_pos = self._calculate_distance_to_goal()
        receiver_pos = self.position_distances[receiver.position]
        pass_distance = abs(passer_pos - receiver_pos)
        
        if pass_distance > 0.4:  # Long pass
            # Use long_balls attribute for long passes
            pass_chance = (passer.attributes["long_balls"] * 0.5 + 
                         passer.attributes["accuracy"] * 0.3 +
                         receiver.attributes["jumping"] * 0.2) / 100.0
        
        # Modify based on receiver's movement
        if receiver.on_run > 0:
            pass_chance *= (0.8 + (receiver.attributes["speed"] / 100.0) * 0.4)
        
        # Modify based on how open the receiver is
        pass_chance *= (0.7 + receiver.open * 0.3)
        
        return min(0.95, pass_chance)  # Cap at 95% success rate

    def _attempt_dribble(self, defender, skip_commentary=False):
        """Attempts to dribble past a defender"""
        attacker = self.player_with_ball
        
        # Calculate dribble success chance
        dribble_chance = (attacker.attributes["dribbling"] * 0.4 + 
                         attacker.attributes["dribbling_skills"] * 0.4 +
                         attacker.attributes["speed"] * 0.2) / 100.0
                         
        # Defender's chance to tackle
        tackle_chance = (defender.attributes["tackling"] * 0.4 +
                        defender.attributes["defensive_iq"] * 0.3 +
                        defender.attributes["strength"] * 0.3) / 100.0
                        
        # Compare chances
        if dribble_chance > tackle_chance:
            self._add_event(f"{self._get_player_display(attacker)} skillfully dribbles past {self._get_player_display(defender)}", skip_commentary)
            attacker.open = min(1.0, attacker.open + 0.2)  # Increased space
        else:
            defender.stats["tackles_won"] += 1
            self._add_event(f"{self._get_player_display(defender)} wins the ball from {self._get_player_display(attacker)}", skip_commentary)
            self.player_with_ball = defender
            self._switch_possession()

    def _attempt_long_ball(self, skip_commentary=False):
        """Attempts a long ball to a forward"""
        passer = self.player_with_ball
        
        # Find potential receivers
        teammates = (self.home_players if self.possession_team == self.home_team 
                    else self.away_players)
        forwards = [p for p in teammates if p.position in [Position.ST, Position.LW, Position.RW]]
        
        if not forwards:
            return
            
        receiver = random.choice(forwards)
        
        # Calculate success chance
        success_chance = (passer.attributes["long_balls"] * 0.5 + 
                        passer.attributes["accuracy"] * 0.3 +
                        receiver.attributes["jumping"] * 0.2) / 100.0
                        
        passer.stats["passes_attempted"] += 1
        
        if random.random() < success_chance:
            passer.stats["passes_completed"] += 1
            self.player_with_ball = receiver
            self._add_event(f"Excellent long ball from {self._get_player_display(passer)} finds {self._get_player_display(receiver)}", skip_commentary)
        else:
            self._add_event(f"{self._get_player_display(passer)}'s long ball is intercepted", skip_commentary)
            self._switch_possession()

    def _get_closest_defender(self):
        """Returns the most appropriate defender to pressure the ball"""
        defenders = (self.away_players if self.possession_team == self.home_team 
                    else self.home_players)
        
        # Prioritize defenders and defensive midfielders
        priority_defenders = [p for p in defenders if p.position in [Position.CB, Position.WB, Position.CDM]]
        
        if priority_defenders:
            return random.choice(priority_defenders)
        return random.choice(defenders)

    def _calculate_pressure(self, defender):
        """Calculates the pressure on the player with the ball"""
        if not defender:
            return 0.0
            
        base_pressure = (defender.attributes["tackling"] * 0.3 +
                        defender.attributes["defensive_iq"] * 0.4 +
                        defender.attributes["speed"] * 0.3) / 100.0
                        
        # Modify based on defender's position
        if defender.position in [Position.CB, Position.WB]:
            base_pressure *= 1.2
            
        return min(1.0, base_pressure)

    def _calculate_distance_to_goal(self):
        """Returns a normalized distance to goal (0 = very close, 1 = very far)"""
        if not self.player_with_ball:
            return 1.0
            
        return self.position_distances[self.player_with_ball.position]

    def _get_random_midfielder(self, team):
        """Returns a random midfielder from the team"""
        players = self.home_players if team == self.home_team else self.away_players
        midfielders = [p for p in players if p.position in [Position.CM, Position.CDM, Position.CAM]]
        return random.choice(midfielders) if midfielders else random.choice(players)

    def _switch_possession(self):
        """Switches possession between teams"""
        self.possession_team = (self.away_team if self.possession_team == self.home_team 
                              else self.home_team)
        self.player_with_ball = self._get_random_midfielder(self.possession_team)

    def _update_player_states(self):
        """Updates player states (openness, runs, etc.)"""
        for player in self.home_players + self.away_players:
            # Update openness
            player.open = random.random()  # Simplified for now
            
            # Decide if player should make a run
            if (player.position in [Position.ST, Position.LW, Position.RW, Position.CAM] and 
                random.random() < 0.3):
                player.on_run = random.random()
            else:
                player.on_run = 0

    def _add_event(self, description, skip_commentary=False):
        """Adds a match event and prints it"""
        event = MatchEvent(self.minute, description)
        self.events.append(event)
        if not skip_commentary and not self.silent:
            print(f"{Fore.YELLOW}[{self.minute}'] {Style.RESET_ALL}{description}")
            time.sleep(self.commentary_delay)

    def _print_final_score(self):
        """Prints the final score and match statistics"""
        if self.silent:
            return
            
        print(f"\nFinal Score:")
        print(f"{self.home_team.name} {self.home_score} - {self.away_score} {self.away_team.name}")
        
        print("\nMatch Statistics:")
        print(f"{self.home_team.name}:")
        self._print_team_stats(self.home_players)
        
        print("\nvs\n")
        
        print(f"{self.away_team.name}:")
        self._print_team_stats(self.away_players)
        
        # Update season and career statistics for players who started
        for player in self.home_players + self.away_players:
            player.update_season_stats()
            player.update_career_stats()

    def _print_team_stats(self, players):
        """Prints statistics for a team"""
        print("Goals:", sum(p.stats["goals"] for p in players))
        print("Shots:", sum(p.stats["shots"] for p in players))
        print("Shots on Target:", sum(p.stats["shots_on_target"] for p in players))
        print("Passes Completed:", sum(p.stats["passes_completed"] for p in players))
        print("Pass Accuracy:", f"{sum(p.stats['passes_completed'] for p in players) / max(1, sum(p.stats['passes_attempted'] for p in players)):.2%}")
        print("Tackles Won:", sum(p.stats["tackles_won"] for p in players)) 