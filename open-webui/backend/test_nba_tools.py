#!/usr/bin/env python3
"""
Simple test script for NBA tools.
This script allows you to manually test the NBA tools by calling them directly.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import the nba_tools module
sys.path.append(str(Path(__file__).parent))

from open_webui.nba_tools import (
    get_player_info,
    get_team_info,
    get_game_info,
    set_debug_mode,
    set_use_mock_data
)

def print_menu():
    """Print the menu of available options."""
    print("\n=== NBA Tools Test Menu ===")
    print("1. Get Player Info")
    print("2. Get Team Info")
    print("3. Get Game Info")
    print("4. Toggle Debug Mode")
    print("5. Toggle Mock Data")
    print("0. Exit")
    print("=========================")

def get_player_info_test():
    """Test the get_player_info function."""
    first_name = input("Enter player's first name: ")
    last_name = input("Enter player's last name: ")
    result = get_player_info(first_name, last_name)
    print("\nResult:")
    print(result)

def get_team_info_test():
    """Test the get_team_info function."""
    team_name = input("Enter team name: ")
    result = get_team_info(team_name)
    print("\nResult:")
    print(result)

def get_game_info_test():
    """Test the get_game_info function."""
    season = int(input("Enter season year (e.g., 2023): "))
    home_team = input("Enter home team name: ")
    away_team = input("Enter away team name: ")
    result = get_game_info(season, home_team, away_team)
    print("\nResult:")
    print(result)

def toggle_debug_mode():
    """Toggle debug mode on/off."""
    global debug_mode
    debug_mode = not debug_mode
    set_debug_mode(debug_mode)
    print(f"Debug mode {'enabled' if debug_mode else 'disabled'}")

def toggle_mock_data():
    """Toggle mock data on/off."""
    global use_mock_data
    use_mock_data = not use_mock_data
    set_use_mock_data(use_mock_data)
    print(f"Mock data {'enabled' if use_mock_data else 'disabled'}")

if __name__ == "__main__":
    # Initialize global variables
    debug_mode = False
    use_mock_data = False
    
    # Set initial states
    set_debug_mode(debug_mode)
    set_use_mock_data(use_mock_data)
    
    print("NBA Tools Test Script")
    print("This script allows you to test the NBA tools manually.")
    print("Debug mode is disabled by default.")
    print("Mock data is disabled by default.")
    
    # while True:
    #     print_menu()
    #     choice = input("Enter your choice (0-5): ")
        
    #     if choice == "1":
    #         get_player_info_test()
    #     elif choice == "2":
    #         get_team_info_test()
    #     elif choice == "3":
    #         get_game_info_test()
    #     elif choice == "4":
    #         toggle_debug_mode()
    #     elif choice == "5":
    #         toggle_mock_data()
    #     elif choice == "0":
    #         print("Exiting...")
    #         break
    #     else:
    #         print("Invalid choice. Please try again.") 
    result = get_game_info(2022, "Warriors", "Wizards")
    print("\nResult:")
    print(result)