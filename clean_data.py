import pandas as pd
import json

# --- Configuration ---
# The path to the raw JSON file you downloaded
RAW_DATA_PATH = 'fpl_history_page.json' 
# The path where you want to save your clean data
CLEAN_DATA_PATH = 'fpl_data_cleaned.csv'

# --- Step 1: Load the Raw Data ---
print(f"Loading raw data from '{RAW_DATA_PATH}'...")
try:
    with open(RAW_DATA_PATH, 'r') as f:
        data = json.load(f)
    print("Raw data loaded successfully.")
except FileNotFoundError:
    print(f"ERROR: The file '{RAW_DATA_PATH}' was not found.")
    print("Please make sure your raw data file is in the same folder and the name is correct.")
    exit() # Stop the script if the file doesn't exist

# --- Step 2: Extract the Player List and Create Initial DataFrame ---
# From our previous exploration, we know the player data is in data['history']['all']
try:
    player_list = data['history']
    df = pd.DataFrame(player_list)
    print(f"Initial DataFrame created with {df.shape[0]} rows and {df.shape[1]} columns.")
except KeyError:
    print("ERROR: Could not find the key 'history' or 'all' in the JSON data.")
    print("The structure of the JSON might have changed. Please re-investigate its keys.")
    exit()

# --- Step 3: The Cleaning Process ---
print("\nStarting the data cleaning process...")

# Create a copy to work on, which is good practice
df_clean = df.copy()

# 3a. Remove Unnecessary Columns
# These columns are unlikely to be useful for predicting points.
columns_to_drop = [
    'birth_date', 'id', 'code', 'photo', 'special', 'first_name', 'second_name',
    'squad_number', 'news', 'news_added', 'ep_this', 'ep_next', 'in_dreamteam',
    'dreamteam_count', 'form', 'status' # We will create our own 'form' feature later
]
# We check which of these columns actually exist in our DataFrame to avoid errors
columns_that_exist = [col for col in columns_to_drop if col in df_clean.columns]
df_clean = df_clean.drop(columns=columns_that_exist)
print(f"- Dropped {len(columns_that_exist)} unnecessary columns.")

# 3b. Correct Data Types (dtypes)
# Convert columns that should be numbers from 'object' (text) to numeric types.
numeric_cols = [
    'points', 'now_cost', 'minutes', 'goals_scored', 'assists', 'bonus',
    'bps', 'influence', 'creativity', 'threat', 'ict_index',
    'yellow_cards', 'red_cards', 'goals_conceded', 'own_goals',
    'penalties_saved', 'penalties_missed', 'saves'
]
for col in numeric_cols:
    if col in df_clean.columns:
        # 'errors='coerce'' will gracefully handle any values that can't be converted
        # by turning them into NaN (Not a Number).
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

print("- Converted relevant columns to numeric types.")

# 3c. Handle Missing Values (NaN)
# For our purpose, we'll assume missing numeric data means '0'.
# For example, if 'goals_scored' is NaN, it's because they scored 0.
df_clean.fillna(0, inplace=True)
print("- Filled missing (NaN) values with 0.")

# 3d. Filter Out Inactive Players
# Remove players who have played 0 minutes all season.
initial_rows = len(df_clean)
df_clean = df_clean[df_clean['minutes'] > 0]
final_rows = len(df_clean)
print(f"- Filtered out inactive players. Removed {initial_rows - final_rows} rows.")

# --- Step 4: Final Inspection & Save Clean Data ---
print("\n--- Cleaning Complete! Final Data Info: ---")
df_clean.info()

print("\n--- First 5 Rows of Clean Data: ---")
print(df_clean.head())

# Save the cleaned DataFrame to a new CSV file.
# index=False prevents pandas from writing an extra column for the row numbers.
df_clean.to_csv(CLEAN_DATA_PATH, index=False)
print(f"\n✅ Clean data successfully saved to '{CLEAN_DATA_PATH}'")

