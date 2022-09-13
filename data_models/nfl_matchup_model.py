from sqlalchemy import *
from db_base import Base

class NFLMatchModel(Base):
    __tablename__ = "nfl_match"

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    week = Column(Integer)
    away_team = Column(String(30))
    home_team = Column(String(30))
    date = Column(Date)
    time = Column(Time)