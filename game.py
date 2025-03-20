from player import Player, Position, Personality
from team import Team
from league import League
from match import Match
import os
import time
from colorama import init, Fore, Style
import random

# Initialize colorama
init()

class Game:
    def __init__(self):
        self.leagues = self._initialize_leagues()
        self.current_team = None
        self.current_league = None
        self.youth_team = None  # Will be initialized when team is selected
        self.youth_match_available = False  # New flag to track youth match availability
        
        # Game settings
        self.settings = {
            "match_action_frequency": 5,  # How often (in minutes) match actions occur
            "commentary_delay": 2,  # Delay between commentary lines
        }

    def _initialize_leagues(self):
        """Initializes all leagues with their teams"""
        leagues = {}
        
        # English League
        english = League("English League", 1)
        english_teams = [
            ("London FC", 1), ("FC Liverpool", 1), ("Nottingham FC", 1),
            ("FC Newcastle", 1), ("Manchester FC", 1), ("FC Leicester", 1),
            ("Southhampton FC", 1), ("Coventry FC", 1), ("FC Sheffield", 1)
        ]
        for name, tier in english_teams:
            team = Team(name, tier, game=self)
            english.add_team(team)
        leagues[english.name] = english

        # Spanish League
        spanish = League("Spanish League", 2)
        spanish_teams = [
            ("Madrid FC", 2), ("FC Barcelona", 2), ("Granada FC", 2),
            ("Seville FC", 2), ("Valencia FC", 2), ("Bilbao FC", 2),
            ("FC Palma", 2), ("FC Girona", 2), ("FC Vigo", 2)
        ]
        for name, tier in spanish_teams:
            team = Team(name, tier, game=self)
            spanish.add_team(team)
        leagues[spanish.name] = spanish

        # German League
        german = League("German League", 3)
        german_teams = [
            ("FC Munich", 3), ("FC Leipzig", 3), ("Dortmund FC", 3),
            ("Frankfurt FC", 3), ("Berlin FC", 3), ("FC Dresden", 3),
            ("FC Biefeld", 3), ("Hamburg FC", 3), ("Potsdam FC", 3)
        ]
        for name, tier in german_teams:
            team = Team(name, tier, game=self)
            german.add_team(team)
        leagues[german.name] = german

        # Generate fixtures for all leagues
        for league in leagues.values():
            league.generate_season_fixtures()

        return leagues

    def start(self):
        """Starts the game"""
        self._clear_screen()
        print(f"{Fore.CYAN}Welcome to Soccer Manager!{Style.RESET_ALL}")
        self._select_league_and_team()
        
        while True:
            self._show_main_menu()

    def _select_league_and_team(self):
        """Allows player to select a league and team"""
        print("\nAvailable Leagues:")
        for i, league in enumerate(self.leagues.values(), 1):
            print(f"{i}. {league.name}")

        while True:
            try:
                choice = int(input("\nSelect a league (number): ")) - 1
                if 0 <= choice < len(self.leagues):
                    league_name = list(self.leagues.keys())[choice]
                    self.current_league = self.leagues[league_name]
                    break
            except ValueError:
                print("Please enter a valid number")

        print(f"\nTeams in {self.current_league.name}:")
        for i, team in enumerate(self.current_league.teams, 1):
            print(f"{i}. {team.name} (Rating: {team.get_squad_rating():.1f})")

        while True:
            try:
                choice = int(input("\nSelect your team (number): ")) - 1
                if 0 <= choice < len(self.current_league.teams):
                    self.current_team = self.current_league.teams[choice]
                    # Initialize youth team when main team is selected
                    self.youth_team = Team(f"{self.current_team.name} Youth", 
                                         self.current_league.tier, 
                                         is_youth_team=True,
                                         game=self)
                    break
            except ValueError:
                print("Please enter a valid number")

    def _show_main_menu(self):
        """Shows the main menu"""
        self._clear_screen()
        print(f"{Fore.CYAN}Main Menu - {self.current_team.name}{Style.RESET_ALL}")
        print("\n1. View Squad")
        print("2. View Youth Academy")
        print("3. View League Table")
        print("4. Play Next Match")
        print("5. Simulate Week")
        print("6. Transfer Market")
        print("7. Youth Management")
        print("8. View Player Statistics")
        print("9. Options")
        print("10. Watch Random Youth Game")
        print("11. Save Game")
        print("12. Exit")
        
        choice = input("\nEnter your choice: ")
        self._handle_menu_choice(choice)

    def _handle_menu_choice(self, choice):
        """Handles menu selection"""
        if choice == "1":
            self._view_squad()
        elif choice == "2":
            self._view_youth_academy()
        elif choice == "3":
            self._view_league_table()
        elif choice == "4":
            self._play_next_match()
        elif choice == "5":
            self._simulate_week()
        elif choice == "6":
            self._transfer_market()
        elif choice == "7":
            self._youth_management()
        elif choice == "8":
            self._view_player_statistics()
        elif choice == "9":
            self._show_options_menu()
        elif choice == "10":
            self._watch_random_youth_game()
        elif choice == "11":
            print("Save functionality not implemented yet")
            input("Press Enter to continue...")
        elif choice == "12":
            self._exit_game()

    def _view_squad(self):
        """Shows the current team's squad"""
        self._clear_screen()
        print(f"{Fore.CYAN}Squad List for {self.current_team.name}{Style.RESET_ALL}")
        print("\nFirst Team:")
        
        # Group players by position
        positions = [Position.GK, Position.CB, Position.WB, Position.CDM,
                    Position.CM, Position.CAM, Position.LW, Position.RW, Position.ST]
                    
        for position in positions:
            players = self.current_team.get_players_by_position(position)
            if players:
                print(f"\n{position.abbreviation}s:")
                for player in sorted(players, key=lambda x: x.overall_rating, reverse=True):
                    # Get form rating
                    form = player.get_average_rating("last5")
                    season_avg = player.get_average_rating("season")
                    
                    # Color code form rating
                    if form >= 7.5:
                        form_color = Fore.GREEN
                    elif form >= 6.5:
                        form_color = Fore.YELLOW
                    else:
                        form_color = Fore.RED
                        
                    # Calculate season improvement
                    improvement = player.overall_rating - player.season_start_rating
                    if improvement > 0:
                        improvement_color = Fore.GREEN
                    elif improvement < 0:
                        improvement_color = Fore.RED
                    else:
                        improvement_color = Fore.YELLOW
                        
                    # Format ratings string
                    ratings_str = f"Overall: {player.overall_rating:.1f} (Start: {player.season_start_rating:.1f}, Change: {improvement_color}{improvement:+.1f}{Style.RESET_ALL})"
                    if player.match_ratings:  # Only show form if they've played matches
                        ratings_str += f" | Form: {form_color}{form:.1f}{Style.RESET_ALL}"
                        if player.season_ratings:  # Only show season average if they've played
                            ratings_str += f" | Season Avg: {season_avg:.1f}"
                    
                    print(f"  {player.name} ({player.age}) - {ratings_str}")
                    
        input("\nPress Enter to continue...")

    def _view_youth_academy(self):
        """Shows the youth academy squad and options"""
        while True:
            self._clear_screen()
            print(f"{Fore.CYAN}Youth Academy for {self.current_team.name}{Style.RESET_ALL}")
            
            print("\nOptions:")
            print("1. View Squad")
            print("2. Watch Youth Match")
            print("3. View Scouting Reports")
            print("4. Back to Main Menu")
            
            choice = input("\nEnter your choice: ")
            
            if choice == "1":
                self._view_youth_squad()
            elif choice == "2":
                self._play_youth_match()
            elif choice == "3":
                self._view_scouting_reports()
            elif choice == "4":
                break

    def _view_youth_squad(self):
        """Shows the youth academy squad"""
        self._clear_screen()
        print(f"{Fore.CYAN}Youth Squad for {self.current_team.name}{Style.RESET_ALL}")
        
        # Group players by position
        positions = [Position.GK, Position.CB, Position.WB, Position.CDM,
                    Position.CM, Position.CAM, Position.LW, Position.RW, Position.ST]
                    
        for position in positions:
            players = self.youth_team.get_players_by_position(position)
            if players:
                print(f"\n{position.abbreviation}s:")
                for player in sorted(players, key=lambda x: x.overall_rating, reverse=True):
                    # Get form rating
                    form = player.get_average_rating("last5")
                    season_avg = player.get_average_rating("season")
                    
                    # Color code form rating
                    if form >= 7.5:
                        form_color = Fore.GREEN
                    elif form >= 6.5:
                        form_color = Fore.YELLOW
                    else:
                        form_color = Fore.RED
                        
                    # Format ratings string
                    ratings_str = f"Overall: {player.overall_rating:.1f} (Season: {player.get_improvement_display()})"
                    if player.match_ratings:  # Only show form if they've played matches
                        ratings_str += f" | Form: {form_color}{form:.1f}{Style.RESET_ALL}"
                        if player.season_ratings:  # Only show season average if they've played
                            ratings_str += f" | Season Avg: {season_avg:.1f}"
                    
                    print(f"  {player.name} - {ratings_str}")
                    
        input("\nPress Enter to continue...")

    def _view_scouting_reports(self):
        """Shows scouting reports for youth players"""
        while True:
            self._clear_screen()
            print(f"{Fore.CYAN}Youth Squad Scouting Reports{Style.RESET_ALL}\n")
            
            # List all youth players
            players = self.youth_team.players
            for i, player in enumerate(players, 1):
                print(f"{i}. {player}")
            
            print("\n0. Back")
            
            try:
                choice = int(input("\nSelect a player to view scouting report (0 to go back): "))
                if choice == 0:
                    break
                if 1 <= choice <= len(players):
                    player = players[choice - 1]
                    print("\n" + player.get_latest_scouting_report())
                    input("\nPress Enter to continue...")
            except ValueError:
                continue

    def _play_youth_match(self):
        """Simulates a youth team match"""
        self._clear_screen()
        print(f"{Fore.CYAN}Youth Match{Style.RESET_ALL}")
        
        # Create an opponent youth team from a random league team
        opponent_team = random.choice([t for t in self.current_league.teams if t != self.current_team])
        opponent_youth = Team(f"{opponent_team.name} Youth", self.current_league.tier, is_youth_team=True, game=self)
        
        print(f"\nMatch: {self.youth_team.name} vs {opponent_youth.name}")
        input("Press Enter to start the match...")
        
        # Get starting eleven before match simulation
        youth_starters = self.youth_team.get_starting_eleven()
        
        # Use the same settings as regular matches
        match = Match(self.youth_team, opponent_youth,
                     commentary_delay=self.settings["commentary_delay"],
                     action_frequency=self.settings["match_action_frequency"])
        match.simulate()
        
        # Update scouting information for players who started
        for player in youth_starters:
            # Increment matches_scouted since this was a watched match
            player.matches_scouted += 1
            player.potential_uncertainty = max(5, 15 - (player.matches_scouted // 5))
            if player.matches_scouted % 5 == 0:  # New scouting report every 5 matches
                player._generate_scouting_report()
        
        input("\nPress Enter to continue...")

    def _view_league_table(self):
        """Shows the current league standings"""
        self._clear_screen()
        self.current_league.print_standings()
        input("\nPress Enter to continue...")

    def _play_next_match(self):
        """Plays the next scheduled match"""
        next_fixture = self.current_league.get_next_fixture(self.current_team)
        
        if not next_fixture:
            # Check if all fixtures in the league are played
            all_fixtures_played = all(f["played"] for f in self.current_league.fixtures)
            if all_fixtures_played:
                print("\nSeason completed! Starting new season...")
                input("Press Enter to continue...")
                self.end_season()
                input("Press Enter to continue...")  # After end_season summary
                
                # Get the next fixture after starting new season
                next_fixture = self.current_league.get_next_fixture(self.current_team)
                if not next_fixture:
                    print("Error: No fixtures generated for new season!")
                    input("Press Enter to continue...")
                    return
            else:
                print("\nNo more fixtures scheduled for your team!")
                print("Auto-simulating remaining league matches...")
                
                # Find all unplayed fixtures
                unplayed_fixtures = [f for f in self.current_league.fixtures if not f["played"]]
                
                # Sort fixtures by week to simulate them in order
                unplayed_fixtures.sort(key=lambda x: x["week"])
                
                # Simulate each remaining fixture
                for fixture in unplayed_fixtures:
                    print(f"\nSimulating: {fixture['home'].name} vs {fixture['away'].name}")
                    match = Match(fixture['home'], fixture['away'],
                                commentary_delay=0,  # No delay for auto-simulation
                                action_frequency=self.settings["match_action_frequency"])
                    match.simulate()
                    
                    # Record result
                    fixture['played'] = True
                    fixture['score'] = (match.home_score, match.away_score)
                    
                    # Update standings
                    self.current_league.update_standings(
                        fixture['home'],
                        fixture['away'],
                        match.home_score,
                        match.away_score
                    )
                    
                    print(f"Result: {fixture['home'].name} {match.home_score} - {match.away_score} {fixture['away'].name}")
                
                print("\nAll remaining matches have been simulated!")
                print("Starting new season...")
                input("Press Enter to continue...")
                self.end_season()
                input("Press Enter to continue...")  # After end_season summary
                
                # Get the next fixture after starting new season
                next_fixture = self.current_league.get_next_fixture(self.current_team)
                if not next_fixture:
                    print("Error: No fixtures generated for new season!")
                    input("Press Enter to continue...")
                    return
            
        print(f"\nNext Match: {next_fixture['home'].name} vs {next_fixture['away'].name}")
        input("Press Enter to start the match...")
        
        # First simulate all other matches for this week
        self._simulate_other_matches(next_fixture["week"])
        
        # Then play our match
        match = Match(next_fixture['home'], next_fixture['away'], 
                     commentary_delay=self.settings["commentary_delay"],
                     action_frequency=self.settings["match_action_frequency"])
        match.simulate()
        
        # Update fixture status and record result
        next_fixture['played'] = True
        next_fixture['score'] = (match.home_score, match.away_score)
        
        # Update league standings
        self.current_league.update_standings(
            next_fixture['home'],
            next_fixture['away'],
            match.home_score,
            match.away_score
        )
        
        # Set youth match as available after playing a regular match
        self.youth_match_available = True
        
        # Silently simulate youth match in background
        opponent_team = random.choice([t for t in self.current_league.teams if t != self.current_team])
        opponent_youth = Team(f"{opponent_team.name} Youth", self.current_league.tier, is_youth_team=True, game=self)
        
        # Get starting eleven before match simulation
        youth_starters = self.youth_team.get_starting_eleven()
        
        # Simulate youth match without displaying any output
        youth_match = Match(self.youth_team, opponent_youth,
                          commentary_delay=0,  # No delay for background simulation
                          action_frequency=self.settings["match_action_frequency"],
                          silent=True)
        youth_match.simulate()
        
        input("\nPress Enter to continue...")

    def _simulate_other_matches(self, week):
        """Simulates all other matches for the given week"""
        fixtures = self.current_league.get_week_fixtures(week)
        other_fixtures = [f for f in fixtures if f['home'] != self.current_team and f['away'] != self.current_team and not f['played']]
        
        if other_fixtures:
            print(f"\nSimulating other Week {week} matches...")
            for fixture in other_fixtures:
                match = Match(fixture['home'], fixture['away'], 
                            commentary_delay=0,  # No delay for other matches
                            action_frequency=self.settings["match_action_frequency"])
                match.simulate()
                
                fixture['played'] = True
                fixture['score'] = (match.home_score, match.away_score)
                self.current_league.update_standings(
                    fixture['home'],
                    fixture['away'],
                    match.home_score,
                    match.away_score
                )
                print(f"{fixture['home'].name} {match.home_score} - {match.away_score} {fixture['away'].name}")

    def _simulate_week(self):
        """Simulates all matches for the current week"""
        current_week = self.current_league.current_week + 1
        results = self.current_league.simulate_week(current_week)
        
        if results:
            print(f"\nWeek {current_week} Results:")
            for result in results:
                print(f"{result['home']} {result['score'][0]} - {result['score'][1]} {result['away']}")
            self.current_league.current_week = current_week
        else:
            print("\nNo matches to simulate!")
            
        input("\nPress Enter to continue...")

    def _transfer_market(self):
        """Shows transfer market options"""
        self._clear_screen()
        print(f"{Fore.CYAN}Transfer Market{Style.RESET_ALL}")
        print("Transfer market functionality not implemented yet")
        input("\nPress Enter to continue...")

    def _youth_management(self):
        """Shows youth management options"""
        self._clear_screen()
        print(f"{Fore.CYAN}Youth Academy Management{Style.RESET_ALL}")
        
        # First check for players who might leave
        at_risk_players = []
        for player in self.youth_team.players:
            will_leave, reason = player.might_leave_youth_team()
            if will_leave:
                at_risk_players.append((player, reason))
        
        if at_risk_players:
            print(f"\n{Fore.RED}Warning: Players at Risk of Leaving{Style.RESET_ALL}")
            for player, reason in at_risk_players:
                print(f"- {player.name} ({reason})")
            print("\nConsider promoting these players or they may leave for other teams!")
        
        # Show promotion prospects
        prospects = self.youth_team.get_youth_prospects()
        
        if prospects:
            print("\nPlayers ready for promotion:")
            for i, player in enumerate(prospects, 1):
                print(f"{i}. {player}")
                
            try:
                choice = int(input("\nSelect a player to promote (0 to cancel): ")) - 1
                if 0 <= choice < len(prospects):
                    player = prospects[choice]
                    if self.youth_team.promote_youth_player(player):
                        # Add player to senior team
                        self.current_team.add_player(player)
                        print(f"\n{Fore.GREEN}{player.name} has been promoted to the first team!{Style.RESET_ALL}")
                        
                        # Determine number of new youth players (chance for multiple)
                        rand_val = random.random()
                        num_new_players = 1
                        if rand_val < 0.15:  # 15% chance for 3 players
                            num_new_players = 3
                        elif rand_val < 0.35:  # 20% chance for 2 players
                            num_new_players = 2
                        
                        # Generate new youth players
                        for _ in range(num_new_players):
                            new_player = Player(player.position, youth=True, league_tier=self.current_league.tier)
                            self.youth_team.add_player(new_player)
                            if num_new_players == 1:
                                print(f"{Fore.CYAN}A new youth player, {new_player.name}, has joined the academy as a {new_player.position.value}!{Style.RESET_ALL}")
                            else:
                                print(f"{Fore.CYAN}Youth player {new_player.name} has joined the academy as a {new_player.position.value}!{Style.RESET_ALL}")
                        
                        if num_new_players > 1:
                            print(f"\n{Fore.YELLOW}Your scouts have found {num_new_players} promising young players!{Style.RESET_ALL}")
            except ValueError:
                pass
        else:
            print("\nNo players ready for promotion")
            
        input("\nPress Enter to continue...")

    def _view_player_statistics(self):
        """Shows detailed statistics for players"""
        while True:
            self._clear_screen()
            print(f"{Fore.CYAN}Player Statistics - {self.current_team.name}{Style.RESET_ALL}")
            
            # List all players
            players = self.current_team.players
            for i, player in enumerate(players, 1):
                print(f"{i}. {player.name} - {player.position.abbreviation}")
            
            print("\n0. Back to Main Menu")
            
            try:
                choice = int(input("\nSelect a player (number): "))
                if choice == 0:
                    break
                elif 1 <= choice <= len(players):
                    self._show_player_stats(players[choice - 1])
            except ValueError:
                print("Please enter a valid number")
                input("Press Enter to continue...")

    def _show_player_stats(self, player):
        """Shows detailed statistics for a specific player"""
        while True:
            self._clear_screen()
            print(f"{Fore.CYAN}Statistics for {player.name}{Style.RESET_ALL}")
            print(f"Position: {player.position.abbreviation}")
            print(f"Age: {player.age}")
            print(f"Overall Rating: {player.overall_rating:.1f}")
            print(f"Personality: {player.personality.value}")
            
            print("\nView Statistics:")
            print("1. Last Match")
            print("2. Season")
            print("3. Career")
            print("4. Back to Player List")
            
            choice = input("\nEnter your choice: ")
            
            if choice == "1":
                print(f"\n{Fore.YELLOW}Last Match Statistics:{Style.RESET_ALL}")
                print(player.get_stats_display("match"))
            elif choice == "2":
                print(f"\n{Fore.YELLOW}Season Statistics:{Style.RESET_ALL}")
                print(player.get_stats_display("season"))
            elif choice == "3":
                print(f"\n{Fore.YELLOW}Career Statistics:{Style.RESET_ALL}")
                print(player.get_stats_display("career"))
            elif choice == "4":
                break
                
            input("\nPress Enter to continue...")

    def _show_options_menu(self):
        """Shows the options menu"""
        while True:
            self._clear_screen()
            print(f"{Fore.CYAN}Options Menu{Style.RESET_ALL}\n")
            print("Current Settings:")
            print(f"1. Match Action Frequency: Every {self.settings['match_action_frequency']} minute(s)")
            print(f"2. Commentary Delay: {self.settings['commentary_delay']} second(s)")
            print("\n0. Back to Main Menu")
            
            choice = input("\nEnter your choice (or 0 to return): ")
            
            if choice == "0":
                break
            elif choice == "1":
                self._set_match_frequency()
            elif choice == "2":
                self._set_commentary_delay()

    def _set_match_frequency(self):
        """Sets how often match actions occur"""
        while True:
            try:
                frequency = int(input("\nEnter how often match actions should occur (1-5 minutes): "))
                if 1 <= frequency <= 5:
                    self.settings["match_action_frequency"] = frequency
                    print(f"\nMatch action frequency set to every {frequency} minute(s)")
                    input("Press Enter to continue...")
                    break
                else:
                    print("Please enter a number between 1 and 5")
            except ValueError:
                print("Please enter a valid number")

    def _set_commentary_delay(self):
        """Sets the delay between commentary lines"""
        while True:
            try:
                delay = float(input("\nEnter commentary delay in seconds (0-5): "))
                if 0 <= delay <= 5:
                    self.settings["commentary_delay"] = delay
                    print(f"\nCommentary delay set to {delay} seconds")
                    input("Press Enter to continue...")
                    break
                else:
                    print("Please enter a number between 0 and 5")
            except ValueError:
                print("Please enter a valid number")

    def _watch_random_youth_game(self):
        """Allows player to watch a random youth game and potentially sign players"""
        self._clear_screen()
        print(f"{Fore.CYAN}Watch Random Youth Game{Style.RESET_ALL}")
        
        if not self.youth_match_available:
            print(f"\n{Fore.RED}No youth match available! Play a regular match first.{Style.RESET_ALL}")
            input("\nPress Enter to continue...")
            return
            
        # Select two random teams (excluding user's team) to create youth teams for
        available_teams = [t for t in self.current_league.teams if t != self.current_team]
        if len(available_teams) < 2:
            print("Not enough teams available for a youth match!")
            input("Press Enter to continue...")
            return
            
        team1, team2 = random.sample(available_teams, 2)
        youth_team1 = Team(f"{team1.name} Youth", self.current_league.tier, is_youth_team=True, game=self)
        youth_team2 = Team(f"{team2.name} Youth", self.current_league.tier, is_youth_team=True, game=self)
        
        # Determine which teams (if any) are willing to let players go (65% chance each)
        team1_willing = random.random() < 0.65
        team2_willing = random.random() < 0.65
        
        print(f"\nMatch: {youth_team1.name} vs {youth_team2.name}")
        input("Press Enter to start the match...")
        
        # Get starting elevens before match simulation
        team1_starters = youth_team1.get_starting_eleven()
        team2_starters = youth_team2.get_starting_eleven()
        all_starters = team1_starters + team2_starters
        
        # Initialize scouting attributes for players if they don't exist
        for player in all_starters:
            if not hasattr(player, 'matches_scouted'):
                player.matches_scouted = 0
            if not hasattr(player, 'potential_uncertainty'):
                player.potential_uncertainty = 15
            if not hasattr(player, 'scouting_reports'):
                player.scouting_reports = []
        
        # Simulate the match
        match = Match(youth_team1, youth_team2,
                     commentary_delay=self.settings["commentary_delay"],
                     action_frequency=self.settings["match_action_frequency"])
        match.simulate()
        
        # After match, update scouting information for all players who played
        for player in all_starters:
            # Increment matches_scouted since this was a watched match
            player.matches_scouted += 1
            # Update potential uncertainty (gets more accurate with more scouting)
            player.potential_uncertainty = max(5, 15 - (player.matches_scouted // 5))
            # Always generate a new scouting report after watching a match
            player._generate_scouting_report()
        
        # Store the actual match teams and their players
        match_teams = {
            'team1': {
                'team': youth_team1,
                'players': team1_starters,
                'willing': team1_willing,
                'score': match.home_score
            },
            'team2': {
                'team': youth_team2,
                'players': team2_starters,
                'willing': team2_willing,
                'score': match.away_score
            }
        }
        
        # After match, show player performances and allow scouting
        self._clear_screen()
        print(f"\n{Fore.CYAN}Match Complete: {youth_team1.name} {match.home_score} - {match.away_score} {youth_team2.name}{Style.RESET_ALL}")
        
        # Display team willingness status
        if team1_willing:
            print(f"\n{Fore.GREEN}{youth_team1.name} might be open to letting some players leave.{Style.RESET_ALL}")
        if team2_willing:
            print(f"\n{Fore.GREEN}{youth_team2.name} might be open to letting some players leave.{Style.RESET_ALL}")
        if not team1_willing and not team2_willing:
            print(f"\n{Fore.RED}Neither team is interested in letting any players leave at this time.{Style.RESET_ALL}")
        
        player_signed = False  # Track if a player has been signed this match
        
        while True:
            print("\nOptions:")
            print("1. View Team 1 Players")
            print("2. View Team 2 Players")
            if (team1_willing or team2_willing) and not player_signed:
                print("3. Attempt to Sign Player")
            print("4. Return to Main Menu")
            
            choice = input("\nEnter your choice: ")
            
            if choice == "1":
                self._view_youth_game_team(match_teams['team1']['team'], 
                                         match_teams['team1']['players'],
                                         match_teams['team1']['score'])
            elif choice == "2":
                self._view_youth_game_team(match_teams['team2']['team'], 
                                         match_teams['team2']['players'],
                                         match_teams['team2']['score'])
            elif choice == "3" and (team1_willing or team2_willing) and not player_signed:
                # Create list of available players based on which teams are willing to sell
                available_to_sign = []
                if team1_willing:
                    available_to_sign.extend(match_teams['team1']['players'])
                if team2_willing:
                    available_to_sign.extend(match_teams['team2']['players'])
                if self._attempt_youth_signing(available_to_sign, 
                                             match_teams['team1']['team'] if team1_willing else match_teams['team2']['team']):
                    player_signed = True
            elif choice == "4":
                break
                
        # Reset youth match availability after watching
        self.youth_match_available = False

    def _view_youth_game_team(self, team, starters, score):
        """Shows the players from a team in the youth game"""
        self._clear_screen()
        print(f"{Fore.CYAN}Players from {team.name} (Goals Scored: {score}){Style.RESET_ALL}\n")
        
        for i, player in enumerate(starters, 1):
            # Create a display string that hides the overall rating for other teams
            name_and_pos = f"{player.name} ({player.position.abbreviation})"
            
            # Get match performance
            match_stats = []
            if player.stats["goals"] > 0:
                match_stats.append(f"Goals: {player.stats['goals']}")
            if player.stats["assists"] > 0:
                match_stats.append(f"Assists: {player.stats['assists']}")
            if player.position == Position.GK:
                if player.stats["saves"] > 0:
                    match_stats.append(f"Saves: {player.stats['saves']}")
                if player.stats["clean_sheets"] > 0:
                    match_stats.append("Clean Sheet")
            
            # Get the latest match rating
            if player.match_ratings:
                last_rating = player.match_ratings[-1]
                if last_rating >= 7.5:
                    rating_color = Fore.GREEN
                elif last_rating >= 6.5:
                    rating_color = Fore.YELLOW
                else:
                    rating_color = Fore.RED
                match_stats.append(f"Rating: {rating_color}{last_rating:.1f}{Style.RESET_ALL}")
            
            # Get the latest scouting report for potential range
            latest_report = player.get_latest_scouting_report()
            potential_range = "??"
            
            # Extract potential range from scouting report if it exists
            if latest_report:
                try:
                    # Split report into lines and find the potential range line
                    report_lines = latest_report.split('\n')
                    for line in report_lines:
                        if "Potential Range:" in line:
                            potential_range = line.split(": ")[1].strip()
                            break
                except (IndexError, AttributeError):
                    potential_range = "??"
            
            # Show ?? for overall rating only for other teams' players
            display_rating = "??" if team != self.youth_team else f"{player.overall_rating:.1f}"
            
            # Combine all information
            stats_display = " | ".join(match_stats) if match_stats else "No notable match actions"
            print(f"{i}. {name_and_pos} - Overall: {display_rating} - Potential: {potential_range}")
            print(f"   Match Performance: {stats_display}")
            print(f"   Scouted: {player.matches_scouted} times")
            print()  # Add blank line for readability
            
        while True:
            try:
                choice = int(input("\nSelect a player to view scouting report (0 to go back): "))
                if choice == 0:
                    break
                if 1 <= choice <= len(starters):
                    player = starters[choice - 1]
                    report = player.get_latest_scouting_report()
                    if report:
                        # Hide current ability/rating for players not on your team
                        if team != self.youth_team:
                            report_lines = report.split('\n')
                            filtered_lines = []
                            for line in report_lines:
                                if not any(x in line for x in ["Current Ability:", "Current Rating:"]):
                                    filtered_lines.append(line)
                            report = '\n'.join(filtered_lines)
                    print("\n" + report)
                    input("\nPress Enter to continue...")
                    break
            except ValueError:
                continue

    def _attempt_youth_signing(self, available_players, team):
        """Attempts to sign a youth player from the watched match"""
        self._clear_screen()
        print(f"{Fore.CYAN}Attempt to Sign Youth Player{Style.RESET_ALL}\n")
        
        # Show available players with hidden overalls for other teams
        for i, player in enumerate(available_players, 1):
            name_and_pos = f"{player.name} ({player.position.abbreviation})"
            
            # Get the latest scouting report for potential range
            latest_report = player.get_latest_scouting_report()
            potential_range = "??"
            
            # Extract potential range from scouting report if it exists
            if latest_report:
                try:
                    # Split report into lines and find the potential range line
                    report_lines = latest_report.split('\n')
                    for line in report_lines:
                        if "Potential Range:" in line:
                            potential_range = line.split(": ")[1].strip()
                            break
                except (IndexError, AttributeError):
                    potential_range = "??"
            
            # Always show ?? for overall rating in signing screen since these are other teams' players
            print(f"{i}. {name_and_pos} - Overall: ?? - Potential: {potential_range} (Scouted: {player.matches_scouted} times)")
            
        try:
            choice = int(input("\nSelect a player to attempt to sign (0 to cancel): "))
            if choice == 0:
                return False
                
            if 1 <= choice <= len(available_players):
                target_player = available_players[choice - 1]
                
                print(f"\n{Fore.GREEN}{team.name} is willing to negotiate a deal for {target_player.name}.{Style.RESET_ALL}")
                
                # Show your youth players in the same position
                your_players = [p for p in self.youth_team.players if p.position == target_player.position]
                
                if not your_players:
                    print(f"\n{Fore.RED}You don't have any youth players in position {target_player.position.value} to swap!{Style.RESET_ALL}")
                    input("\nPress Enter to continue...")
                    return False
                    
                print(f"\nSelect a player to swap for {target_player.name}:")
                for i, player in enumerate(your_players, 1):
                    print(f"{i}. {player}")  # Show full stats for your own players
                    
                try:
                    swap_choice = int(input("\nSelect a player to swap (0 to cancel): "))
                    if swap_choice == 0:
                        return False
                        
                    if 1 <= swap_choice <= len(your_players):
                        swap_player = your_players[swap_choice - 1]
                        
                        # Perform the swap
                        self.youth_team.remove_player(swap_player)
                        self.youth_team.add_player(target_player)
                        
                        print(f"\n{Fore.GREEN}Success! {target_player.name} has joined your youth academy!{Style.RESET_ALL}")
                        input("\nPress Enter to continue...")
                        return True
                except ValueError:
                    print("\nInvalid choice!")
                    input("Press Enter to continue...")
                    return False
        except ValueError:
            print("\nInvalid choice!")
            input("Press Enter to continue...")
            return False
            
        return False

    def _exit_game(self):
        """Exits the game"""
        print("\nThanks for playing!")
        exit()

    @staticmethod
    def _clear_screen():
        """Clears the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def end_season(self):
        """Handles end of season tasks"""
        print("\nEnd of Season Summary")
        print("--------------------")
        
        # Check for retirements
        retired_players = []
        for player in self.current_team.players:
            should_retire, reason = player.check_retirement()
            if should_retire:
                retired_players.append((player, reason))
        
        # Process retirements
        if retired_players:
            print("\nPlayer Retirements")
            print("-----------------")
            for player, reason in retired_players:
                print(f"\n{reason}")
                self.current_team.players.remove(player)
        
        # Reset season statistics and set season start rating
        for player in self.current_team.players:
            player.season_stats = {
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
            player.season_ratings = []
            player.season_start_rating = player.overall_rating  # Set season start rating to current overall rating
            
        # Generate replacement players for retired positions
        positions_needed = {}
        for player, _ in retired_players:
            pos = player.position
            positions_needed[pos] = positions_needed.get(pos, 0) + 1
        
        if positions_needed:
            print("\nNew Signings")
            print("------------")
            for position, count in positions_needed.items():
                for _ in range(count):
                    # Generate a replacement player aged 20-24
                    new_player = Player(position, age=random.randint(20, 24), league_tier=self.current_team.tier)
                    new_player.season_start_rating = new_player.overall_rating  # Set season start rating for new players
                    self.current_team.players.append(new_player)
                    print(f"Signed {new_player.name} ({new_player.age}) - {position.value}")
        
        # Age all players by 1 year
        for player in self.current_team.players:
            player.age += 1
        
        # Check youth players who might leave
        departed_youth = []
        for player in self.youth_team.players:
            should_leave, reason = player.might_leave_youth_team()
            if should_leave:
                departed_youth.append((player, reason))
        
        if departed_youth:
            print("\nYouth Academy Departures")
            print("----------------------")
            for player, reason in departed_youth:
                print(f"{player.name} has left the youth academy. ({reason})")
                self.youth_team.players.remove(player)
        
        # Generate new youth players to maintain squad size
        min_youth_players = 15
        while len(self.youth_team.players) < min_youth_players:
            # Randomly choose a position that needs filling
            position = random.choice(list(Position))
            new_player = Player(position, youth=True, league_tier=self.current_team.tier)
            new_player.season_start_rating = new_player.overall_rating  # Set season start rating for new youth players
            self.youth_team.players.append(new_player)
            print(f"New youth player joined the academy: {new_player.name} ({new_player.age}) - {position.value}")
        
        # Start new season
        print("\nStarting New Season...")
        self.current_league.current_week = 0  # Reset to week 0
        
        # Reset league standings for all teams
        for team in self.current_league.teams:
            self.current_league.standings[team.name] = {
                "played": 0,
                "won": 0,
                "drawn": 0,
                "lost": 0,
                "goals_for": 0,
                "goals_against": 0,
                "points": 0
            }
        
        # Generate new fixtures
        self.current_league.generate_season_fixtures()
        print("New season fixtures have been generated!")
        
        # Verify fixture count
        expected_fixtures = (len(self.current_league.teams) - 1) * 2  # Each team plays every other team twice
        actual_fixtures = len(self.current_league.get_team_fixtures(self.current_team))
        if actual_fixtures != expected_fixtures:
            print(f"\nWarning: Team has {actual_fixtures} fixtures, expected {expected_fixtures}")
        
        print("\nPress Enter to continue...")

if __name__ == "__main__":
    game = Game()
    game.start() 