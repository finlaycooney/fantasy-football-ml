Phase 1  

What are we aiming for here?
want total points per gameweek

best metric - points per million
trying to predict points per million 

Key Technologies: Python, Pandas, Scikit-learn, Requests, PuLP.




Phase 2

You need good data. The most crucial source is the official FPL API.

Endpoint: https://fantasy.premierleague.com/api/bootstrap-static/

What it contains: A massive JSON file with player info (points, cost, team, position), team data, and gameweek data.

-  Betting odds are a good idea
- clean sheet predictor for each defender
- anytime goal scorer predictor for each forward or midfielder

Other useful metrics:
- xG
- xA
- xGChain
- xGBuildup
- xGProgression
- xGProgressionChain
- xGProgressionBuildup
- xGProgressionProgression
- xGProgressionProgressionChain
- xGProgressionProgressionBuildup



i may run into trouble further down the line as my data probably needs to be clearer. there will be NANs and other things in some collumns. 

two options - start developing features and move into the science of the data and sort the NANs after 

- clean the data now and then develope features 




feature 
- we have the first five fixtures of the premier league so want to optimize for these five games 
- if we compare each set of players from a team with their opposing fixture in the first five games and compare that to form at the end of last season and how they played against them last time too.

