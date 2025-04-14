from typing import List, Dict, Optional, Union
from datetime import datetime, timedelta
from balldontlie import BalldontlieAPI
import os
from pathlib import Path
import traceback

# Mock data for testing
MOCK_PLAYERS = [
    {
        "id": 1,
        "first_name": "Stephen",
        "last_name": "Curry",
        "position": "G",
        "height_feet": 6,
        "height_inches": 3,
        "weight_pounds": 185,
        "team": {
            "id": 1,
            "name": "Warriors",
            "full_name": "Golden State Warriors"
        }
    },
    {
        "id": 2,
        "first_name": "LeBron",
        "last_name": "James",
        "position": "F",
        "height_feet": 6,
        "height_inches": 9,
        "weight_pounds": 250,
        "team": {
            "id": 2,
            "name": "Lakers",
            "full_name": "Los Angeles Lakers"
        }
    }
]

MOCK_TEAMS = [
    {
        "id": 1,
        "name": "Warriors",
        "full_name": "Golden State Warriors",
        "city": "Golden State",
        "conference": "West",
        "division": "Pacific"
    },
    {
        "id": 2,
        "name": "Lakers",
        "full_name": "Los Angeles Lakers",
        "city": "Los Angeles",
        "conference": "West",
        "division": "Pacific"
    }
]

MOCK_STANDINGS = [
    {
        "team": MOCK_TEAMS[0],
        "conference_rank": 1,
        "division_rank": 1,
        "wins": 45,
        "losses": 20
    },
    {
        "team": MOCK_TEAMS[1],
        "conference_rank": 2,
        "division_rank": 2,
        "wins": 40,
        "losses": 25
    }
]

MOCK_LEADERS = {
    "pts": [
        {
            "player": MOCK_PLAYERS[0],
            "pts": 28.5,
            "season": 2023
        },
        {
            "player": MOCK_PLAYERS[1],
            "pts": 25.3,
            "season": 2023
        }
    ],
    "reb": [
        {
            "player": MOCK_PLAYERS[1],
            "reb": 8.2,
            "season": 2023
        }
    ]
}

MOCK_GAMES = [
    {
        "id": 1,
        "date": "2024-03-15",
        "home_team": MOCK_TEAMS[0],
        "visitor_team": MOCK_TEAMS[1],
        "home_team_score": 120,
        "visitor_team_score": 115
    }
]

MOCK_ODDS = [
    {
        "game_id": 1,
        "bookmaker": "DraftKings",
        "spread": -5.5,
        "over_under": 235.5,
        "home_team_odds": -110,
        "away_team_odds": -110
    }
]

MOCK_INJURIES = [
    {
        "player": MOCK_PLAYERS[0],
        "team": MOCK_TEAMS[0],
        "status": "Questionable",
        "note": "Right ankle sprain"
    }
]

# Global flags
USE_MOCK_DATA = False
DEBUG_MODE = False

def set_debug_mode(debug: bool):
    """Set whether to enable debug print statements.
    
    Args:
        debug: Boolean indicating whether to enable debug prints
    """
    global DEBUG_MODE
    DEBUG_MODE = debug

def debug_print(*args, **kwargs):
    """Print debug messages only when DEBUG_MODE is True."""
    if DEBUG_MODE:
        print(*args, **kwargs)

def set_use_mock_data(use_mock: bool):
    """Set whether to use mock data for testing.
    
    Args:
        use_mock: Boolean indicating whether to use mock data
    """
    global USE_MOCK_DATA
    USE_MOCK_DATA = use_mock

####################################
# Load .env file
####################################

OPEN_WEBUI_DIR = Path(__file__).parent  # the path containing this file
print(OPEN_WEBUI_DIR)

BACKEND_DIR = OPEN_WEBUI_DIR.parent  # the path containing this file
BASE_DIR = BACKEND_DIR.parent  # the path containing the backend/

print(BACKEND_DIR)
print(BASE_DIR)

