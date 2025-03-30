import unittest
from nba_tools import (
    get_player_info,
    get_team_info,
    get_team_standings,
    get_league_leaders,
    get_game_odds,
    get_player_injuries,
    get_head_to_head_stats,
    set_use_mock_data,
    set_debug_mode,
    MOCK_PLAYERS,
    MOCK_TEAMS,
    MOCK_STANDINGS,
    MOCK_LEADERS,
    MOCK_GAMES,
    MOCK_ODDS,
    MOCK_INJURIES
)
import time
from datetime import datetime, timedelta

class TestResult(unittest.TestResult):
    def __init__(self, stream=None, descriptions=None, verbosity=None):
        super().__init__(stream, descriptions, verbosity)
        self.start_time = None
        self.end_time = None
        self.test_times = {}
        self.test_descriptions = {}
        self._summary_printed = False  # Flag to track if summary has been printed

    def startTest(self, test):
        self.start_time = time.time()
        super().startTest(test)

    def stopTest(self, test):
        self.end_time = time.time()
        test_time = self.end_time - self.start_time
        self.test_times[test.id()] = test_time
        self.test_descriptions[test.id()] = test.shortDescription() or test.id()
        super().stopTest(test)

    def printErrors(self):
        super().printErrors()
        if not self._summary_printed:
            self.printSummary()
            self._summary_printed = True

    def printSummary(self):
        if self._summary_printed:
            return
            
        print("\n" + "="*50)
        print("TEST SUMMARY")
        print("="*50)
        
        # Calculate statistics
        total_tests = self.testsRun
        successful_tests = total_tests - len(self.failures) - len(self.errors)
        failed_tests = len(self.failures)
        error_tests = len(self.errors)
        total_time = sum(self.test_times.values())
        avg_time = total_time / total_tests if total_tests > 0 else 0

        # Print statistics
        print(f"\nTotal Tests Run: {total_tests}")
        print(f"Successful Tests: {successful_tests}")
        print(f"Failed Tests: {failed_tests}")
        print(f"Error Tests: {error_tests}")
        if total_tests > 0:
            print(f"Success Rate: {(successful_tests/total_tests)*100:.2f}%")
        print(f"\nTotal Time: {total_time:.2f} seconds")
        print(f"Average Time per Test: {avg_time:.2f} seconds")

        # Print individual test times
        print("\nTest Execution Times:")
        for test_id, test_time in self.test_times.items():
            print(f"{self.test_descriptions[test_id]}: {test_time:.3f} seconds")

        # Print failures and errors if any
        if self.failures:
            print("\nFailures:")
            for failure in self.failures:
                print(f"- {failure[1]}")
        
        if self.errors:
            print("\nErrors:")
            for error in self.errors:
                print(f"- {error[1]}")

        print("\n" + "="*50)
        self._summary_printed = True

    def wasSuccessful(self):
        return super().wasSuccessful()

