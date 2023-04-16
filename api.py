from dotenv import load_dotenv
import os
from requests import post, get
import json
from datetime import datetime


# load the .env file from the dir, wich contain the client id and passwrd to request the token
load_dotenv()

# import the key from the .env file 
api_key = os.getenv("api_key")

# set the language_code TODO: set language selection
language_code = "en"

MEN_2023_SEASON_ID = "sr:stage:1023889"


# get the brut info about the season, call the format_race_info() to return formated info
def get_season_info(language_code, season_id, api_key):
    url = "https://api.sportradar.us/cycling/trial/v2"
    langue = language_code 
    season = season_id
    key = api_key

    final_url = f"{url}/{langue}/sport_events/{season}/schedule.json?api_key={key}" 
    result = get(final_url)
    json_result = json.loads(result.content)

    return format_season_info(json_result) 


# take a season as arg and return a list of dict with each race and their info, formated to be use in fullcalendar
def format_season_info(season):
    races_info = []

    for race in season["stages"][0]["stages"]:
        description = race["description"]
        date = format_dateTime_to_time(race["scheduled"]) 
        # scheduled_end = race["scheduled_end"]
        
        # key must be readable by fullcalendar
        race_detail = {
                    "todo":description,
                    "date":date,
                     }

        races_info.append(race_detail)

    return races_info 


# unuse so far, test it but should return detail about a race
def get_race_info(language_code, stage_id, api_key):
    url = "https://api.sportradar.com/cycling/trial/v2"
    langue = language_code 
    stage = stage_id
    key = api_key
    
    final_url = f"{url}/{langue}/sport_events/{stage}/summary.json?api_key={key}" 
    result = get(final_url)
    json_result = json.loads(result.content)
    return json_result 

# take a datetime format and convert it to just date
def format_dateTime_to_time(date_time):
    date_time_object = datetime.fromisoformat(date_time) 

    date_only = date_time_object.date()
    date_only_str = date_only.isoformat()

    return date_only_str



# season_2023 = get_season_info(language_code,MEN_2023_SEASON_ID,api_key)

# races_info_2023 = format_race_info(season_2023) 

