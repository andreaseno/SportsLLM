from typing import List, Dict, Optional, Union
from datetime import datetime
from balldontlie import BalldontlieAPI
import os
from pathlib import Path
import traceback

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

def get_player_info(player_name: str) -> Dict:
    """Get detailed information about an NBA player.

    Args:
        player_name: Full name of the player (e.g., "Stephen Curry")

    Returns:
        Dict containing player information including id, name, position, height, weight, etc.
    """
    print(f"\n[DEBUG] get_player_info() called with player_name: {player_name}")
    try:
        # Search for player
        response = api.nba.players.list(search="kyrie")
        print(f"[DEBUG] API Response: {response}")
        
        # Access the data field of the paginated response
        players = response.data if hasattr(response, 'data') else []
        
        if not players:
            print(f"[DEBUG] No player found with name: {player_name}")
            return {"error": f"No player found with name {player_name}"}
        
        # Return the first (most relevant) match
        player = players[0]
        print(f"[DEBUG] Found player: {player}")
        print(f"[DEBUG] Player type: {type(player)}")
        print(f"[DEBUG] Player attributes: {dir(player)}")
        return player
    except Exception as e:
        print(f"[ERROR] Error in get_player_info(): {str(e)}")
        print("[DEBUG] Full error traceback:")
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
        response = api.nba.teams.list()
        teams = response.data if hasattr(response, 'data') else []
        print(f"[DEBUG] Found {len(teams)} teams in total")
        
        for team in teams:
            if team_name.lower() in team["full_name"].lower() or team_name.lower() in team["name"].lower():
                print(f"[DEBUG] Found matching team: {team}")
                return team
        print(f"[DEBUG] No team found with name: {team_name}")
        return {"error": f"No team found with name {team_name}"}
    except Exception as e:
        print(f"[ERROR] Error in get_team_info(): {str(e)}")
        print("[DEBUG] Full error traceback:")
        traceback.print_exc()
        return {"error": f"Error fetching team info: {str(e)}"}

def get_team_standings(season: int) -> Dict:
    """Get the current NBA standings for a specific season.

    Args:
        season: The season year (e.g., 2023 for 2023-24 season)

    Returns:
        Dict containing standings information for all teams including wins, losses, conference rank, etc.
    """
    print(f"\n[DEBUG] get_team_standings() called with season: {season}")
    try:
        response = api.nba.standings.get(season=season)
        standings = response.data if hasattr(response, 'data') else []
        print(f"[DEBUG] Retrieved standings for {season} season with {len(standings)} teams")
        return standings
    except Exception as e:
        print(f"[ERROR] Error in get_team_standings(): {str(e)}")
        print("[DEBUG] Full error traceback:")
        traceback.print_exc()
        return {"error": f"Error fetching standings: {str(e)}"}

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

def get_league_leaders(season: int, stat_type: str) -> List[Dict]:
    """Get the NBA statistical leaders for a specific category.

    Args:
        season: The season year (e.g., 2023 for 2023-24 season)
        stat_type: Type of stat to get leaders for (e.g., "pts", "reb", "ast", "stl", "blk")

    Returns:
        List of dicts containing top players and their stats for the specified category
    """
    print(f"\n[DEBUG] get_league_leaders() called with season: {season}, stat_type: {stat_type}")
    try:
        response = api.nba.leaders.get(
            season=season,
            stat_type=stat_type
        )
        leaders = response.data if hasattr(response, 'data') else []
        print(f"[DEBUG] Retrieved {len(leaders)} leaders for {stat_type}")
        return leaders
    except Exception as e:
        print(f"[ERROR] Error in get_league_leaders(): {str(e)}")
        print("[DEBUG] Full error traceback:")
        traceback.print_exc()
        return {"error": f"Error fetching league leaders: {str(e)}"}