try:
    from dotenv import find_dotenv, load_dotenv

    load_dotenv(find_dotenv(str(BASE_DIR / ".env")))
except ImportError:
    print("dotenv not installed, skipping...")

# Initialize the API client
api = BalldontlieAPI(api_key=os.environ.get("BALLDONTLIE_API_KEY"))

def get_player_info(player_first_name: str, player_last_name: str) -> Dict:
    """Get detailed information about an NBA player.

    Args:
        player_first_name: First name of the player (e.g., "Stephen")
        player_last_name: Last name of the player (e.g., "Curry")

    Returns:
        Dict containing player information including id, name, position, height, weight, etc.
    """
    debug_print(f"\n[DEBUG] get_player_info() called with player_first_name: {player_first_name}, player_last_name: {player_last_name}")
    try:
        # Input validation
        if not player_first_name or not player_last_name:
            return {"error": "First name and last name are required"}
        
        if USE_MOCK_DATA:
            # Search through mock players
            for player in MOCK_PLAYERS:
                full_name = f"{player['first_name']} {player['last_name']}"
                if player_first_name.lower() in full_name.lower() and player_last_name.lower() in full_name.lower():
                    debug_print(f"[DEBUG] Found mock player: {player}")
                    return player
            debug_print(f"[DEBUG] No mock player found with name: {player_first_name} {player_last_name}")
            return {"error": f"No player found with name {player_first_name} {player_last_name}"}
        
        # Real API call
        response = api.nba.players.list(search=f"{player_first_name}")
        debug_print(f"[DEBUG] API Response: {response}")
        
        # Access the data field of the paginated response
        players = response.data if hasattr(response, 'data') else []
        
        if not players:
            debug_print(f"[DEBUG] No player found with name: {player_first_name} {player_last_name}")
            return {"error": f"No player found with name {player_first_name} {player_last_name}"}
        
        # Return the first (most relevant) match
        player = players[0]
        debug_print(f"[DEBUG] Found player: {player}")
        debug_print(f"[DEBUG] Player type: {type(player)}")
        debug_print(f"[DEBUG] Player attributes: {dir(player)}")
        return player
    except Exception as e:
        debug_print(f"[ERROR] Error in get_player_info(): {str(e)}")
        debug_print("[DEBUG] Full error traceback:")
        traceback.print_exc()
        return {"error": f"Error fetching player info: {str(e)}"}

def get_team_info(team_name: str) -> Dict:
    """Get detailed information about an NBA team.

    Args:
        team_name: Name of the team (e.g., "Warriors" or "Golden State Warriors")

    Returns:
        Dict containing team information including id, full_name, conference, division, etc.
    """
    print(f"\n[DEBUG] get_team_info() called with team_name: {team_name}")
    try:
        # Input validation
        if not team_name:
            return {"error": "Team name is required"}
        
        if USE_MOCK_DATA:
            # Search through mock teams
            matching_teams = []
            for team in MOCK_TEAMS:
                if team_name.lower() in team["full_name"].lower() or team_name.lower() in team["name"].lower():
                    matching_teams.append(team)
            
            if len(matching_teams) > 1:
                return {"error": "Multiple teams found. Please use full team name."}
            elif len(matching_teams) == 1:
                print(f"[DEBUG] Found mock team: {matching_teams[0]}")
                return matching_teams[0]
            else:
                print(f"[DEBUG] No mock team found with name: {team_name}")
                return {"error": f"No team found with name {team_name}"}
        
        # Real API call
        response = api.nba.teams.list()
        teams = response.data if hasattr(response, 'data') else []
        # print(f"[DEBUG] Found {len(teams)} teams in total")
        # print(f"[DEBUG] Teams: {teams}")
        
        matching_teams = []
        for team in teams:
            # print(f"[DEBUG] Team: {team}")
            if team_name.lower() in team.full_name.lower() or team_name.lower() in team.name.lower():
                matching_teams.append(team)
        
        if len(matching_teams) > 1:
            return {"error": "Multiple teams found. Please use full team name."}
        elif len(matching_teams) == 1:
            print(f"[DEBUG] Found matching team: {matching_teams[0]}")
            return matching_teams[0]
        else:
            print(f"[DEBUG] No team found with name: {team_name}")
            return {"error": f"No team found with name {team_name}"}
    except Exception as e:
        print(f"[ERROR] Error in get_team_info(): {str(e)}")
        print("[DEBUG] Full error traceback:")
        traceback.print_exc()
        return {"error": f"Error fetching team info: {str(e)}"}

