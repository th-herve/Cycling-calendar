# from typing import NotRequired
from typing import final
from dotenv import load_dotenv, main
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


# return the season_data either from cache or api request                   source: indently (yt), Caching your api requests 
def fetch_season_data(season_id, year = "2023", language_code = "en", update: bool = False):

    # all seasons cache file should follow this naming convention 
    formated_id = season_id.replace(":","")
    season_cache = "data/" + formated_id + ".json"

    if update:
        season_data = None
    else:
        try:
            with open(season_cache, 'r') as file:
                season_data = json.load(file)
                print("fetched data from local cache")
        except(FileNotFoundError, json.JSONDecodeError):
            print("No local cache found") 
            season_data = None

    if not season_data:
        print("Fetching new local data, with api request")
        # make api request, if it fails, it will return none and the backup will be use instead
        season_data = get_season_info(season_id, year, language_code) 

        if not season_data:
            backup = "data/backup_srstage1023889.json"
            with open(backup,'r') as file:
                season_data = json.load(file)
        
        else:
            # write the request in the json cache file, if it is not from the backup
            with open(season_cache, 'w') as file:
                json.dump(season_data, file)


    return format_season_info(season_data, year)




# api call to get the info of a given season
def get_season_info(season_id, api_key = api_key, year = "2023", language_code = "en"):
    url = "https://api.sportradar.us/cycling/trial/v2"
    langue = language_code 
    season = season_id
    key = api_key

    final_url = f"{url}/{langue}/sport_events/{season}/schedule.json?api_key={key}" 

    print(final_url)
    # try to retrive the api
    try:
        result = get(final_url)
        print(result)
        json_result = json.loads(result.content)
    except:
        print("error: could not retrieve api, fetching from backup instead")

        json_result = None

    return json_result


# take a season as arg and return a list of dict with each race and their info, formated to be use in fullcalendar
def format_season_info(season,year):
    races_info = []

    for race in season["stages"][0]["stages"]:
        id = race["id"]
        description = race["description"]
        date = format_dateTime_to_time(race["scheduled"]) 
        single_event = race["single_event"] # boolean
        # scheduled_end = race["scheduled_end"]
        
        # key must be readable by fullcalendar (not really but I think it's better)
        race_detail = {
                    "id" : id, 
                    "title" : description,  # title of the event in calendar
                    "date" : date,
                    "backgroundColor" : "green",
                    "single_event" : single_event
                     }

        # add the stages if not a single event race in a list
        if single_event == False:
            try:
                race_detail["stages"] = []
                for stage in race["stages"]:
                    stage_id = stage["id"]
                    stage_description =  stage["description"]
                    stage_date = format_dateTime_to_time(stage["scheduled"]) 

                    stage_detail = {
                            "id" : stage_id, 
                            "title": description +" "+ stage_description, 
                            "date" : stage_date,
                            }
                    race_detail["stages"].append(stage_detail)
            # some races do not have stages entry even though they should (problem from the api provider)
            except:
                print(f"no stages detail for {description}")

                

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

# data = fetch_season_data(MEN_2023_SEASON_ID)
# print(data)
