from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db_base import Base
from nfl_matchup_model import NFLTeam

engine = create_engine("sqlite:///main.db", echo=True, future = True)

Base.metadata.create_all(engine)

with Session(engine) as session:
    game1 = NFLTeam(
        away_team = "test",
        home_team = "woot"
    )

    session.add_all([game1])
    session.commit()