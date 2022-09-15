from .nfl_database import NFLDatabase
from .nfl_matchup_model import NFLMatchModel
from sqlalchemy.orm import Session

class NFLMatchupDao():
    def __init__(self, database: NFLDatabase):
        self.db = database

    def upsert_match(self, match: NFLMatchModel):
        perform_create = False

        with Session(self.db.engine) as session:
            potential_duplicates = session.query(NFLMatchModel) \
                .filter(NFLMatchModel.year == match.year) \
                .filter(NFLMatchModel.week == match.week) \
                .filter(NFLMatchModel.away_team == match.away_team) \
                .filter(NFLMatchModel.home_team == match.home_team) \
                .all()

            if len(potential_duplicates) > 0:
                update_payload = {
                    "final": match.final, 
                    "away_score": match.away_score, 
                    "home_score": match.home_score,
                    "date": match.date,
                    "time": match.time
                }
                
                session.query(NFLMatchModel) \
                    .filter(NFLMatchModel.week == match.week) \
                    .filter(NFLMatchModel.away_team == match.away_team) \
                    .filter(NFLMatchModel.home_team == match.home_team) \
                    .update(update_payload, synchronize_session="fetch")
            else:
                perform_create = True    

            session.commit()

        if (perform_create):
            self.add_match(match)

    def add_match(self, match: NFLMatchModel):
        with Session(self.db.engine) as session:
            session.add(match)
            session.commit()

    def add_matches(self, matches: [NFLMatchModel]):
        with Session(self.db.engine) as session:
            session.add_all(matches)
            session.commit()