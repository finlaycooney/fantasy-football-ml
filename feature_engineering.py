import pandas as pd

# --- Configuration ---
# The path to the detailed gameweek data we scraped in the last lesson.
GAMEWEEK_DATA_PATH = 'fpl_gameweek_data_2024-25_raw.csv'
# The final output file, ready for a machine learning model.
MODEL_READY_DATA_PATH = 'fpl_model_ready_data.csv'

# --- Step 1: Load the Gameweek Data ---
print(f"Loading gameweek data from '{GAMEWEEK_DATA_PATH}'...")
try:
    df = pd.read_csv(GAMEWEEK_DATA_PATH)
    print("Gameweek data loaded successfully.")
except FileNotFoundError:
    print(f"ERROR: The file '{GAMEWEEK_DATA_PATH}' was not found.")
    print("Please run the gameweek scraping script first.")
    exit()

# --- Step 2: Sort the Data Correctly ---
# This is a CRITICAL step. For our 'form' and 'next week's points'
# features to work, the data must be in the correct chronological order for each player.
df.sort_values(by=['player_id', 'gameweek'], inplace=True)
print("\nData sorted by player and gameweek.")

# --- Step 3: Create the Target Variable ---
# The "target" is the value we want our model to predict.
# We want to predict a player's points in their *next* match.
# The .shift(-1) function looks at the *next* row in a group.
# We group by 'player_id' to ensure we're only looking at the next game
# for the same player and not mixing players up.
df['points_next_gameweek'] = df.groupby('player_id')['total_points'].shift(-1)
print("Created the target variable: 'points_next_gameweek'.")


# --- Step 4: Create Rolling Average Features (Form) ---
# These features will describe a player's recent performance trend.
print("Creating rolling average features (form)...")

# Define the stats we want to calculate rolling averages for.
stats_for_rolling = [
    'total_points',
    'minutes',
    'goals_scored',
    'assists',
    'bps', # Bonus Points System
    'ict_index' # Influence, Creativity, Threat Index
]

# We will calculate the rolling average over the last 5 games.
# min_periods=1 means it will calculate even if there's only 1 past game (for early in the season).
for stat in stats_for_rolling:
    # The new column will be named e.g., 'rolling_5_total_points'
    new_col_name = f'rolling_5_{stat}'
    # We group by player, select the stat, and then calculate the rolling average.
    # .shift(1) is used so that the calculation for GW5 only includes data from GW1-4.
    df[new_col_name] = df.groupby('player_id')[stat].shift(1).rolling(window=5, min_periods=1).mean()


# --- Step 5: Handle NaN Values Created by Feature Engineering ---
# The rolling and shifting operations create NaN values.
# For example, the first gameweek for any player has no previous data, so its rolling average is NaN.
# The last gameweek for any player has no "next gameweek", so 'points_next_gameweek' is NaN.
# We will drop the rows with NaN in our target variable, as we can't train on them.
# For the other NaNs, we will fill them with 0.

print("Handling NaN values created during feature engineering...")
# First, fill the NaNs in our new rolling average columns with 0
rolling_cols = [f'rolling_5_{stat}' for stat in stats_for_rolling]
df[rolling_cols] = df[rolling_cols].fillna(0)

# Now, drop any rows where our target variable is NaN. This will be the last gameweek for each player.
initial_rows = len(df)
df.dropna(subset=['points_next_gameweek'], inplace=True)
final_rows = len(df)
print(f"- Dropped {initial_rows - final_rows} rows with no target value (last gameweek for each player).")


# --- Step 6: Final Inspection and Save ---
print("\n--- Feature Engineering Complete! ---")
# Let's select some columns to see how our new features look
print(df[[
    'player_name', 'gameweek', 'total_points', 
    'points_next_gameweek', 'rolling_5_total_points', 'rolling_5_minutes'
]].tail(10))


# Save the final, model-ready DataFrame to a new CSV file.
df.to_csv(MODEL_READY_DATA_PATH, index=False)
print(f"\n✅ Model-ready data successfully saved to '{MODEL_READY_DATA_PATH}'")
