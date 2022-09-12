from sqlalchemy import *
from db_base import Base

class NFLTeam(Base):
    __tablename__ = "nfl_team"

    id = Column(Integer, primary_key=True)
    away_team = Column(String(30))
    home_team = Column(String(30))
    