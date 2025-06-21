import pandas as pd
import os
import glob # For finding multiple files matching a pattern

# --- Configuration ---
# Path to the folder containing the gameweek CSVs for a specific season
# IMPORTANT: Adjust this path to where you put the downloaded 'gws' folder
# Example for 2024-25 season data:
GAMEWEEK_CSVS_DIR = '/Users/fincooney/fpl2/player_stats_2425/gws' # Make sure this matches your folder structure!

# Path for the combined output CSV file
COMBINED_DATA_PATH = 'fpl_gameweek_data_2024-25_raw.csv'

# --- Step 1: Find all CSV files in the specified directory ---
# glob.glob() finds all files matching a pattern
csv_files = glob.glob(os.path.join(GAMEWEEK_CSVS_DIR, '*.csv'))

if not csv_files:
    print(f"ERROR: No CSV files found in '{GAMEWEEK_CSVS_DIR}'.")
    print("Please ensure the path is correct and the folder contains .csv files.")
    print("Example correct path: 'data/2024-25/gws'")
    exit()

print(f"Found {len(csv_files)} gameweek CSV files to combine.")

# --- Step 2: Read each CSV and store them in a list of DataFrames ---
all_dfs = []
for file_path in csv_files:
    try:
        # pd.read_csv reads a CSV file into a DataFrame
        df_gw = pd.read_csv(file_path)
        all_dfs.append(df_gw)
        print(f" - Read {os.path.basename(file_path)}")
    except Exception as e:
        print(f"ERROR: Could not read {file_path}: {e}. Skipping this file.")

if not all_dfs:
    print("No DataFrames were successfully loaded. Exiting.")
    exit()

# --- Step 3: Concatenate all DataFrames into a single one ---
# pd.concat stacks DataFrames on top of each other
combined_df = pd.concat(all_dfs, ignore_index=True)

print(f"\nSuccessfully combined {len(all_dfs)} gameweek files into a single DataFrame.")
print(f"Total rows in combined DataFrame: {combined_df.shape[0]}")
print(f"Total columns in combined DataFrame: {combined_df.shape[1]}")

# --- Step 4: Initial Inspection of Combined Data ---
print("\n--- Combined Data Head (first 5 rows): ---")
print(combined_df.head())

print("\n--- Combined Data Info (overview): ---")
combined_df.info()

# --- Step 5: Save the combined data to a new CSV file ---
combined_df.to_csv(COMBINED_DATA_PATH, index=False)
print(f"\n✅ Combined raw gameweek data saved to '{COMBINED_DATA_PATH}'")

