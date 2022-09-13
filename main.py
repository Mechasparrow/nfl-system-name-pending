from matchup_parser import *
from data_models.nfl_matchup_model import NFLMatchModel
from data_models.nfl_database import NFLDatabase

from sqlalchemy.orm import Session

# 1..18
week_count = 18
nfl_weeks = list(range(1,week_count+1))

database = NFLDatabase("nfldb.db")

matchups_to_index = []

for week in nfl_weeks:
    nfl_matchups = get_nfl_matchups(get_nfl_soup(2022,week))

    print(f"Week {week}")
    for matchup in nfl_matchups:
        mod = NFLMatchModel.parse_from_scrape_model(matchup)
        matchups_to_index.append(mod)

with Session(database.engine) as session:
    session.add_all(matchups_to_index)
    session.commit()