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



def find_team_name(team_soup):
    return team_soup.find(class_="nfl-c-matchup-strip__team-name").find(class_="nfl-c-matchup-strip__team-fullname").text.strip()

def get_matchup_teams(matchup_soup):
    matchup_teams_soup = matchup_soup.find(class_ = "nfl-c-matchup-strip__game").find_all(class_ = "nfl-c-matchup-strip__team")
    matchup_team_names = list(map(lambda name: find_team_name(name), matchup_teams_soup))
    return (matchup_team_names[0], matchup_team_names[1])

def get_matchup_time(matchup_soup):
    matchup_time_details = matchup_soup.find(class_ = "nfl-c-matchup-strip__date-time")
    matchup_time = None
    if (matchup_time_details != None):
        matchup_time = matchup_time_details.text.strip()

    return matchup_time 

def get_nfl_section_information(nfl_json_soup):
    nfl_json_sections = nfl_json_soup.find_all(class_ = "nfl-o-matchup-group")
    
    section_information_list = []

    for section in nfl_json_sections:
        section_date = section.find(class_ = "d3-o-section-title").text
        matchups = section.find_all(class_ = "nfl-c-matchup-strip")

        section_detail = (section_date, matchups)
        section_information_list.append(section_detail)

    return section_information_list

def get_nfl_matchups(year, nfl_json_soup):
    nfl_matchup_list = []

    nfl_sections = get_nfl_section_information(nfl_json_soup)

    for (section_date, matchups) in nfl_sections:
        for matchup in matchups:
            matchup_time = get_matchup_time(matchup)
            away_team, home_team = get_matchup_teams(matchup)
            
            nfl_matchup = NFLMatchup(year, section_date, matchup_time, home_team, away_team)
            
            nfl_matchup_list.append(nfl_matchup)
    
    return nfl_matchup_list
