class NFLMatchup():
    def __init__(self, year, date, time, home_team, away_team):
        self.year = year 
        self.date = date
        self.time = time
        self.home_team = home_team
        self.away_team = away_team
        self.final = False 
        self.home_team_score = None 
        self.away_team_score = None 

    def set_final(self, home_team_score, away_team_score):
        self.final = True 
        self.home_team_score = home_team_score
        self.away_team_score = away_team_score
    
    def __str__(self):
        timestr = ""
        scorestr = ""

        if (self.time != None):
            timestr = f", {self.time}"

        if (self.final):
            scorestr = f"{self.away_team_score} - {self.home_team_score}"

        return f'{self.year}, {self.date}{timestr}: {self.away_team} @ {self.home_team} {scorestr}'