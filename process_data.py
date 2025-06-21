import pandas as pd
import json

JSON_FILE_PATH = 'fpl_history_page.json' # Assuming the file is in the same folder

print(f"Loading data from {JSON_FILE_PATH}...")

with open(JSON_FILE_PATH, 'r') as file:
    data = json.load(file)

print("Data loaded. Top-level keys are:", data.keys())

# --- NEW EXPLORATION STEP ---
# Let's grab the 'history' object and see what it is

try:
    history_data = data['history']
    
    print("\n--- Exploring the 'history' object ---")
    print(f"The type of 'history_data' is: {type(history_data)}")

    # If it's a dictionary, what are its keys?
    if isinstance(history_data, dict):
        print("The 'history_data' object is a dictionary. Its keys are:")
        print(history_data.keys())
        
        # We can now try to make a DataFrame from one of THESE keys.
        # Let's guess that the player list is under a key called 'all'.
        # This is just a guess, you may need to change 'all'.
        if 'all' in history_data:
            print("\nFound a key named 'all', trying to create DataFrame from it...")
            df = pd.DataFrame(history_data['all'])
            print("\n--- Success! Here is your data: ---")
            print(df.head())

    # If it's a list, how many items are there?
    elif isinstance(history_data, list):
        print(f"The 'history_data' object is a list with {len(history_data)} items.")
        print("Here is the first item:")
        print(history_data[0])
        
        # If it's a list, we can create the DataFrame directly from it.
        df = pd.DataFrame(history_data)
        print("\n--- Success! Here is your data: ---")
        print(df.head())

except KeyError:
    print("Could not find the 'history' key.")
except Exception as e:
    print(f"An error occurred: {e}")



print("\n--- Data Summary ---")
df.info()

print("\n--- Column Names ---")
print(df.columns)

print("\n--- Statistical Summary ---")
print(df.describe())

df.shape  # Returns a tuple (number_of_rows, number_of_columns)

# 1. Filter for the team
arsenal_players = df[df['team'] == 'Arsenal']

# 2. Select and print the name column
print("--- All Arsenal Player Names ---")
print(arsenal_players['web_name'])