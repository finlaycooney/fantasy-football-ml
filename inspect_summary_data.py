import json
import pandas as pd # Just for pretty printing if needed

# --- Configuration ---
# Path to the raw historical summary JSON file
SUMMARY_DATA_PATH = 'fpl_history_page.json'

# --- Load the Data ---
print(f"Loading summary data from '{SUMMARY_DATA_PATH}' for inspection...")
try:
    with open(SUMMARY_DATA_PATH, 'r') as f:
        data = json.load(f)
    print("Summary data loaded successfully.")
except FileNotFoundError:
    print(f"ERROR: The file '{SUMMARY_DATA_PATH}' was not found.")
    print("Please ensure it exists and the path is correct.")
    exit()
except json.JSONDecodeError:
    print(f"ERROR: Could not decode JSON from '{SUMMARY_DATA_PATH}'. Is it valid JSON?")
    exit()
except Exception as e:
    print(f"An unexpected error occurred while loading: {e}")
    exit()

# --- Navigate to the Player List ---
# Based on our previous debugging, the player list should be under the 'history' key
player_list = []
try:
    player_list = data['history']
    print(f"\nFound a list under the 'history' key with {len(player_list)} items.")
except KeyError:
    print(f"\nERROR: Could not find the 'history' key in '{SUMMARY_DATA_PATH}'.")
    print("Please check the structure of your JSON file.")
    exit()
except TypeError:
    print(f"\nERROR: Expected a dictionary at the top level, but 'data' is not a dictionary.")
    exit()

# --- Inspect Individual Player Records ---
if not player_list:
    print("The player list is empty. No players to inspect.")
    exit()

print("\n--- Inspecting First Few Player Records ---")
# We'll inspect the first 5 records (or fewer if there aren't 5)
for i, player_record in enumerate(player_list[:5]):
    print(f"\nPlayer Record {i+1}:")
    print(f"Type: {type(player_record)}")

    if isinstance(player_record, dict):
        print("Keys present in this record:")
        print(list(player_record.keys())) # Convert to list for cleaner printing

        # --- IMPORTANT: Look for these keys ---
        # This is what you NEED for the next scraping step
        required_keys = ['id', 'element_type', 'web_name', 'team'] # Common FPL keys
        found_all_required = True
        for key in required_keys:
            if key not in player_record:
                print(f"  WARNING: Required key '{key}' is MISSING from this record.")
                found_all_required = False
            else:
                print(f"  {key}: {player_record[key]}")
        
        if found_all_required:
            print("  ✅ All essential keys ('id', 'element_type', 'web_name', 'team') found for this player.")
        else:
            print("  ❌ Some essential keys were missing for this player record.")
        
    elif isinstance(player_record, list):
        print("This record is a list. This is unexpected for player summaries.")
        print(f"First item in this list: {player_record[0]}")
    else:
        print(f"This record is of an unexpected type: {type(player_record)}")

print("\n--- Inspection complete. ---")
print("Based on the output, identify the correct key for 'player_id' (e.g., 'id', 'element', 'code').")
print("You also need 'web_name' (player's common name) and 'element_type' (position).")
print("Update your 'get_gameweek_data.py' script accordingly.")

