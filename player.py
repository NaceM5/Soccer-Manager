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
        self.retired = False  # New attribute to track retirement status
        
        # Add potential and scouting attributes
        self.true_potential = 0  # Actual potential (hidden)
        self.potential_uncertainty = 15 if youth else 5  # Higher uncertainty for youth
        self.scouting_reports = []  # List of scouting observations
        self.matches_scouted = 0  # Number of matches scouted
        self.development_rate = 1.0  # Base development rate
        
        # Match rating tracking
        self.current_match_rating = 6.0  # Base rating for current match
        self.match_ratings = []  # List of all match ratings
        self.season_ratings = []  # List of ratings for current season
        self.career_ratings = []  # List of all career ratings
        
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

        # Store initial rating for season improvement tracking
        self.season_start_rating = self.overall_rating

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
        # Calculate age factor for senior players
        if not self.youth:
            # Peak age range is 25-29
            if self.age < 21:
                # Young players (20 and under) get lower base ratings
                age_factor = 0.85 + ((self.age - 18) * 0.05)  # 0.85 at 18, increasing to 0.95 at 20
            elif self.age <= 24:
                # Development phase (21-24) approaching peak
                age_factor = 0.95 + ((self.age - 21) * 0.0125)  # 0.95 at 21, increasing to 1.0 at 24
            elif self.age <= 29:
                # Prime years (25-29)
                age_factor = 1.0
            elif self.age <= 32:
                # Early decline (30-32)
                age_factor = 1.0 - ((self.age - 29) * 0.02)  # 1.0 at 29, decreasing to 0.94 at 32
            else:
                # Steeper decline (33+)
                age_factor = 0.94 - ((self.age - 32) * 0.03)  # 0.94 at 32, decreasing by 0.03 per year
        else:
            # Youth players use existing age factor calculation
            age_factor = (self.age - 14) / 4  # 0.0 to 1.0 scale

        # Create different tiers of players based on potential and age
        if self.youth:
            # Youth player generation remains unchanged
            player_tier = random.random()
            if player_tier < 0.02:  # 2% chance for wonderkid
                base_range = (45 + (age_factor * 20), 55 + (age_factor * 20))
                potential_range = (88, 95)
            elif player_tier < 0.15:  # 13% chance for highly promising
                base_range = (40 + (age_factor * 20), 50 + (age_factor * 20))
                potential_range = (82, 89)
            elif player_tier < 0.35:  # 20% chance for solid prospect
                base_range = (35 + (age_factor * 20), 45 + (age_factor * 20))
                potential_range = (75, 83)
            elif player_tier < 0.70:  # 35% chance for average youth
                base_range = (30 + (age_factor * 20), 40 + (age_factor * 20))
                potential_range = (70, 76)
            else:  # 30% chance for raw talent
                base_range = (25 + (age_factor * 20), 35 + (age_factor * 20))
                potential_range = (65, 71)
        else:
            # Senior player generation with age factor applied
            player_tier = random.random()
            if player_tier < 0.05:  # 5% chance for exceptional players
                base_range = (int(85 * age_factor), int(95 * age_factor))
            elif player_tier < 0.25:  # 20% chance for very good players
                base_range = (int(78 * age_factor), int(88 * age_factor))
            elif player_tier < 0.55:  # 30% chance for above average players
                base_range = (int(72 * age_factor), int(82 * age_factor))
            elif player_tier < 0.85:  # 30% chance for average players
                base_range = (int(65 * age_factor), int(75 * age_factor))
            else:  # 15% chance for below average players
                base_range = (int(58 * age_factor), int(68 * age_factor))

        # Adjust ranges based on league tier for youth players
        if self.youth:
            tier_bonus = max(0, (8 - self.league_tier) * 2)
            base_range = (base_range[0] + tier_bonus, base_range[1] + tier_bonus)
            
            # Set true potential and ensure it's higher than current max rating
            max_possible_rating = base_range[1]
            min_potential = max(potential_range[0], max_possible_rating + 5)
            
            if min_potential >= potential_range[1]:
                self.true_potential = potential_range[1]
            else:
                self.true_potential = random.randint(min_potential, potential_range[1])
        else:
            # Senior players have more accurate potential assessment
            # For older players (30+), potential is closer to current rating
            if self.age >= 30:
                potential_boost = random.randint(0, 2)  # Minimal improvement potential
            else:
                potential_boost = random.randint(1, 4)  # More room for improvement
            self.true_potential = min(99, int(base_range[1] * (1 + potential_boost / 100)))

        # Position-specific attribute generation remains unchanged
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

    def improve_attributes(self, training_focus=None, is_match_improvement=False, improvement_amount=0.0):
        """Improves or declines player attributes based on age, potential, personality, and training focus"""
        # Get personality-based development modifiers
        personality_traits = self.personality.development_traits
        development_speed = personality_traits["development_speed"]
        consistency = personality_traits["consistency"]
        preferred_attributes = personality_traits["preferred_attributes"]

        # Define physical attributes that decline faster with age
        physical_attributes = ["speed", "stamina", "strength", "jumping"]
        
        # Calculate attribute changes based on age
        if self.age >= 30:
            # Calculate decline chance and severity based on age
            # More gradual decline starting at 30
            if self.age <= 32:
                # Early decline phase (30-32)
                decline_chance = (self.age - 29) * 0.1  # 10% at 30, up to 30% at 32
                base_decline = 0.3  # Minimal decline
            elif self.age <= 34:
                # Mid decline phase (33-34)
                decline_chance = 0.3 + ((self.age - 32) * 0.1)  # 30-50% chance
                base_decline = 0.5
            else:
                # Late decline phase (35+)
                decline_chance = 0.5 + ((self.age - 34) * 0.1)  # 50%+ chance
                base_decline = 0.8
            
            # Process potential decline for each attribute
            for attr in self.attributes:
                if random.random() < decline_chance:
                    decline = base_decline
                    # Physical attributes decline faster
                    if attr in physical_attributes:
                        decline *= 1.5
                    # Mental attributes decline slower
                    elif attr in ["playmaking", "overall_iq", "attacking_iq", "midfield_iq", "defensive_iq"]:
                        decline *= 0.5
                    
                    # Apply consistency modifier to decline
                    if random.random() < consistency:
                        decline *= 0.7  # More consistent players decline slower
                    
                    # Apply the decline
                    self.attributes[attr] = max(1, self.attributes[attr] - random.uniform(0, decline))
            
            # Also process goalkeeper attributes if applicable
            if self.position == Position.GK:
                for attr in self.gk_attributes:
                    if random.random() < decline_chance:
                        decline = base_decline
                        if random.random() < consistency:
                            decline *= 0.7
                        self.gk_attributes[attr] = max(1, self.gk_attributes[attr] - random.uniform(0, decline))
            
            # Very limited improvement chance for focused attribute
            max_improvement = 0.5
        elif self.age <= 23:
            # Young players improve more
            # Higher improvement chance if current rating is below potential
            rating_gap = max(0, self.true_potential - self.overall_rating)
            
            # Calculate improvement potential based on age and rating gap
            if self.age <= 19:
                # Highest improvement potential (18-19)
                max_improvement = min(6, 4 + (rating_gap // 8))
            elif self.age <= 21:
                # Strong improvement potential (20-21)
                max_improvement = min(5, 3 + (rating_gap // 9))
            else:
                # Good improvement potential (22-23)
                max_improvement = min(4, 2 + (rating_gap // 10))
        elif self.age <= 29:
            # Prime years (24-29)
            # Still room for improvement but more moderate
            rating_gap = max(0, self.true_potential - self.overall_rating)
            max_improvement = min(3, 1 + (rating_gap // 12))
        else:
            # Limited improvement (30+)
            rating_gap = max(0, self.true_potential - self.overall_rating)
            max_improvement = min(1, rating_gap // 15)

        # Apply personality development speed modifier
        max_improvement = max_improvement * development_speed

        # Use provided improvement amount if it's a match-based improvement
        if is_match_improvement and improvement_amount > 0:
            max_improvement = improvement_amount

        # Improve focused attributes more
        if training_focus:
            # Base improvement
            improvement = random.uniform(0, max_improvement)
            
            # Bonus for preferred attributes
            if training_focus in preferred_attributes:
                improvement *= 1.2
                
            # Apply consistency modifier
            if random.random() < consistency:
                improvement = max(0, improvement)
            else:
                improvement = max(0, improvement * 0.7)
                
            # Ensure we don't exceed potential
            if training_focus in self.gk_attributes:
                self.gk_attributes[training_focus] = min(self.true_potential, 
                    self.gk_attributes[training_focus] + improvement)
            else:
                self.attributes[training_focus] = min(self.true_potential, 
                    self.attributes[training_focus] + improvement)

        # Random small improvements to other attributes
        if self.age < 30:  # Only apply random improvements to players under 30
            # Process regular attributes
            for attr in self.attributes:
                if attr != training_focus and random.random() < 0.3:  # 30% chance
                    # Base improvement
                    improvement = random.uniform(0, max_improvement * 0.5)  # Half the focused improvement
                    
                    # Bonus for preferred attributes
                    if attr in preferred_attributes:
                        improvement *= 1.2
                        
                    # Apply consistency modifier
                    if random.random() < consistency:
                        improvement = max(0, improvement)
                    else:
                        improvement = max(0, improvement * 0.7)
                        
                    # Ensure we don't exceed potential
                    if self.attributes[attr] < self.true_potential:
                        self.attributes[attr] = min(self.true_potential,
                            self.attributes[attr] + improvement)
            
            # Process goalkeeper attributes if applicable
            if self.position == Position.GK:
                for attr in self.gk_attributes:
                    if attr != training_focus and random.random() < 0.3:  # 30% chance
                        improvement = random.uniform(0, max_improvement * 0.5)
                        if attr in preferred_attributes:
                            improvement *= 1.2
                        if random.random() < consistency:
                            improvement = max(0, improvement)
                        else:
                            improvement = max(0, improvement * 0.7)
                        if self.gk_attributes[attr] < self.true_potential:
                            self.gk_attributes[attr] = min(self.true_potential,
                                self.gk_attributes[attr] + improvement)

        # Update scouted potential and generate new scouting report
        if self.youth:
            self.matches_scouted += 1
            self.potential_uncertainty = max(5, 15 - (self.matches_scouted // 5))
            self._generate_scouting_report()

    def improve_from_match(self, match_rating):
        """Improves attributes based on match performance"""
        # Calculate improvement chance based on match rating with a more generous curve
        # 6.0 = 10% chance, 7.0 = 30% chance, 8.0 = 60% chance, 9.0 = 90% chance
        improvement_chance = min(0.95, max(0.05, (match_rating - 6.0) / 3.0))
        
        # Add bonus chance for very good performances
        if match_rating >= 8.5:
            improvement_chance = min(0.95, improvement_chance + 0.2)
        
        if random.random() < improvement_chance:
            # Determine which attributes to improve based on position and performance
            if self.position == Position.GK:
                focus_attrs = ["diving", "handling", "positioning"]
            elif self.position in [Position.CB, Position.WB]:
                focus_attrs = ["tackling", "defensive_iq", "strength", "jumping"]
            elif self.position in [Position.CDM, Position.CM]:
                focus_attrs = ["playmaking", "passing", "midfield_iq", "stamina"]
            elif self.position in [Position.CAM, Position.LW, Position.RW]:
                focus_attrs = ["dribbling", "passing", "attacking_iq", "speed"]
            elif self.position == Position.ST:
                focus_attrs = ["finishing", "attacking_iq", "dribbling_skills"]
            
            # Randomly choose a focus attribute
            training_focus = random.choice(focus_attrs)
            
            # Calculate improvement amount based on match rating and age
            base_improvement = (match_rating - 6.0) / 2.0  # Base improvement from 0.5 to 2.0
            
            # Age-based modifiers
            if self.age <= 23:
                base_improvement *= 1.5  # 50% bonus for young players
            elif self.age >= 30:
                base_improvement *= 0.5  # 50% penalty for older players
            
            # Potential-based modifier
            rating_gap = max(0, self.true_potential - self.overall_rating)
            if rating_gap > 0:
                base_improvement *= (1 + (rating_gap / 20))  # Up to 50% bonus for players below potential
            
            # Store old rating before improvement
            old_rating = self.overall_rating
            
            # Call improve_attributes with match-based flag and calculated improvement
            self.improve_attributes(training_focus, is_match_improvement=True, improvement_amount=base_improvement)
            
            # If this is the first improvement of the season, set the season start rating
            if self.season_start_rating is None:
                self.season_start_rating = old_rating

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
            
            # Add match rating information
            if self.match_ratings:
                last_5_avg = self.get_average_rating("last5")
                season_avg = self.get_average_rating("season")
                career_avg = self.get_average_rating("career")
                
                # Color code the form rating
                if last_5_avg >= 7.5:
                    form_color = Fore.GREEN
                elif last_5_avg >= 6.5:
                    form_color = Fore.YELLOW
                else:
                    form_color = Fore.RED
                    
                stats_display.extend([
                    f"Current Form (Last 5): {form_color}{last_5_avg:.1f}{Style.RESET_ALL}",
                    f"Season Average: {season_avg:.1f}",
                    f"Career Average: {career_avg:.1f}"
                ])
                
                # Show rating trend
                if len(self.match_ratings) >= 3:
                    last_3 = self.match_ratings[-3:]
                    if all(a > b for a, b in zip(last_3[1:], last_3[:-1])):
                        stats_display.append(f"{Fore.GREEN}Rating Trend: ↑ Improving{Style.RESET_ALL}")
                    elif all(a < b for a, b in zip(last_3[1:], last_3[:-1])):
                        stats_display.append(f"{Fore.RED}Rating Trend: ↓ Declining{Style.RESET_ALL}")
                    else:
                        stats_display.append(f"{Fore.YELLOW}Rating Trend: → Inconsistent{Style.RESET_ALL}")
            
            if self.position == Position.GK:
                stats_display.extend([
                    f"Clean Sheets: {stats.get('clean_sheets', 0)}",
                    f"Saves: {stats.get('saves', 0)}"
                ])
            else:
                stats_display.extend([
                    f"Goals: {stats.get('goals', 0)}",
                    f"Assists: {stats.get('assists', 0)}",
                    f"Shots: {stats.get('shots', 0)} ({stats.get('shots_on_target', 0)} on target)",
                    f"Pass Accuracy: {stats.get('passes_completed', 0)}/{stats.get('passes_attempted', 0)} " +
                    f"({(stats.get('passes_completed', 0)/max(1, stats.get('passes_attempted', 0))*100):.1f}%)",
                    f"Tackles Won: {stats.get('tackles_won', 0)}/{stats.get('tackles_attempted', 0)} " +
                    f"({(stats.get('tackles_won', 0)/max(1, stats.get('tackles_attempted', 0))*100):.1f}%)"
                ])
        
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

    def update_match_rating(self, action_type, success):
        """Updates the player's match rating based on their actions"""
        # Base impact values for different actions
        rating_impacts = {
            "goal": 1.0,
            "assist": 0.8,
            "shot_on_target": 0.3,
            "shot_off_target": -0.1,
            "successful_pass": 0.1,
            "failed_pass": -0.1,
            "successful_tackle": 0.3,
            "failed_tackle": -0.2,
            "save": 0.4,  # For goalkeepers
            "conceded": -0.3,  # For goalkeepers
            "clean_sheet_minute": 0.01  # Small bonus for each minute of clean sheet (GK and defenders)
        }
        
        # Get the impact value
        impact = rating_impacts.get(action_type, 0)
        if not success:
            impact = -abs(impact)  # Negative impact for failed actions
            
        # Update current match rating
        self.current_match_rating = max(1.0, min(10.0, self.current_match_rating + impact))

    def finalize_match_rating(self):
        """Finalizes the match rating and adds it to history"""
        # Round to one decimal place
        final_rating = round(self.current_match_rating, 1)
        
        # Add to match ratings history
        self.match_ratings.append(final_rating)
        self.season_ratings.append(final_rating)
        self.career_ratings.append(final_rating)
        
        # Reset current match rating for next match
        self.current_match_rating = 6.0
        
        return final_rating

    def get_average_rating(self, period="season"):
        """Returns the player's average rating for the specified period"""
        if period == "season" and self.season_ratings:
            return sum(self.season_ratings) / len(self.season_ratings)
        elif period == "career" and self.career_ratings:
            return sum(self.career_ratings) / len(self.career_ratings)
        elif period == "last5" and self.match_ratings:
            last_5 = self.match_ratings[-5:] if len(self.match_ratings) >= 5 else self.match_ratings
            return sum(last_5) / len(last_5)
        return 6.0  # Default rating if no matches played

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
            
            # Add average rating based on the stat type
            if stat_type == "season":
                stats_str.append(f"Average Rating: {self.get_average_rating('season'):.1f}")
            elif stat_type == "career":
                stats_str.append(f"Average Rating: {self.get_average_rating('career'):.1f}")
            elif stat_type == "match" and self.match_ratings:
                stats_str.append(f"Match Rating: {self.match_ratings[-1]:.1f}")

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

    def check_retirement(self):
        """
        Checks if a player should retire based on age, performance, and other factors.
        Returns (should_retire, reason) tuple.
        """
        if self.youth or self.retired:
            return False, None

        # Base retirement chance increases with age
        if self.age < 32:
            return False, None
        elif self.age < 35:
            base_chance = (self.age - 31) * 0.05  # 5% per year over 31
        elif self.age < 38:
            base_chance = 0.20 + (self.age - 34) * 0.10  # 20% base + 10% per year over 34
        else:
            base_chance = 0.50 + (self.age - 37) * 0.15  # 50% base + 15% per year over 37

        # Performance factors
        if self.season_ratings:
            avg_rating = self.get_average_rating("season")
            if avg_rating < 6.0:
                base_chance += 0.2  # Poor performance increases retirement chance
            elif avg_rating < 6.5:
                base_chance += 0.1
            elif avg_rating > 7.5:
                base_chance -= 0.1  # Good performance decreases retirement chance

        # Playing time factor
        if self.season_stats["matches_played"] > 0:
            matches_played_ratio = self.season_stats["matches_played"] / max(1, self.season_stats["matches_played"] + 5)
            if matches_played_ratio < 0.3:  # Less than 30% of matches played
                base_chance += 0.15
            elif matches_played_ratio < 0.5:  # Less than 50% of matches played
                base_chance += 0.08

        # Position-specific factors
        if self.position in [Position.ST, Position.LW, Position.RW]:
            base_chance += 0.05  # Attackers tend to retire slightly earlier
        elif self.position == Position.GK:
            base_chance -= 0.08  # Goalkeepers tend to play longer

        # Rating decline factor
        if self.age >= 33:
            last_5_ratings = self.match_ratings[-5:] if len(self.match_ratings) >= 5 else self.match_ratings
            if len(last_5_ratings) >= 3:
                if all(a < b for a, b in zip(last_5_ratings[1:], last_5_ratings[:-1])):
                    base_chance += 0.1  # Consistent decline increases retirement chance

        # Random factor to add unpredictability
        base_chance += random.uniform(-0.05, 0.05)

        # Cap the maximum chance
        retirement_chance = min(0.95, max(0, base_chance))

        # Check if player retires
        if random.random() < retirement_chance:
            reason = self._get_retirement_reason()
            self.retired = True
            return True, reason

        return False, None

    def _get_retirement_reason(self):
        """Returns a personalized retirement message based on player's career and attributes."""
        reasons = []
        
        # Age-based reasons
        if self.age >= 38:
            reasons.append(f"After a long and illustrious career spanning {self.age - 18} years")
        elif self.age >= 35:
            reasons.append(f"Having given {self.age - 18} years to professional football")
        else:
            reasons.append("After careful consideration of their future")

        # Performance-based reasons
        if self.season_ratings:
            avg_rating = self.get_average_rating("season")
            if avg_rating < 6.5:
                reasons.append("struggling to maintain peak performance")
            elif avg_rating > 7.5:
                reasons.append("choosing to end their career on a high note")

        # Playing time reasons
        if self.season_stats["matches_played"] > 0:
            matches_played_ratio = self.season_stats["matches_played"] / max(1, self.season_stats["matches_played"] + 5)
            if matches_played_ratio < 0.3:
                reasons.append("finding limited opportunities in the first team")

        # Career achievements
        career_goals = self.career_stats["goals"]
        career_assists = self.career_stats["assists"]
        career_clean_sheets = self.career_stats["clean_sheets"]
        
        achievements = []
        if self.position == Position.GK and career_clean_sheets > 0:
            achievements.append(f"{career_clean_sheets} clean sheets")
        if career_goals > 0:
            achievements.append(f"{career_goals} goals")
        if career_assists > 0:
            achievements.append(f"{career_assists} assists")

        if achievements:
            reasons.append(f"with a career record of {', '.join(achievements)}")

        # Combine reasons into a retirement message
        message = f"{self.name} has announced their retirement. {', '.join(reasons)}, "
        message += f"the {self.age}-year-old {self.position.value.lower()} has decided to hang up their boots."

        return message 

    def get_season_improvement(self):
        """Returns the player's improvement this season"""
        if self.season_start_rating is None:
            return 0.0
        return round(self.overall_rating - self.season_start_rating, 1)

    def get_improvement_display(self):
        """Returns a formatted string showing the player's improvement"""
        improvement = self.get_season_improvement()
        if improvement > 0:
            return f"{Fore.GREEN}+{improvement:.1f}{Style.RESET_ALL}"
        elif improvement < 0:
            return f"{Fore.RED}{improvement:.1f}{Style.RESET_ALL}"
        else:
            return f"{Fore.YELLOW}0.0{Style.RESET_ALL}"

    def end_season(self):
        """Handles end of season tasks"""
        # Store the current rating as the start rating for next season
        self.season_start_rating = self.overall_rating
        
        # Reset season statistics
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
        self.season_ratings = [] 