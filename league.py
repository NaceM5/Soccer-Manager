from team import Team
import random
from itertools import combinations
from datetime import datetime, timedelta

class League:
    def __init__(self, name, tier):
        self.name = name
        self.tier = tier
        self.teams = []
        self.fixtures = []
        self.current_week = 0
        self.standings = {}
        
    def add_team(self, team):
        """Adds a team to the league"""
        self.teams.append(team)
        self.standings[team.name] = {
            "played": 0,
            "won": 0,
            "drawn": 0,
            "lost": 0,
            "goals_for": 0,
            "goals_against": 0,
            "points": 0
        }
        
    def generate_season_fixtures(self, start_date=None):
        """Generates a full season of fixtures"""
        if start_date is None:
            start_date = datetime.now()
            
        # Clear existing fixtures
        self.fixtures = []
            
        # Generate all possible combinations of teams
        matches = list(combinations(self.teams, 2))
        
        # Create home and away fixtures
        all_fixtures = []
        for home, away in matches:
            # Home game
            all_fixtures.append({
                "week": None,
                "date": None,
                "home": home,
                "away": away,
                "played": False,
                "score": None
            })
            # Away game (reverse fixture)
            all_fixtures.append({
                "week": None,
                "date": None,
                "home": away,
                "away": home,
                "played": False,
                "score": None
            })
            
        # Shuffle fixtures
        random.shuffle(all_fixtures)
        
        # Calculate total weeks needed (each team plays every other team twice)
        total_weeks = (len(self.teams) - 1) * 2  # Each team plays every other team twice
        
        # Assign weeks and dates
        current_date = start_date
        
        # Create a list to track which teams have played in each week
        weekly_teams = {week: set() for week in range(total_weeks)}
        
        # First pass: Try to distribute fixtures evenly
        for fixture in all_fixtures:
            assigned = False
            for week in range(total_weeks):
                if (fixture["home"] not in weekly_teams[week] and 
                    fixture["away"] not in weekly_teams[week]):
                    fixture["week"] = week + 1
                    fixture["date"] = current_date + timedelta(days=week*7)
                    weekly_teams[week].add(fixture["home"])
                    weekly_teams[week].add(fixture["away"])
                    assigned = True
                    break
            if assigned:
                self.fixtures.append(fixture)
        
        # Second pass: If any fixtures weren't assigned, try to fit them in
        remaining_fixtures = [f for f in all_fixtures if f not in self.fixtures]
        for fixture in remaining_fixtures:
            for week in range(total_weeks):
                if (fixture["home"] not in weekly_teams[week] or 
                    fixture["away"] not in weekly_teams[week]):
                    fixture["week"] = week + 1
                    fixture["date"] = current_date + timedelta(days=week*7)
                    weekly_teams[week].add(fixture["home"])
                    weekly_teams[week].add(fixture["away"])
                    self.fixtures.append(fixture)
                    break
        
        # Sort fixtures by week
        self.fixtures.sort(key=lambda x: x["week"])
        
        # Verify fixture distribution
        for team in self.teams:
            team_fixtures = self.get_team_fixtures(team)
            expected_fixtures = (len(self.teams) - 1) * 2
            if len(team_fixtures) != expected_fixtures:
                print(f"Warning: {team.name} has {len(team_fixtures)} fixtures, expected {expected_fixtures}")
                print(f"Weeks played: {[f['week'] for f in team_fixtures]}")
        
    def get_week_fixtures(self, week):
        """Returns fixtures for a specific week"""
        return [f for f in self.fixtures if f["week"] == week]
        
    def get_team_fixtures(self, team):
        """Returns all fixtures for a specific team"""
        return [f for f in self.fixtures if f["home"] == team or f["away"] == team]
        
    def update_standings(self, home_team, away_team, home_score, away_score):
        """Updates league standings after a match"""
        # Update home team
        self.standings[home_team.name]["played"] += 1
        self.standings[home_team.name]["goals_for"] += home_score
        self.standings[home_team.name]["goals_against"] += away_score
        
        # Update away team
        self.standings[away_team.name]["played"] += 1
        self.standings[away_team.name]["goals_for"] += away_score
        self.standings[away_team.name]["goals_against"] += home_score
        
        if home_score > away_score:
            self.standings[home_team.name]["won"] += 1
            self.standings[home_team.name]["points"] += 3
            self.standings[away_team.name]["lost"] += 1
        elif away_score > home_score:
            self.standings[away_team.name]["won"] += 1
            self.standings[away_team.name]["points"] += 3
            self.standings[home_team.name]["lost"] += 1
        else:
            self.standings[home_team.name]["drawn"] += 1
            self.standings[home_team.name]["points"] += 1
            self.standings[away_team.name]["drawn"] += 1
            self.standings[away_team.name]["points"] += 1
            
    def get_standings(self):
        """Returns current league standings sorted by points"""
        standings_list = []
        for team_name, stats in self.standings.items():
            team_stats = stats.copy()
            team_stats["team"] = team_name
            team_stats["goal_difference"] = team_stats["goals_for"] - team_stats["goals_against"]
            standings_list.append(team_stats)
            
        # Sort by points, then goal difference, then goals scored
        return sorted(
            standings_list,
            key=lambda x: (x["points"], x["goal_difference"], x["goals_for"]),
            reverse=True
        )
        
    def print_standings(self):
        """Prints current league standings"""
        standings = self.get_standings()
        
        print(f"\n{self.name} Standings:")
        print("Pos  Team                 P    W    D    L    GF   GA   GD   Pts")
        print("-" * 65)
        
        for pos, team in enumerate(standings, 1):
            print(f"{pos:2}   {team['team']:<18} {team['played']:2}   "
                  f"{team['won']:2}   {team['drawn']:2}   {team['lost']:2}   "
                  f"{team['goals_for']:2}   {team['goals_against']:2}   "
                  f"{team['goal_difference']:3}   {team['points']:2}")
            
    def simulate_week(self, week):
        """Simulates all matches for a given week"""
        fixtures = self.get_week_fixtures(week)
        results = []
        
        for fixture in fixtures:
            if not fixture["played"]:
                # Simulate match
                from match import Match
                match = Match(fixture["home"], fixture["away"])
                match.simulate()
                
                # Record result
                fixture["played"] = True
                fixture["score"] = (match.home_score, match.away_score)
                
                # Update standings
                self.update_standings(
                    fixture["home"],
                    fixture["away"],
                    match.home_score,
                    match.away_score
                )
                
                results.append({
                    "home": fixture["home"].name,
                    "away": fixture["away"].name,
                    "score": fixture["score"]
                })
                
        return results
        
    def get_next_fixture(self, team):
        """Returns the next unplayed fixture for a team"""
        team_fixtures = self.get_team_fixtures(team)
        unplayed = [f for f in team_fixtures if not f["played"]]
        
        # If there are no unplayed fixtures, check if all fixtures in the league are played
        if not unplayed:
            all_fixtures_played = all(f["played"] for f in self.fixtures)
            if all_fixtures_played:
                return None  # Season is complete
            else:
                # If some fixtures are not marked as played but we have no more team fixtures,
                # something might be wrong with the fixture generation
                print("Warning: No more fixtures for team but season is not complete!")
                return None
                
        # Return the fixture with the lowest week number
        return min(unplayed, key=lambda x: x["week"]) 