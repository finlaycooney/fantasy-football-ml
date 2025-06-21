# fantasy-football-ml
A data-driven machine learning project to predict player performance and optimize squad selection for Fantasy Premier League (FPL).

**FPL AI Predictor**
A data-driven machine learning project to predict player performance and optimize squad selection for Fantasy Premier League (FPL). This repository contains the full pipeline, from data acquisition and cleaning to feature engineering and model training, with the ultimate goal of achieving a top-tier rank.

**🎯 Project Goal**
The primary objective of this project is to move beyond simple heuristics and use a robust data pipeline to build a predictive model for FPL player points. The model's predictions are then fed into a linear optimization algorithm to select the optimal 15-player squad for the upcoming gameweek, respecting all budget and formation constraints.

**✨ Features**
- **Automated Data Pipeline:** Scripts to fetch, clean, and process multiple seasons of detailed, gameweek-level player data.
- **Advanced Feature Engineering:** Generates insightful features like rolling performance averages (form), points-per-million (value), and a "points_next_gameweek" target variable.
- **Predictive Modeling:** Ready for a machine learning model (e.g., XGBoost) to be trained on the engineered features to predict future performance.
- **Squad Optimization:** A framework to use the model's predictions to solve the "knapsack problem" of selecting the highest-scoring squad within the £100m budget.

**🛠️ The Data Pipeline**
The project is structured as a sequential data pipeline, where each script is responsible for one stage of the process.
1. **Data Acquisition (get_gameweek_data.py)**
- Loads a summary file of all players for a given season.
- Iterates through each player, constructs a unique API endpoint URL for their detailed history.
- Scrapes the gameweek-by-gameweek data for every player.Combines all data into a single raw output file (fpl_gameweek_data_all_players.csv).

2. **Data Cleaning (clean_data.py)Loads the raw gameweek data.**
- Removes unnecessary columns, corrects data types, and fills missing values.
- Filters out inactive players to reduce noise.
- Saves a clean, reliable dataset (fpl_data_cleaned.csv).

3. **Feature Engineering (feature_engineering.py)**
- Loads the clean dataset.
- Sorts data chronologically by player and gameweek.
- Creates the crucial points_next_gameweek target variable.
- Calculates rolling averages for key stats (points, minutes, goals, assists, etc.) to model player form.
- Saves the final, feature-rich dataset ready for modeling (fpl_model_ready_data.csv).

**🚀 How to Use**
To run this project, follow the steps in order.

**1. Clone the repository:**

git clone https://github.com/finlaycooney/fpl-ai-predictor.git
cd fpl-ai-predictor

**2. Set up the environment:**

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt 

_(Note: You will need to create a requirements.txt file containing pandas, requests, etc.)Run the pipeline:python get_gameweek_data.py
python clean_data.py_

python feature_engineering.py
After these steps, fpl_model_ready_data.csv will be available for you to train a model with.

**💻 Tech Stack**
- **Language:** Python
- **Data Manipulation:** Pandas
- **Web Scraping:** Requests
- **Future Modeling:** Scikit-learn, XGBoostFuture
- **Optimization:** PuLP
















