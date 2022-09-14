from sqlalchemy import *
from .db_base import Base

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

    def set_final(self, home_team_score, away_team_score):
        self.final = True 
        self.away_score = away_team_score
        self.home_score = home_team_score

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