def get_game_odds(game_date: str = None, game_id: int = None) -> List[Dict]:
    """Get betting odds for NBA games.

    Args:
        game_date: Date of games in YYYY-MM-DD format (e.g., "2024-04-01")
        game_id: Specific game ID to get odds for

    Returns:
        List of dicts containing betting odds information including moneyline, spread, and over/under
    """
    print(f"\n[DEBUG] get_game_odds() called with game_date: {game_date}, game_id: {game_id}")
    try:
        if game_date:
            response = api.nba.odds.list(date=game_date)
            odds = response.data if hasattr(response, 'data') else []
            print(f"[DEBUG] Retrieved {len(odds)} odds for date {game_date}")
        elif game_id:
            response = api.nba.odds.list(game_id=game_id)
            odds = response.data if hasattr(response, 'data') else []
            print(f"[DEBUG] Retrieved odds for game_id {game_id}")
        else:
            print("[DEBUG] No game_date or game_id provided")
            return {"error": "Either game_date or game_id must be provided"}
        
        return odds
    except Exception as e:
        print(f"[ERROR] Error in get_game_odds(): {str(e)}")
        print("[DEBUG] Full error traceback:")
        traceback.print_exc()
        return {"error": f"Error fetching game odds: {str(e)}"}

def get_player_injuries() -> List[Dict]:
    """Get current NBA player injuries.

    Returns:
        List of dicts containing information about injured players including status and expected return
    """
    print("\n[DEBUG] get_player_injuries() called")
    try:
        response = api.nba.player_injuries.list()
        injuries = response.data if hasattr(response, 'data') else []
        print(f"[DEBUG] Retrieved {len(injuries)} player injuries")
        return injuries
    except Exception as e:
        print(f"[ERROR] Error in get_player_injuries(): {str(e)}")
        print("[DEBUG] Full error traceback:")
        traceback.print_exc()
        return {"error": f"Error fetching player injuries: {str(e)}"}

def get_head_to_head_stats(team1_name: str, team2_name: str, season: int) -> Dict:
    """Get head-to-head statistics between two teams for a specific season.

    Args:
        team1_name: Name of first team
        team2_name: Name of second team
        season: The season year (e.g., 2023 for 2023-24 season)

    Returns:
        Dict containing head-to-head statistics between the teams
    """
    print(f"\n[DEBUG] get_head_to_head_stats() called with team1: {team1_name}, team2: {team2_name}, season: {season}")
    try:
        # Get team IDs
        team1 = get_team_info(team1_name)
        team2 = get_team_info(team2_name)
        
        if "error" in team1 or "error" in team2:
            print("[DEBUG] One or both teams not found")
            return {"error": "One or both teams not found"}
        
        print(f"[DEBUG] Found team IDs - team1: {team1['id']}, team2: {team2['id']}")
        
        # Get games between these teams
        response = api.nba.games.list(
            team_ids=[team1["id"], team2["id"]],
            seasons=[season]
        )
        games = response.data if hasattr(response, 'data') else []
        
        print(f"[DEBUG] Found {len(games)} games between teams")
        
        # Process head-to-head stats
        stats = {
            "total_games": len(games),
            f"{team1['name']}_wins": 0,
            f"{team2['name']}_wins": 0,
            "games": games
        }
        
        for game in games:
            if game["home_team_score"] > game["visitor_team_score"]:
                winner_id = game["home_team"]["id"]
            else:
                winner_id = game["visitor_team"]["id"]
                
            if winner_id == team1["id"]:
                stats[f"{team1['name']}_wins"] += 1
            else:
                stats[f"{team2['name']}_wins"] += 1
        
        print(f"[DEBUG] Final head-to-head stats: {stats}")
        return stats
    except Exception as e:
        print(f"[ERROR] Error in get_head_to_head_stats(): {str(e)}")
        print("[DEBUG] Full error traceback:")
        traceback.print_exc()
        return {"error": f"Error fetching head-to-head stats: {str(e)}"} 