from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db_base import Base
from nfl_matchup_model import NFLTeam

class NFLDatabase():
    def __init__(self, db_name):
        self.engine = create_engine(f"sqlite:///{db_name}", future = True)
        Base.metadata.create_all(self.engine)

    