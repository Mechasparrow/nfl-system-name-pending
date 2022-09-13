from matchup_parser import *

# 1..18
week_count = 18
nfl_weeks = list(range(1,week_count+1))

for week in nfl_weeks:
    nfl_matchups = get_nfl_matchups(get_nfl_soup(2022,week))

    print(f"Week {week}")
    for matchup in nfl_matchups:
        print(matchup)