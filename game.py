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
            team = Team(name, tier)
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
            team = Team(name, tier)
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
            team = Team(name, tier)
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
                                         is_youth_team=True)
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
        print("10. Save Game")
        print("11. Exit")
        
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
            print("Save functionality not implemented yet")
            input("Press Enter to continue...")
        elif choice == "11":
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
                    print(f"  {player}")
                    
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
                    print(f"  {player}")
                    
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
        opponent_youth = Team(f"{opponent_team.name} Youth", self.current_league.tier, is_youth_team=True)
        
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
            print("No more fixtures scheduled!")
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
        
        # Silently simulate youth match in background
        opponent_team = random.choice([t for t in self.current_league.teams if t != self.current_team])
        opponent_youth = Team(f"{opponent_team.name} Youth", self.current_league.tier, is_youth_team=True)
        
        # Get starting eleven before match simulation
        youth_starters = self.youth_team.get_starting_eleven()
        
        # Simulate youth match without displaying any output
        youth_match = Match(self.youth_team, opponent_youth,
                          commentary_delay=0,  # No delay for background simulation
                          action_frequency=self.settings["match_action_frequency"],
                          silent=True)  # Enable silent mode
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
                        self.current_team.add_player(player)
                        print(f"\n{player.name} has been promoted to the first team!")
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

    def _exit_game(self):
        """Exits the game"""
        print("\nThanks for playing!")
        exit()

    @staticmethod
    def _clear_screen():
        """Clears the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    game = Game()
    game.start() 