def get_game_info(season: int, home_team: str, away_team: str) -> Dict:
    """Get detailed information about an NBA game, or all nba games. Search for specific game by season, home_team, and away team.

    Args:
        season: The season year (e.g., 2023 for 2023-24 season)
        home_team: Name of the home team (e.g., "Warriors" or "Golden State Warriors")
        away_team: Name of the away team (e.g., "Warriors" or "Golden State Warriors")

    Returns:
        Dict containing game information including period, start_time, time_in_period, etc.
    """
    print(f"\n[DEBUG] get_game_info() called with season: {season}, home_team: {home_team}, away_team: {away_team} ")
    try:
        # Input validation
        if not home_team:
            return {"error": "home_team name is required"}
        if not away_team:
            return {"error": "away_team name is required"}
        if not season:
            return {"error": "season name is required"}
        
        if USE_MOCK_DATA:
            # Search through mock games
            matching_games = []
            for game in MOCK_GAMES:
                if (game["home_team"]["name"].lower() == home_team.lower() and 
                    game["visitor_team"]["name"].lower() == away_team.lower()):
                    matching_games.append(game)
            
            if len(matching_games) >= 1:
                print(f"[DEBUG] Found matching mock games: {matching_games}")
                return matching_games
            else:
                print(f"[DEBUG] No mock games found")
                return {"error": f"No games found"}
        
        # Real API call with pagination
        all_games = []
        next_cursor = None
        per_page = 100  # Maximum allowed by the API
        
        # while True:
            # Make API request with current cursor
        params = {
            "seasons": [season],
            "per_page": per_page
        }
        
        # if next_cursor is not None:
        #     params["cursor"] = next_cursor
            
        response = api.nba.games.list(**params)
        all_games = response.data if hasattr(response, 'data') else  []
        
        print(f"[DEBUG] Retrieved {len(all_games)} games in total")
        
        # Filter games by home and away team
        matching_games = []
        for game in all_games:
            if (home_team.lower() in game.home_team.name.lower() and 
                away_team.lower() in game.visitor_team.name.lower()):
                matching_games.append(game)
        
        if len(matching_games) >= 1:
            print(f"[DEBUG] Found {len(matching_games)} matching games")
            return matching_games
        else:
            print(f"[DEBUG] No matching games found")
            return {"error": f"No games found"}
            
    except Exception as e:
        print(f"[ERROR] Error in get_game_info(): {str(e)}")
        print("[DEBUG] Full error traceback:")
        traceback.print_exc()
        return {"error": f"Error fetching game info: {str(e)}"}

# def get_team_standings(season: int) -> Dict:
#     """Get the current NBA standings for a specific season.

#     Args:
#         season: The season year (e.g., 2023 for 2023-24 season)

#     Returns:
#         Dict containing standings information for all teams including wins, losses, conference rank, etc.
#     """
#     print(f"\n[DEBUG] get_team_standings() called with season: {season}")
#     try:
#         # Input validation
#         current_year = datetime.now().year
#         if not isinstance(season, int) or season < 2000 or season > current_year:
#             return {"error": f"Invalid year. Please use a year between 2000 and {current_year}"}
        
#         if USE_MOCK_DATA:
#             print(f"[DEBUG] Returning mock standings for {season} season")
#             return MOCK_STANDINGS
        
