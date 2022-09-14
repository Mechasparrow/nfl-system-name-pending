from matchup_parser import *
from data_models.nfl_database import NFLDatabase
from data_models.nfl_matchup_model import NFLMatchModel
from data_models.nfl_matchup_dao import NFLMatchupDao

from concurrent.futures import ThreadPoolExecutor, as_completed
futureSession = FuturesSession(executor=ThreadPoolExecutor(max_workers=10))

# 1..18
week_count = 18
nfl_weeks = list(range(1,week_count+1))
matchups_to_index: [NFLMatchModel] = []
nfl_reqs = []

for week in nfl_weeks:
    nfl_matchup_request = make_nfl_request(2022, week, future_session=futureSession)
    nfl_matchup_request.week = week
    nfl_reqs.append(nfl_matchup_request)

weeks_added = 0
for nfl_req in as_completed(nfl_reqs):
    real_nfl_req: requests.Response = nfl_req.result()
    week = nfl_req.week 
    nfl_soup = get_nfl_soup_from_request(real_nfl_req)
    nfl_matchups = get_nfl_matchups(nfl_soup)
    matchups_to_index += nfl_matchups
    weeks_added += 1

database = NFLDatabase("nfldb.db")
match_dao = NFLMatchupDao(database)
match_dao.add_matches(matchups_to_index)

print(f"{weeks_added} NFL weeks updated in database")