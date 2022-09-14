from .nfl_database import NFLDatabase
from .nfl_matchup_model import NFLMatchModel
from sqlalchemy.orm import Session

class NFLMatchupDao():
    def __init__(self, database: NFLDatabase):
        self.db = database

    def update_match(self, match: NFLMatchModel):
        pass

    def add_matches(self, matches: [NFLMatchModel]):
        with Session(self.db.engine) as session:
            session.add_all(matches)
            session.commit()