#         # Real API call
#         response = api.nba.standings.get(season=season)
#         standings = response.data if hasattr(response, 'data') else []
#         print(f"[DEBUG] Retrieved standings for {season} season with {len(standings)} teams")
#         return standings
#     except Exception as e:
#         print(f"[ERROR] Error in get_team_standings(): {str(e)}")
#         print("[DEBUG] Full error traceback:")
#         traceback.print_exc()
#         return {"error": f"Error fetching standings: {str(e)}"}

# TODO: FIX get_player_season_stats

# Traceback (most recent call last):
#   File "/Users/oga/Desktop/gwu_stuff/Masters Stuff/Capstone/SportsLLM/open-webui/backend/open_webui/nba_tools.py", line 133, in get_player_season_stats
#     response = api.nba.season_averages.get(
#                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# TypeError: NBASeasonAveragesAPI.get() got an unexpected keyword argument 'player_ids'

# def get_player_season_stats(player_name: str, season: int) -> Dict:
#     """Get a player's season averages for a specific season.

#     Args:
#         player_name: Full name of the player (e.g., "Stephen Curry")
#         season: The season year (e.g., 2023 for 2023-24 season)

#     Returns:
#         Dict containing player's season averages including points, rebounds, assists, etc.
#     """
#     print(f"\n[DEBUG] get_player_season_stats() called with player_name: {player_name}, season: {season}")
#     try:
#         # First get player ID
#         player = get_player_info(player_name)
#         if isinstance(player, dict) and "error" in player:
#             print(f"[DEBUG] Error finding player: {player['error']}")
#             return player
        
#         print(f"[DEBUG] Found player ID: {player.id}")
#         # Get season averages
#         response = api.nba.season_averages.get(
#             season=season,
#             player_ids=[player.id]
#         )
#         stats = response.data if hasattr(response, 'data') else []
        
#         if not stats:
#             print(f"[DEBUG] No stats found for player in season {season}")
#             return {"error": f"No stats found for {player_name} in {season} season"}
        
#         print(f"[DEBUG] Retrieved season stats: {stats[0]}")
#         return stats[0]
#     except Exception as e:
#         print(f"[ERROR] Error in get_player_season_stats(): {str(e)}")
#         print("[DEBUG] Full error traceback:")
#         traceback.print_exc()
#         return {"error": f"Error fetching season stats: {str(e)}"}

# def get_league_leaders(season: int, stat_type: str) -> List[Dict]:
#     """Get the NBA statistical leaders for a specific category.

#     Args:
#         season: The season year (e.g., 2023 for 2023-24 season)
#         stat_type: Type of stat to get leaders for (e.g., "pts", "reb", "ast", "stl", "blk")

#     Returns:
#         List of dicts containing top players and their stats for the specified category
#     """
#     print(f"\n[DEBUG] get_league_leaders() called with season: {season}, stat_type: {stat_type}")
#     try:
#         # Input validation
#         if not stat_type or stat_type.strip() == "":
#             return {"error": "Stat type is required"}
        
#         if USE_MOCK_DATA:
#             if stat_type in MOCK_LEADERS:
#                 print(f"[DEBUG] Returning mock leaders for {stat_type}")
#                 return MOCK_LEADERS[stat_type]
#             print(f"[DEBUG] No mock data for stat type: {stat_type}")
#             return {"error": f"No mock data available for stat type {stat_type}"}
        
#         # Real API call
#         response = api.nba.leaders.get(
#             season=season,
#             stat_type=stat_type
#         )
#         leaders = response.data if hasattr(response, 'data') else []
#         print(f"[DEBUG] Retrieved {len(leaders)} leaders for {stat_type}")
#         return leaders
#     except Exception as e:
#         print(f"[ERROR] Error in get_league_leaders(): {str(e)}")
#         print("[DEBUG] Full error traceback:")
#         traceback.print_exc()
#         return {"error": f"Error fetching league leaders: {str(e)}"}

