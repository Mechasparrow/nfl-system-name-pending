from .nfl_database import NFLDatabase
from .nfl_matchup_model import NFLMatchModel

class NFLMatchupDao():
    def __init__(self, database: NFLDatabase):
        self.db = database

    def update_match(self, match: NFLMatchModel):
        pass

    def add_match(self, match: NFLMatchModel):
        pass
    