from matchup_parser import *

# 1..18
week_count = 18
nfl_weeks = list(range(1,week_count+1))

nfl_matchups = get_nfl_matchups(get_nfl_soup(2021,1))

for matchup in nfl_matchups:
    print(matchup)