# def get_game_odds(game_date: str = None, game_id: int = None) -> List[Dict]:
#     """Get betting odds for NBA games.

#     Args:
#         game_date: Date of games in YYYY-MM-DD format (e.g., "2024-04-01")
#         game_id: Specific game ID to get odds for

#     Returns:
#         List of dicts containing betting odds information including moneyline, spread, and over/under
#     """
#     print(f"\n[DEBUG] get_game_odds() called with game_date: {game_date}, game_id: {game_id}")
#     try:
#         # Input validation
#         if not game_date and not game_id:
#             return {"error": "Either game_date or game_id must be provided"}
        
#         if game_id is not None:
#             if not isinstance(game_id, int) or game_id <= 0:
#                 return {"error": "Invalid game ID"}
        
#         if game_date:
#             try:
#                 # Validate date format
#                 datetime.strptime(game_date, "%Y-%m-%d")
#                 # Check if date is in the past
#                 game_datetime = datetime.strptime(game_date, "%Y-%m-%d")
#                 if game_datetime.date() < datetime.now().date():
#                     return {"error": "No games found for the specified date"}
#                 # Check if date is too far in the future
#                 if game_datetime.date() > (datetime.now() + timedelta(days=30)).date():
#                     return {"error": "No games found for the specified date"}
#             except ValueError:
#                 return {"error": "Invalid date format. Please use YYYY-MM-DD"}
        
#         if USE_MOCK_DATA:
#             if game_id:
#                 # Filter mock odds by game_id
#                 odds = [odd for odd in MOCK_ODDS if odd["game_id"] == game_id]
#                 if not odds:
#                     return {"error": f"No game found with ID {game_id}"}
#             elif game_date:
#                 # For mock data, we'll just return all odds since we don't have date filtering
#                 odds = MOCK_ODDS
#             print(f"[DEBUG] Returning {len(odds)} mock odds")
#             return odds
        
#         # Real API call
#         if game_date:
#             response = api.nba.odds.list(date=game_date)
#             odds = response.data if hasattr(response, 'data') else []
#             if not odds:
#                 return {"error": "No games found for the specified date"}
#             print(f"[DEBUG] Retrieved {len(odds)} odds for date {game_date}")
#         elif game_id:
#             response = api.nba.odds.list(game_id=game_id)
#             odds = response.data if hasattr(response, 'data') else []
#             if not odds:
#                 return {"error": f"No game found with ID {game_id}"}
#             print(f"[DEBUG] Retrieved odds for game_id {game_id}")
        
#         return odds
#     except Exception as e:
#         print(f"[ERROR] Error in get_game_odds(): {str(e)}")
#         print("[DEBUG] Full error traceback:")
#         traceback.print_exc()
#         return {"error": f"Error fetching game odds: {str(e)}"}

# def get_player_injuries() -> List[Dict]:
#     """Get current NBA player injuries.

#     Returns:
#         List of dicts containing information about injured players including status and expected return
#     """
#     print("\n[DEBUG] get_player_injuries() called")
#     try:
#         if USE_MOCK_DATA:
#             print(f"[DEBUG] Returning {len(MOCK_INJURIES)} mock injuries")
#             return MOCK_INJURIES
        
#         # Real API call
#         response = api.nba.player_injuries.list()
#         injuries = response.data if hasattr(response, 'data') else []
#         print(f"[DEBUG] Retrieved {len(injuries)} player injuries")
#         return injuries
#     except Exception as e:
#         print(f"[ERROR] Error in get_player_injuries(): {str(e)}")
#         print("[DEBUG] Full error traceback:")
#         traceback.print_exc()
#         return {"error": f"Error fetching player injuries: {str(e)}"}

# def get_head_to_head_stats(team1_name: str, team2_name: str, season: int) -> Dict:
#     """Get head-to-head statistics between two teams for a specific season.

#     Args:
#         team1_name: Name of first team
#         team2_name: Name of second team
#         season: The season year (e.g., 2023 for 2023-24 season)