class TestNBATools(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        set_use_mock_data(True)  # Enable mock data for all tests
        set_debug_mode(False)    # Disable debug prints during tests

    def tearDown(self):
        """Clean up after each test."""
        set_use_mock_data(False)  # Disable mock data after each test
        set_debug_mode(False)     # Ensure debug mode is disabled

    def test_get_player_info_success(self):
        """Test successful player info retrieval."""
        # Test with exact name match
        result = get_player_info("Stephen", "Curry")
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["first_name"], "Stephen")
        self.assertEqual(result["last_name"], "Curry")
        self.assertEqual(result["position"], "G")

        # Test with case-insensitive match
        result = get_player_info("lebron", "james")
        self.assertEqual(result["id"], 2)
        self.assertEqual(result["first_name"], "LeBron")
        self.assertEqual(result["last_name"], "James")

    def test_get_player_info_not_found(self):
        """Test player info retrieval when player not found."""
        result = get_player_info("John", "Doe")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "No player found with name John Doe")

    def test_get_team_info_success(self):
        """Test successful team info retrieval."""
        # Test with full name
        result = get_team_info("Golden State Warriors")
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "Warriors")
        self.assertEqual(result["conference"], "West")

        # Test with short name
        result = get_team_info("Lakers")
        self.assertEqual(result["id"], 2)
        self.assertEqual(result["full_name"], "Los Angeles Lakers")

    def test_get_team_info_not_found(self):
        """Test team info retrieval when team not found."""
        result = get_team_info("NonExistent Team")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "No team found with name NonExistent Team")

    def test_get_team_standings_success(self):
        """Test successful standings retrieval."""
        result = get_team_standings(2023)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["team"]["id"], 1)  # Warriors
        self.assertEqual(result[0]["wins"], 45)
        self.assertEqual(result[1]["team"]["id"], 2)  # Lakers
        self.assertEqual(result[1]["wins"], 40)

    def test_get_league_leaders_success(self):
        """Test successful league leaders retrieval."""
        # Test points leaders
        result = get_league_leaders(2023, "pts")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["player"]["id"], 1)  # Curry
        self.assertEqual(result[0]["pts"], 28.5)
        self.assertEqual(result[1]["player"]["id"], 2)  # James
        self.assertEqual(result[1]["pts"], 25.3)

        # Test rebounds leaders
        result = get_league_leaders(2023, "reb")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["player"]["id"], 2)  # James
        self.assertEqual(result[0]["reb"], 8.2)

    def test_get_league_leaders_invalid_stat(self):
        """Test league leaders retrieval with invalid stat type."""
        result = get_league_leaders(2023, "invalid_stat")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "No mock data available for stat type invalid_stat")

    def test_get_game_odds_success(self):
        """Test successful game odds retrieval."""
        # Test with game_id
        result = get_game_odds(game_id=1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["game_id"], 1)
        self.assertEqual(result[0]["spread"], -5.5)
        self.assertEqual(result[0]["over_under"], 235.5)

        # Test with date
        result = get_game_odds(game_date="2024-03-15")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["game_id"], 1)

    def test_get_game_odds_missing_params(self):
        """Test game odds retrieval with missing parameters."""
        result = get_game_odds()
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Either game_date or game_id must be provided")

    def test_get_player_injuries_success(self):
        """Test successful player injuries retrieval."""
        result = get_player_injuries()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["player"]["id"], 1)  # Curry
        self.assertEqual(result[0]["status"], "Questionable")
        self.assertEqual(result[0]["note"], "Right ankle sprain")

    def test_get_head_to_head_stats_success(self):
        """Test successful head-to-head stats retrieval."""
        result = get_head_to_head_stats("Warriors", "Lakers", 2023)
        self.assertEqual(result["total_games"], 1)
        self.assertEqual(result["Warriors_wins"], 1)
        self.assertEqual(result["Lakers_wins"], 0)
        self.assertEqual(len(result["games"]), 1)
        self.assertEqual(result["games"][0]["home_team_score"], 120)
        self.assertEqual(result["games"][0]["visitor_team_score"], 115)

    def test_get_head_to_head_stats_team_not_found(self):
        """Test head-to-head stats retrieval when team not found."""
        result = get_head_to_head_stats("NonExistent Team", "Lakers", 2023)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "One or both teams not found")

    def test_get_head_to_head_stats_no_games(self):
        """Test head-to-head stats retrieval when no games exist."""
        # Add a new team to mock data that has no games
        result = get_head_to_head_stats("Warriors", "NonExistent Team", 2023)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "One or both teams not found")

    def test_get_player_info_empty_names(self):
        """Test player info retrieval with empty names."""
        # Test with empty first name
        result = get_player_info("", "Curry")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "First name and last name are required")

        # Test with empty last name
        result = get_player_info("Stephen", "")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "First name and last name are required")

        # Test with both names empty
        result = get_player_info("", "")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "First name and last name are required")

    def test_get_player_info_special_characters(self):
        """Test player info retrieval with special characters in names."""
        result = get_player_info("O'Connor", "Smith")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "No player found with name O'Connor Smith")

    def test_get_team_info_partial_matches(self):
        """Test team info retrieval with partial matches."""
        # Test with partial name that matches multiple teams
        result = get_team_info("Warriors")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Multiple teams found. Please use full team name.")

        # Test with very short partial name
        result = get_team_info("War")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Multiple teams found. Please use full team name.")

    def test_get_team_standings_invalid_year(self):
        """Test standings retrieval with invalid years."""
        # Test with future year
        result = get_team_standings(2025)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Invalid year. Please use a year between 2000 and 2024")

        # Test with past year
        result = get_team_standings(1999)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Invalid year. Please use a year between 2000 and 2024")

        # Test with current year
        current_year = datetime.now().year
        result = get_team_standings(current_year)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_get_league_leaders_empty_stats(self):
        """Test league leaders retrieval with empty or invalid stats."""
        # Test with empty stat type
        result = get_league_leaders(2023, "")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Stat type is required")

        # Test with whitespace stat type
        result = get_league_leaders(2023, "   ")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Stat type is required")

        # Test with non-existent stat type
        result = get_league_leaders(2023, "nonexistent")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "No mock data available for stat type nonexistent")

    def test_get_game_odds_invalid_date(self):
        """Test game odds retrieval with invalid dates."""
        # Test with invalid date format
        result = get_game_odds(game_date="invalid-date")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Invalid date format. Please use YYYY-MM-DD")

        # Test with future date
        future_date = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
        result = get_game_odds(game_date=future_date)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "No games found for the specified date")

        # Test with past date
        past_date = "2000-01-01"
        result = get_game_odds(game_date=past_date)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "No games found for the specified date")

    def test_get_game_odds_invalid_game_id(self):
        """Test game odds retrieval with invalid game IDs."""
        # Test with non-existent game ID
        result = get_game_odds(game_id=999)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "No game found with ID 999")

        # Test with negative game ID
        result = get_game_odds(game_id=-1)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Invalid game ID")

        # Test with zero game ID
        result = get_game_odds(game_id=0)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Invalid game ID")

    def test_get_player_injuries_empty_list(self):
        """Test player injuries retrieval with no injuries."""
        # Temporarily modify mock data to have no injuries
        original_injuries = MOCK_INJURIES.copy()
        MOCK_INJURIES.clear()
        
        result = get_player_injuries()
        self.assertEqual(len(result), 0)
        
        # Restore original mock data
        MOCK_INJURIES.extend(original_injuries)

    def test_get_head_to_head_stats_same_team(self):
        """Test head-to-head stats retrieval with same team."""
        result = get_head_to_head_stats("Warriors", "Warriors", 2023)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Cannot compare a team with itself")

    def test_get_head_to_head_stats_invalid_year(self):
        """Test head-to-head stats retrieval with invalid year."""
        # Test with future year
        result = get_head_to_head_stats("Warriors", "Lakers", 2025)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Invalid year. Please use a year between 2000 and 2024")

        # Test with past year
        result = get_head_to_head_stats("Warriors", "Lakers", 1999)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Invalid year. Please use a year between 2000 and 2024")

    def test_get_head_to_head_stats_empty_team_names(self):
        """Test head-to-head stats retrieval with empty team names."""
        # Test with empty home team
        result = get_head_to_head_stats("", "Lakers", 2023)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Both team names are required")

        # Test with empty away team
        result = get_head_to_head_stats("Warriors", "", 2023)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Both team names are required")

        # Test with both teams empty
        result = get_head_to_head_stats("", "", 2023)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Both team names are required")

    def test_get_head_to_head_stats_case_sensitivity(self):
        """Test head-to-head stats retrieval with different case variations."""
        # Test with lowercase team names
        result = get_head_to_head_stats("warriors", "lakers", 2023)
        self.assertEqual(result["total_games"], 1)
        self.assertEqual(result["Warriors_wins"], 1)

        # Test with uppercase team names
        result = get_head_to_head_stats("WARRIORS", "LAKERS", 2023)
        self.assertEqual(result["total_games"], 1)
        self.assertEqual(result["Warriors_wins"], 1)

        # Test with mixed case team names
        result = get_head_to_head_stats("WaRrIoRs", "LaKeRs", 2023)
        self.assertEqual(result["total_games"], 1)
        self.assertEqual(result["Warriors_wins"], 1)

if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNBATools)

    # Create a custom test result handler
    result = TestResult()
    
    # Create a custom runner that uses our result class
    runner = unittest.TextTestRunner(resultclass=TestResult)
    
    # Run the tests using our custom runner
    runner.run(suite)
    
    # Exit with appropriate status code
    success = result.wasSuccessful()
    exit(not success)
