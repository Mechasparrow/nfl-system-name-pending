from sqlalchemy import *
from .db_base import Base

import sys
sys.path.append('..')

from nfl_matchup import NFLMatchup

class NFLMatchModel(Base):
    __tablename__ = "nfl_match"

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    week = Column(Integer)
    away_team = Column(String(30))
    away_score = Column(Integer)
    home_team = Column(String(30))
    home_score = Column(Integer)
    date = Column(Date)
    time = Column(Time)
    final = Column(Boolean)

    def parse_from_scrape_model(matchup: NFLMatchup):
        return NFLMatchModel(
            year = matchup.year,
            week = matchup.week,
            away_team = matchup.away_team,
            away_score = matchup.away_team_score,
            home_team = matchup.home_team,
            home_score = matchup.home_team_score,
            date = matchup.date,
            time = matchup.time,
            final = matchup.final
        )

    def __str__(self):
        return f'''
        Year: {self.year}
        Week: {self.week}
        Away Team: {self.away_team} Score: {self.away_score}
        Home Team: {self.home_team} Score: {self.home_score}
        Date: {self.date}
        Time: {self.time}
        Final: {self.final}
        '''