#     Returns:
#         Dict containing head-to-head statistics between the teams
#     """
#     print(f"\n[DEBUG] get_head_to_head_stats() called with team1: {team1_name}, team2: {team2_name}, season: {season}")
#     try:
#         # Input validation
#         if not team1_name or not team2_name:
#             return {"error": "Both team names are required"}
        
#         if team1_name.lower() == team2_name.lower():
#             return {"error": "Cannot compare a team with itself"}
        
#         current_year = datetime.now().year
#         if not isinstance(season, int) or season < 2000 or season > current_year:
#             return {"error": f"Invalid year. Please use a year between 2000 and {current_year}"}
        
#         if USE_MOCK_DATA:
#             # Get team IDs from mock data
#             team1 = get_team_info(team1_name)
#             team2 = get_team_info(team2_name)
            
#             if "error" in team1 or "error" in team2:
#                 print("[DEBUG] One or both teams not found in mock data")
#                 return {"error": "One or both teams not found"}
            
#             print(f"[DEBUG] Found team IDs - team1: {team1['id']}, team2: {team2['id']}")
            
#             # Filter mock games between these teams
#             games = [game for game in MOCK_GAMES 
#                     if (game["home_team"]["id"] == team1["id"] and game["visitor_team"]["id"] == team2["id"]) or
#                        (game["home_team"]["id"] == team2["id"] and game["visitor_team"]["id"] == team1["id"])]
            
#             print(f"[DEBUG] Found {len(games)} mock games between teams")
            
#             # Process head-to-head stats
#             stats = {
#                 "total_games": len(games),
#                 f"{team1['name']}_wins": 0,
#                 f"{team2['name']}_wins": 0,
#                 "games": games
#             }
            
#             for game in games:
#                 if game["home_team_score"] > game["visitor_team_score"]:
#                     winner_id = game["home_team"]["id"]
#                 else:
#                     winner_id = game["visitor_team"]["id"]
                    
#                 if winner_id == team1["id"]:
#                     stats[f"{team1['name']}_wins"] += 1
#                 else:
#                     stats[f"{team2['name']}_wins"] += 1
            
#             print(f"[DEBUG] Final head-to-head stats: {stats}")
#             return stats
        
#         # Real API call
#         # Get team IDs
#         team1 = get_team_info(team1_name)
#         team2 = get_team_info(team2_name)
        
#         if "error" in team1 or "error" in team2:
#             print("[DEBUG] One or both teams not found")
#             return {"error": "One or both teams not found"}
        
#         print(f"[DEBUG] Found team IDs - team1: {team1['id']}, team2: {team2['id']}")
        
#         # Get games between these teams
#         response = api.nba.games.list(
#             team_ids=[team1["id"], team2["id"]],
#             seasons=[season]
#         )
#         games = response.data if hasattr(response, 'data') else []
        
#         print(f"[DEBUG] Found {len(games)} games between teams")
        
#         # Process head-to-head stats
#         stats = {
#             "total_games": len(games),
#             f"{team1['name']}_wins": 0,
#             f"{team2['name']}_wins": 0,
#             "games": games
#         }
        
#         for game in games:
#             if game["home_team_score"] > game["visitor_team_score"]:
#                 winner_id = game["home_team"]["id"]
#             else:
#                 winner_id = game["visitor_team"]["id"]
                
#             if winner_id == team1["id"]:
#                 stats[f"{team1['name']}_wins"] += 1
#             else:
#                 stats[f"{team2['name']}_wins"] += 1
        
#         print(f"[DEBUG] Final head-to-head stats: {stats}")
#         return stats
#     except Exception as e:
#         print(f"[ERROR] Error in get_head_to_head_stats(): {str(e)}")
#         print("[DEBUG] Full error traceback:")
#         traceback.print_exc()
#         return {"error": f"Error fetching head-to-head stats: {str(e)}"} 