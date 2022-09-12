import requests
from bs4 import BeautifulSoup
import json
from nfl_matchup import NFLMatchup

def get_nfl_soup(year, week):
    json_template_str = "https://www.nfl.com/api/lazy/load?json="

    nfl_json = {
        "Name":"Schedules",
        "Module":{
            "seasonFromUrl":year,
            "SeasonType":f"REG{week}",
            "WeekFromUrl":week,
            "HeaderCountryCode":"US",
            "PreSeasonPlacement":0,
            "RegularSeasonPlacement":0,
            "PostSeasonPlacement":0,
            "TimeZoneID":"America/Chicago"
        }
    }

    nfl_json_api_url = f'{json_template_str}{json.dumps(nfl_json)}'

    nfl_json_response = requests.get(nfl_json_api_url)
    return BeautifulSoup(nfl_json_response.text, 'html.parser')

def get_nfl_matchups(year, nfl_json_soup):

    nfl_json_sections = nfl_json_soup.find_all(class_ = "nfl-o-matchup-group")

    nfl_matchup_list = []

    for section in nfl_json_sections:
        section_title = section.find(class_ = "d3-o-section-title")
        section_date = section_title.text
        matchups = section.find_all(class_ = "nfl-c-matchup-strip")
        
        for matchup in matchups:
            matchup_details = matchup.find(class_ = "nfl-c-matchup-strip__game")
            matchup_teams_soup = matchup_details.find_all(class_ = "nfl-c-matchup-strip__team")
            find_team_name = lambda team_soup: team_soup.find(class_="nfl-c-matchup-strip__team-name").find(class_="nfl-c-matchup-strip__team-fullname").text
            matchup_team_names = list(map(lambda name: find_team_name(name).strip(), matchup_teams_soup))
            away_team = matchup_team_names[0]
            home_team = matchup_team_names[1]
            
            matchup_time_details = matchup.find(class_ = "nfl-c-matchup-strip__date-time")

            matchup_time = None

            if (matchup_time_details != None):
                matchup_time = matchup_time_details.text.strip()

            nfl_matchup = NFLMatchup(year, section_date, matchup_time, home_team, away_team)
            nfl_matchup_list.append(nfl_matchup)
    
    return nfl_matchup_list