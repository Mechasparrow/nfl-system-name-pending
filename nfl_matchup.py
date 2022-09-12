class NFLMatchup():
    def __init__(self, year, date, time, home_team, away_team):
        self.year = year 
        self.date = date
        self.time = time
        self.home_team = home_team
        self.away_team = away_team
    
    def __str__(self):
        if (self.time != None):
            return f'{self.year}, {self.date}, {self.time}: {self.away_team} @ {self.home_team}'
        return f'{self.year}, {self.date}: {self.away_team} @ {self.home_team}'