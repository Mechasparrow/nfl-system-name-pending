from matchup_parser import *
from data_models.nfl_matchup_model import NFLMatchModel
from data_models.nfl_database import NFLDatabase

from sqlalchemy.orm import Session

# 1..18
week_count = 18
nfl_weeks = list(range(1,week_count+1))

database = NFLDatabase("nfldb.db")

matchups_to_index = []
nfl_reqs = []

for week in nfl_weeks:
    nfl_matchup_request = make_nfl_request(2022, week)
    print(f"Retrieved Week {week}")
    nfl_reqs.append(nfl_matchup_request)

week = 1
for nfl_req in nfl_reqs:
    nfl_soup = get_nfl_soup_from_request(nfl_req)
    nfl_matchups = get_nfl_matchups(nfl_soup)
    matchups_to_index += nfl_matchups

    print(f"Processed Week {week}")
    week+=1

with Session(database.engine) as session:
    session.add_all(matchups_to_index)
    session.commit()
