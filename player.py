import random
import names
from enum import Enum
from colorama import Fore, Style

class Position(Enum):
    GK = "Goalkeeper"
    CB = "Center Back"
    WB = "Wing Back"
    CDM = "Defensive Midfielder"
    CM = "Central Midfielder"
    CAM = "Attacking Midfielder"
    LW = "Left Wing"
    RW = "Right Wing"
    ST = "Striker"

    @property
    def abbreviation(self):
        """Returns the abbreviated form of the position"""
        abbrev_map = {
            Position.GK: "GK",
            Position.CB: "CB",
            Position.WB: "WB",
            Position.CDM: "CDM",
            Position.CM: "CM",
            Position.CAM: "CAM",
            Position.LW: "LW",
            Position.RW: "RW",
            Position.ST: "ST"
        }
        return abbrev_map[self]

class Personality(Enum):
    MAVERICK = "Maverick"
    HEARTBEAT = "Heartbeat"
    VITROSO = "Vitroso"

    @property
    def development_traits(self):
        """Returns development traits for each personality"""
        traits = {
            "MAVERICK": {
                "development_speed": 1.2,  # Faster development
                "consistency": 0.7,  # Less consistent
                "preferred_attributes": ["dribbling", "finishing", "dribbling_skills"],
                "description": "Quick learner but inconsistent. Excels in technical skills."
            },
            "HEARTBEAT": {
                "development_speed": 0.9,  # Slower but steady
                "consistency": 1.3,  # More consistent
                "preferred_attributes": ["playmaking", "passing", "stamina"],
                "description": "Steady, consistent development. Strong mental growth."
            },
            "VITROSO": {
                "development_speed": 1.1,  # Above average
                "consistency": 1.0,  # Balanced
                "preferred_attributes": ["dribbling", "passing", "accuracy"],
                "description": "Well-rounded development. Good technical and mental growth."
            }
        }
        return traits[self.name]

