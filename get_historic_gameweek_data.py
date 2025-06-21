#never used this file in the end
import pandas as pd
import json
import requests
import time # We need this library to add delays

# --- Configuration ---
SUMMARY_DATA_PATH = 'fpl_history_page.json' # The summary file we already have
GAMEWEEK_DATA_PATH = 'fpl_gameweek_data_all_players.csv' # The final output file

# --- Stage 1: Load the Master Player List ---
print("Loading summary data to get the master player list...")
try:
    with open(SUMMARY_DATA_PATH, 'r') as f:
        summary_data = json.load(f)
    # Get the list of players from the summary data
    player_list = summary_data['history']
    print(f"Found {len(player_list)} players in the summary file.")
except Exception as e:
    print(f"Error loading summary data: {e}")
    exit()

# --- Stage 2: Loop, Scrape, and Combine ---

# This is where we will store the gameweek data for EVERY player
all_players_gameweek_data = []

print("\nStarting to scrape gameweek data for each player...")
# Loop through each player from our master list
for i, player in enumerate(player_list):
    try:
        # Get the unique ID for the player. Inspect your player_list to find the correct key!
        # It might be 'id', 'code', or something similar.
        player_id = player['id'] # <-- YOU MIGHT NEED TO CHANGE 'id'
        player_name = player['web_name']

        # --- This is the part you need to investigate! ---
        # 1. Go to a player's page on Fantasy Nutmeg in your browser.
        # 2. Open Developer Tools -> Network -> Fetch/XHR.
        # 3. Find the hidden API URL that loads their gameweek data.
        # 4. Paste that URL here, replacing the player's ID with {player_id}.
        API_URL_TEMPLATE = "https://www.fantasynutmeg.com/api/player/history/{player_id}/2022-23" # <-- YOU MUST REPLACE THIS

        # Construct the final URL for this specific player
        player_api_url = API_URL_TEMPLATE.format(player_id=player_id)

        # Make the request to the API
        response = requests.get(player_api_url)
        response.raise_for_status() # This will raise an error if the request fails

        # Get the JSON data, which should be a list of gameweeks for this player
        gameweek_history = response.json()

        # Add the player's ID and name to each gameweek record so we know who it belongs to
        for gameweek in gameweek_history:
            gameweek['player_id'] = player_id
            gameweek['player_name'] = player_name
        
        # Add this player's history to our master list
        all_players_gameweek_data.extend(gameweek_history)
        
        # Print progress and be polite!
        print(f"({i+1}/{len(player_list)}) Successfully fetched data for {player_name}")
        time.sleep(1) # IMPORTANT: Wait 1 second before the next request

    except requests.exceptions.RequestException as e:
        print(f"({i+1}/{len(player_list)}) ERROR fetching data for player ID {player.get('id', 'N/A')}: {e}")
        time.sleep(1) # Still wait even if there's an error
    except KeyError as e:
        print(f"({i+1}/{len(player_list)}) KeyError for a player. Maybe missing '{e}'. Skipping.")
        continue


# --- Stage 3: Create Final DataFrame and Save ---
print("\nScraping complete. Creating final DataFrame...")

# Create the final, big DataFrame from our master list
df_final = pd.DataFrame(all_players_gameweek_data)

print(f"Final DataFrame created with {df_final.shape[0]} rows.")
print("--- First 5 rows of the final data: ---")
print(df_final.head())

# Save the final result to a CSV
df_final.to_csv(GAMEWEEK_DATA_PATH, index=False)

print(f"\n✅ All gameweek data successfully saved to '{GAMEWEEK_DATA_PATH}'")

