import requests
from bs4 import BeautifulSoup
import json
from nfl_matchup import NFLMatchup
from datetime import datetime, time
import re

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

def get_date(year, section_date):
    sanitized_section_date = re.sub(r'(\d)(st|nd|rd|th)', r'\1', section_date)
    sanitized_section_date = sanitized_section_date.replace(",", "")

    if ("not yet" in section_date):
        return None

    dt = datetime.strptime(f"{year} {sanitized_section_date}", "%Y %A %B %d").date()
    return dt

def get_team_soups(matchup_soup):
    matchup_teams_soup = matchup_soup.find(class_ = "nfl-c-matchup-strip__game").find_all(class_ = "nfl-c-matchup-strip__team")
    return matchup_teams_soup

def find_team_name(team_soup):
    return team_soup.find(class_="nfl-c-matchup-strip__team-name").find(class_="nfl-c-matchup-strip__team-fullname").text.strip()

def get_matchup_final_score(team_soup):
    team_score_elem = team_soup.find(class_ = "nfl-c-matchup-strip__team-score")

    if (team_score_elem != None):
        return int(team_score_elem.get("data-score"))
    else:
        return None

def get_matchup_teams(matchup_soup):
    matchup_team_names = list(map(lambda matchup_team: find_team_name(matchup_team), get_team_soups(matchup_soup)))
    return (matchup_team_names[0], matchup_team_names[1])

def get_matchup_team_scores(matchup_soup):
    matchup_team_scores = list(map(lambda team_soup: get_matchup_final_score(team_soup), get_team_soups(matchup_soup)))

    return (matchup_team_scores[0], matchup_team_scores[1])

def get_matchup_time(matchup_soup):
    matchup_time_details = matchup_soup.find(class_ = "nfl-c-matchup-strip__date-time")
    matchup_time = None
    if (matchup_time_details != None):
        matchup_time = matchup_time_details.text.strip()
        
        return datetime.strptime(matchup_time, "%I:%M %p").time()

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

def get_nfl_matchups(nfl_json_soup):
    data_json_raw = nfl_json_soup.find("div").get('data-json-module')
    matchup_json = json.loads(data_json_raw)
    matchup_year = matchup_json["Module"]["seasonFromUrl"]
    nfl_matchup_list = []

    nfl_sections = get_nfl_section_information(nfl_json_soup)

    for (section_date, matchups) in nfl_sections:
        for matchup in matchups:
            matchup_time = get_matchup_time(matchup)
            away_team, home_team = get_matchup_teams(matchup)

            nfl_date = get_date(matchup_year, section_date)
            nfl_matchup = NFLMatchup(matchup_year, nfl_date, matchup_time, home_team, away_team)
            
            away_team_score, home_team_score = get_matchup_team_scores(matchup)

            if (away_team_score != None and home_team_score != None):
                nfl_matchup.set_final(home_team_score, away_team_score)

            nfl_matchup_list.append(nfl_matchup)
    
    return nfl_matchup_list