class Player:
    def __init__(self, position, age=None, youth=False, league_tier=1):
        self.name = names.get_full_name(gender='male')
        self.position = position
        
        # More realistic age distribution for youth players
        if youth and not age:
            # Weighted random choice for youth ages:
            # 14: 10% chance
            # 15: 25% chance
            # 16: 35% chance
            # 17: 25% chance
            # 18: 5% chance
            age_weights = [0.10, 0.25, 0.35, 0.25, 0.05]
            self.age = random.choices([14, 15, 16, 17, 18], weights=age_weights)[0]
        else:
            self.age = age if age else random.randint(20, 35)
            
        self.youth = youth
        self.league_tier = league_tier
        
        # Add potential and scouting attributes
        self.true_potential = 0  # Actual potential (hidden)
        self.potential_uncertainty = 15 if youth else 5  # Higher uncertainty for youth
        self.scouting_reports = []  # List of scouting observations
        self.matches_scouted = 0  # Number of matches scouted
        self.development_rate = 1.0  # Base development rate
        
        # Initialize attributes
        self.attributes = {
            "playmaking": 0,
            "passing": 0,
            "speed": 0,
            "overall_iq": 0,
            "tackling": 0,
            "attacking_iq": 0,
            "midfield_iq": 0,
            "defensive_iq": 0,
            "dribbling": 0,
            "dribbling_skills": 0,
            "finishing": 0,
            "jumping": 0,
            "long_balls": 0,
            "stamina": 0,
            "strength": 0,
            "accuracy": 0,
            "fk_pk_ability": 0,
            "off_ball_movement": 0  # New attribute for getting open
        }

        # GK specific attributes
        self.gk_attributes = {
            "diving": 0,
            "handling": 0,
            "positioning": 0,
            "kicking": 0,
            "field_skills": 0
        }

        # Match state attributes
        self.open = 0  # How open the player is
        self.on_run = 0  # If player is making a run (0 for no, >0 for run rating)
        self.has_ball = False

        # Current match statistics
        self.stats = {
            "passes_attempted": 0,
            "passes_completed": 0,
            "shots": 0,
            "shots_on_target": 0,
            "goals": 0,
            "assists": 0,
            "tackles_attempted": 0,
            "tackles_won": 0,
            "saves": 0,  # For goalkeepers
            "clean_sheets": 0  # For goalkeepers
        }

        # Season statistics
        self.season_stats = {
            "matches_played": 0,
            "minutes_played": 0,
            "passes_attempted": 0,
            "passes_completed": 0,
            "shots": 0,
            "shots_on_target": 0,
            "goals": 0,
            "assists": 0,
            "tackles_attempted": 0,
            "tackles_won": 0,
            "saves": 0,
            "clean_sheets": 0,
            "yellow_cards": 0,
            "red_cards": 0
        }

        # Career statistics
        self.career_stats = {
            "matches_played": 0,
            "minutes_played": 0,
            "passes_attempted": 0,
            "passes_completed": 0,
            "shots": 0,
            "shots_on_target": 0,
            "goals": 0,
            "assists": 0,
            "tackles_attempted": 0,
            "tackles_won": 0,
            "saves": 0,
            "clean_sheets": 0,
            "yellow_cards": 0,
            "red_cards": 0
        }

        # Set personality probabilities based on position
        self.set_personality_probabilities()
        # Generate attributes based on position
        self.generate_attributes()

    def set_personality_probabilities(self):
        """Sets personality probabilities based on position"""
        position_personalities = {
            Position.GK: [0.2, 0.5, 0.3],  # [Maverick, Heartbeat, Vitroso]
            Position.CB: [0.1, 0.6, 0.3],
            Position.WB: [0.2, 0.3, 0.5],
            Position.CDM: [0.1, 0.6, 0.3],
            Position.CM: [0.2, 0.3, 0.5],
            Position.CAM: [0.3, 0.2, 0.5],
            Position.LW: [0.4, 0.1, 0.5],
            Position.RW: [0.4, 0.1, 0.5],
            Position.ST: [0.5, 0.2, 0.3]
        }
        self.personality_probabilities = position_personalities[self.position]
        self.personality = self.get_personality()

    def get_personality(self):
        """Returns a personality based on probabilities"""
        return random.choices(
            [Personality.MAVERICK, Personality.HEARTBEAT, Personality.VITROSO],
            weights=self.personality_probabilities
        )[0]

    def generate_attributes(self):
        """Generates attributes based on position and personality"""
        # Wider base range for more variety
        if self.youth:
            # Calculate age factor (14-18 years old)
            # Younger players get lower base ratings
            age_factor = (self.age - 14) / 4  # 0.0 to 1.0 scale
            
            # Create different tiers of youth players based on potential
            player_tier = random.random()
            if player_tier < 0.02:  # 2% chance for wonderkid
                base_range = (45 + (age_factor * 20), 55 + (age_factor * 20))  # 45-65 to 55-75
                potential_range = (88, 95)  # Exceptional potential
            elif player_tier < 0.15:  # 13% chance for highly promising
                base_range = (40 + (age_factor * 20), 50 + (age_factor * 20))  # 40-60 to 50-70
                potential_range = (82, 89)
            elif player_tier < 0.35:  # 20% chance for solid prospect
                base_range = (35 + (age_factor * 20), 45 + (age_factor * 20))  # 35-55 to 45-65
                potential_range = (75, 83)
            elif player_tier < 0.70:  # 35% chance for average youth
                base_range = (30 + (age_factor * 20), 40 + (age_factor * 20))  # 30-50 to 40-60
                potential_range = (70, 76)
            else:  # 30% chance for raw talent
                base_range = (25 + (age_factor * 20), 35 + (age_factor * 20))  # 25-45 to 35-55
                potential_range = (65, 71)
            
            # Adjust ranges based on league tier (higher tier = better youth players)
            tier_bonus = max(0, (8 - self.league_tier) * 2)  # Tier 1 = +14, Tier 7 = +2
            base_range = (base_range[0] + tier_bonus, base_range[1] + tier_bonus)
            
            # Set true potential and ensure it's higher than current max rating
            max_possible_rating = base_range[1]
            min_potential = max(potential_range[0], max_possible_rating + 5)  # At least 5 points higher
            
            # Handle case where min_potential would exceed potential_range[1]
            if min_potential >= potential_range[1]:
                # Set potential to the maximum allowed for this tier
                self.true_potential = potential_range[1]
            else:
                # Normal case - random value between min_potential and max allowed
                self.true_potential = random.randint(min_potential, potential_range[1])
            
            # Generate initial scouting report
            self._generate_scouting_report()
        else:
            # Create different tiers of senior players
            player_tier = random.random()
            if player_tier < 0.05:  # 5% chance for exceptional players
                base_range = (85, 95)
            elif player_tier < 0.25:  # 20% chance for very good players
                base_range = (78, 88)
            elif player_tier < 0.55:  # 30% chance for above average players
                base_range = (72, 82)
            elif player_tier < 0.85:  # 30% chance for average players
                base_range = (65, 75)
            else:  # 15% chance for below average players
                base_range = (58, 68)
            
            # Senior players have more accurate potential assessment
            self.true_potential = min(99, self.overall_rating + random.randint(0, 3))

        # Position-specific attribute ranges
        if self.position == Position.GK:
            self._generate_goalkeeper_attributes(base_range)
        elif self.position in [Position.CB, Position.WB]:
            self._generate_defender_attributes(base_range)
        elif self.position in [Position.CDM, Position.CM]:
            self._generate_midfielder_attributes(base_range)
        elif self.position in [Position.CAM, Position.LW, Position.RW]:
            self._generate_attacking_midfielder_attributes(base_range)
        elif self.position == Position.ST:
            self._generate_striker_attributes(base_range)

        # Apply personality modifiers
        self._apply_personality_modifiers()

    def _generate_goalkeeper_attributes(self, base_range):
        """Generates goalkeeper-specific attributes"""
        # Goalkeepers get slightly higher base attributes in their specialty
        gk_range = (base_range[0] + 5, base_range[1] + 5)
        for attr in self.gk_attributes:
            self.gk_attributes[attr] = random.randint(gk_range[0], gk_range[1])
        # Basic field attributes for goalkeepers are lower
        for attr in self.attributes:
            self.attributes[attr] = random.randint(35, 55)  # Even lower field skills

    def _generate_defender_attributes(self, base_range):
        defensive_attrs = ["tackling", "defensive_iq", "strength", "jumping"]
        for attr in self.attributes:
            if attr in defensive_attrs:
                self.attributes[attr] = random.randint(base_range[0] + 8, base_range[1] + 8)
            elif attr == "off_ball_movement":  # Special case for off_ball_movement
                if self.position == Position.WB:  # Wing backs need decent movement
                    self.attributes[attr] = random.randint(base_range[0] + 4, base_range[1] + 4)
                else:  # Center backs need less
                    self.attributes[attr] = random.randint(base_range[0] - 3, base_range[1] - 3)
            else:
                self.attributes[attr] = random.randint(base_range[0] - 8, base_range[1] - 8)

    def _generate_midfielder_attributes(self, base_range):
        midfield_attrs = ["playmaking", "passing", "midfield_iq", "stamina"]
        movement_bonus = 3  # Smaller bonus for midfielders
        for attr in self.attributes:
            if attr in midfield_attrs:
                self.attributes[attr] = random.randint(base_range[0] + 8, base_range[1] + 8)
            elif attr == "off_ball_movement":  # Special case for off_ball_movement
                self.attributes[attr] = random.randint(base_range[0] + movement_bonus, base_range[1] + movement_bonus)
            else:
                self.attributes[attr] = random.randint(base_range[0] - 5, base_range[1] - 5)

    def _generate_attacking_midfielder_attributes(self, base_range):
        attacking_attrs = ["dribbling", "passing", "attacking_iq", "speed", "off_ball_movement"]  # Added off_ball_movement
        for attr in self.attributes:
            if attr in attacking_attrs:
                self.attributes[attr] = random.randint(base_range[0] + 8, base_range[1] + 8)
            else:
                self.attributes[attr] = random.randint(base_range[0] - 5, base_range[1] - 5)

    def _generate_striker_attributes(self, base_range):
        striker_attrs = ["finishing", "attacking_iq", "dribbling_skills", "off_ball_movement"]  # Added off_ball_movement
        for attr in self.attributes:
            if attr in striker_attrs:
                self.attributes[attr] = random.randint(base_range[0] + 8, base_range[1] + 8)
            else:
                self.attributes[attr] = random.randint(base_range[0] - 5, base_range[1] - 5)

    def _apply_personality_modifiers(self):
        """Applies attribute modifiers based on personality"""
        if self.personality == Personality.MAVERICK:
            self._apply_maverick_modifiers()
        elif self.personality == Personality.HEARTBEAT:
            self._apply_heartbeat_modifiers()
        elif self.personality == Personality.VITROSO:
            self._apply_vitroso_modifiers()

    def _apply_maverick_modifiers(self):
        """Applies Maverick personality modifiers"""
        increase_attrs = ["dribbling", "finishing", "dribbling_skills"]
        decrease_attrs = ["playmaking", "passing", "long_balls"]
        
        for attr in increase_attrs:
            self.attributes[attr] = min(99, self.attributes[attr] + 8)
        for attr in decrease_attrs:
            self.attributes[attr] = max(1, self.attributes[attr] - 8)

    def _apply_heartbeat_modifiers(self):
        """Applies Heartbeat personality modifiers"""
        increase_attrs = ["playmaking", "passing", "long_balls"]
        decrease_attrs = ["dribbling", "dribbling_skills", "finishing"]
        
        for attr in increase_attrs:
            self.attributes[attr] = min(99, self.attributes[attr] + 8)
        for attr in decrease_attrs:
            self.attributes[attr] = max(1, self.attributes[attr] - 8)

    def _apply_vitroso_modifiers(self):
        """Applies Vitroso personality modifiers"""
        increase_attrs = ["dribbling", "passing", "accuracy"]
        decrease_attrs = ["dribbling_skills", "long_balls"]
        
        for attr in increase_attrs:
            self.attributes[attr] = min(99, self.attributes[attr] + 8)
        for attr in decrease_attrs:
            self.attributes[attr] = max(1, self.attributes[attr] - 8)

    @property
    def overall_rating(self):
        """Calculates overall rating based on position-specific attributes"""
        if self.position == Position.GK:
            return sum(self.gk_attributes.values()) / len(self.gk_attributes)
        
        # Weight attributes based on position
        weights = self._get_position_weights()
        weighted_sum = sum(self.attributes[attr] * weight 
                         for attr, weight in weights.items())
        return weighted_sum / sum(weights.values())

    def _get_position_weights(self):
        """Returns attribute weights based on position"""
        weights = {attr: 1 for attr in self.attributes}
        
        # Position-specific weights for off_ball_movement
        if self.position == Position.ST:
            weights["off_ball_movement"] = 2.5  # Very important for strikers
        elif self.position in [Position.LW, Position.RW]:
            weights["off_ball_movement"] = 2.2  # Very important for wingers
        elif self.position == Position.CAM:
            weights["off_ball_movement"] = 2.0  # Important for attacking midfielders
        elif self.position in [Position.CM, Position.CDM]:
            weights["off_ball_movement"] = 1.5  # Moderately important for midfielders
        elif self.position == Position.WB:
            weights["off_ball_movement"] = 1.3  # Somewhat important for wing backs
        else:
            weights["off_ball_movement"] = 1.0  # Less important for other positions
        
        if self.position in [Position.CB, Position.WB]:
            defensive_attrs = ["tackling", "defensive_iq", "strength", "jumping"]
            for attr in defensive_attrs:
                weights[attr] = 2
        elif self.position in [Position.CDM, Position.CM]:
            midfield_attrs = ["playmaking", "passing", "midfield_iq", "stamina"]
            for attr in midfield_attrs:
                weights[attr] = 2
        elif self.position in [Position.CAM, Position.LW, Position.RW]:
            attacking_attrs = ["dribbling", "passing", "attacking_iq", "speed"]
            for attr in attacking_attrs:
                weights[attr] = 2
        elif self.position == Position.ST:
            striker_attrs = ["finishing", "attacking_iq", "dribbling_skills"]
            for attr in striker_attrs:
                weights[attr] = 2
                
        return weights

    def _generate_scouting_report(self):
        """Generates a detailed scouting report for youth players"""
        if not self.youth:
            return

        # Calculate attribute strengths and weaknesses
        strengths = []
        weaknesses = []
        for attr, value in self.attributes.items():
            if value >= 65:
                strengths.append(attr)
            elif value <= 45:
                weaknesses.append(attr)

        # Generate personality-based observations
        personality_traits = self.personality.development_traits
        
        # Calculate potential range based on uncertainty
        # The range will always include true_potential and gets narrower with more scouting
        uncertainty_range = self.potential_uncertainty
        potential_range = f"{max(1, self.true_potential - uncertainty_range)}-{min(99, self.true_potential + uncertainty_range)}"
        
        report = {
            "date_scouted": self.matches_scouted,
            "current_ability": f"{self.overall_rating:.1f}",
            "potential_range": potential_range,
            "strengths": random.sample(strengths, min(3, len(strengths))) if strengths else ["None identified"],
            "weaknesses": random.sample(weaknesses, min(2, len(weaknesses))) if weaknesses else ["None identified"],
            "personality_notes": personality_traits["description"],
            "development_prediction": self._get_development_prediction()
        }
        
        self.scouting_reports.append(report)

    def _get_development_prediction(self):
        """Generates a development prediction based on attributes and personality"""
        personality_traits = self.personality.development_traits
        development_speed = personality_traits["development_speed"]
        consistency = personality_traits["consistency"]
        
        if development_speed >= 1.2:
            speed_text = "Rapid"
        elif development_speed >= 1.0:
            speed_text = "Good"
        else:
            speed_text = "Steady"
            
        if consistency >= 1.2:
            consistency_text = "Very Consistent"
        elif consistency >= 1.0:
            consistency_text = "Consistent"
        else:
            consistency_text = "Inconsistent"
            
        return f"{speed_text} development, {consistency_text} progression"

    def improve_attributes(self, training_focus=None):
        """Improves player attributes based on age, potential, personality, and training focus"""
        # Get personality-based development modifiers
        personality_traits = self.personality.development_traits
        development_speed = personality_traits["development_speed"]
        consistency = personality_traits["consistency"]
        preferred_attributes = personality_traits["preferred_attributes"]

        # Calculate maximum possible improvement based on age and potential
        if self.age >= 32:  # Older players improve less
            max_improvement = 1
        elif self.age <= 23:  # Young players improve more
            # Higher improvement chance if current rating is below potential
            rating_gap = max(0, self.true_potential - self.overall_rating)
            max_improvement = min(5, 3 + (rating_gap // 10))  # Up to +5 for players far below potential
        else:
            max_improvement = 2

        # Apply personality development speed modifier
        max_improvement = max_improvement * development_speed

        # Improve focused attributes more
        if training_focus:
            # Base improvement
            improvement = random.randint(1, int(max_improvement))
            
            # Bonus for preferred attributes
            if training_focus in preferred_attributes:
                improvement += 1
                
            # Apply consistency modifier
            if random.random() < consistency:
                improvement = max(1, int(improvement))
            else:
                improvement = max(0, int(improvement * 0.5))
                
            # Ensure we don't exceed potential
            self.attributes[training_focus] = min(self.true_potential, 
                self.attributes[training_focus] + improvement)

        # Random small improvements to other attributes
        for attr in self.attributes:
            if attr != training_focus and random.random() < 0.3:  # 30% chance
                # Base improvement
                improvement = random.randint(0, int(max_improvement))
                
                # Bonus for preferred attributes
                if attr in preferred_attributes:
                    improvement += 1
                    
                # Apply consistency modifier
                if random.random() < consistency:
                    improvement = max(0, int(improvement))
                else:
                    improvement = max(0, int(improvement * 0.5))
                    
                # Ensure we don't exceed potential
                if self.attributes[attr] < self.true_potential:
                    self.attributes[attr] = min(self.true_potential,
                        self.attributes[attr] + improvement)

        # Update scouted potential and generate new scouting report
        if self.youth:
            self.matches_scouted += 1
            self.potential_uncertainty = max(5, 15 - (self.matches_scouted // 5))
            self._generate_scouting_report()

    def might_leave_youth_team(self):
        """Checks if a youth player might leave for another team"""
        if not self.youth:
            return False, None
            
        if self.age > 18:
            # Higher chance of leaving as they get older
            age_factor = (self.age - 18) * 0.2  # 20% increase per year over 18
            base_chance = 0.3  # 30% base chance
            total_chance = min(0.9, base_chance + age_factor)  # Cap at 90%
            
            # Better players are more likely to be poached
            if self.overall_rating >= 70:
                total_chance += 0.2
            elif self.overall_rating >= 65:
                total_chance += 0.1
                
            if random.random() < total_chance:
                reason = f"Age {self.age}, Rating {self.overall_rating:.1f}"
                return True, reason
                
        return False, None

    def get_latest_scouting_report(self):
        """Returns a formatted string of the latest scouting report"""
        if not self.scouting_reports:
            return "No scouting reports available."
            
        report = self.scouting_reports[-1]
        
        # Get season stats if available, otherwise match stats
        stats = self.season_stats if any(self.season_stats.values()) else self.stats
        
        stats_display = []
        if stats.get("matches_played", 0) > 0:  # Use get() with default value
            stats_display.extend([
                f"Matches Played: {stats.get('matches_played', 0)}",
                f"Minutes Played: {stats.get('minutes_played', 0)}"
            ])
            
            if self.position == Position.GK:
                stats_display.extend([
                    f"Clean Sheets: {stats.get('clean_sheets', 0)}",
                    f"Saves: {stats.get('saves', 0)}"
                ])
            else:
                goals = stats.get('goals', 0)
                assists = stats.get('assists', 0)
                passes_completed = stats.get('passes_completed', 0)
                passes_attempted = stats.get('passes_attempted', 0)
                pass_accuracy = (passes_completed/max(1, passes_attempted)*100) if passes_attempted > 0 else 0
                
                stats_display.extend([
                    f"Goals: {goals}",
                    f"Assists: {assists}",
                    f"Pass Accuracy: {passes_completed}/{passes_attempted} ({pass_accuracy:.1f}%)"
                ])
                
                if self.position in [Position.CB, Position.WB, Position.CDM]:
                    tackles_won = stats.get('tackles_won', 0)
                    tackles_attempted = stats.get('tackles_attempted', 0)
                    tackle_accuracy = (tackles_won/max(1, tackles_attempted)*100) if tackles_attempted > 0 else 0
                    stats_display.append(
                        f"Tackles Won: {tackles_won}/{tackles_attempted} ({tackle_accuracy:.1f}%)"
                    )
                elif self.position in [Position.ST, Position.LW, Position.RW, Position.CAM]:
                    shots_on_target = stats.get('shots_on_target', 0)
                    shots = stats.get('shots', 0)
                    shot_accuracy = (shots_on_target/max(1, shots)*100) if shots > 0 else 0
                    stats_display.append(
                        f"Shots on Target: {shots_on_target}/{shots} ({shot_accuracy:.1f}%)"
                    )
        
        return f"""
{Fore.CYAN}Scouting Report for {self.name}{Style.RESET_ALL}
Age: {self.age}
Position: {self.position.value}
Personality: {self.personality.value}

Current Ability: {report['current_ability']}
Current Rating: {self.overall_rating:.1f}
Potential Range: {report['potential_range']}

{Fore.GREEN}Strengths:{Style.RESET_ALL}
{', '.join(report['strengths'])}

{Fore.RED}Areas for Improvement:{Style.RESET_ALL}
{', '.join(report['weaknesses'])}

{Fore.YELLOW}Development Outlook:{Style.RESET_ALL}
{report['personality_notes']}
{report['development_prediction']}

{Fore.CYAN}Performance Statistics:{Style.RESET_ALL}
{chr(10).join(stats_display) if stats_display else "No match statistics available yet"}

Matches Scouted: {self.matches_scouted}
Scouting Certainty: {100 - (self.potential_uncertainty / 15 * 100):.0f}%
"""

    def update_season_stats(self):
        """Updates season statistics with current match statistics"""
        # Only increment matches_played if player was in the starting eleven
        # This is handled by the Match class when it calls this method
        for stat in self.stats:
            if stat in self.season_stats:
                self.season_stats[stat] += self.stats[stat]

    def update_career_stats(self):
        """Updates career statistics with current match statistics"""
        # Only increment matches_played if player was in the starting eleven
        # This is handled by the Match class when it calls this method
        for stat in self.stats:
            if stat in self.career_stats:
                self.career_stats[stat] += self.stats[stat]

    def get_stats_display(self, stat_type="match"):
        """Returns a formatted string of player statistics"""
        stats_dict = {
            "match": self.stats,
            "season": self.season_stats,
            "career": self.career_stats
        }[stat_type]

        stats_str = []
        if "matches_played" in stats_dict:
            stats_str.append(f"Matches Played: {stats_dict['matches_played']}")
            stats_str.append(f"Minutes Played: {stats_dict['minutes_played']}")

        stats_str.extend([
            f"Goals: {stats_dict['goals']}",
            f"Assists: {stats_dict['assists']}",
            f"Shots: {stats_dict['shots']} ({stats_dict['shots_on_target']} on target)",
            f"Pass Accuracy: {stats_dict['passes_completed']}/{stats_dict['passes_attempted']} " +
            f"({(stats_dict['passes_completed']/max(1, stats_dict['passes_attempted'])*100):.1f}%)",
            f"Tackles Won: {stats_dict['tackles_won']}/{stats_dict['tackles_attempted']} " +
            f"({(stats_dict['tackles_won']/max(1, stats_dict['tackles_attempted'])*100):.1f}%)"
        ])

        if self.position == Position.GK:
            stats_str.extend([
                f"Saves: {stats_dict['saves']}",
                f"Clean Sheets: {stats_dict['clean_sheets']}"
            ])

        if stat_type != "match":
            stats_str.extend([
                f"Yellow Cards: {stats_dict['yellow_cards']}",
                f"Red Cards: {stats_dict['red_cards']}"
            ])

        return "\n".join(stats_str)

    def __str__(self):
        if self.youth:
            # Calculate potential range based on current uncertainty
            uncertainty_range = self.potential_uncertainty
            potential_range = f"{max(1, self.true_potential - uncertainty_range)}-{min(99, self.true_potential + uncertainty_range)}"
            return f"{self.name} ({self.age}) - {self.position.value} - {self.personality.value} - Overall: {self.overall_rating:.1f} - Potential: {potential_range}"
        return f"{self.name} ({self.age}) - {self.position.value} - {self.personality.value} - Overall: {self.overall_rating:.1f}" 