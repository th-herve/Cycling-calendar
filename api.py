# from typing import NotRequired
from typing import final
from dotenv import load_dotenv, main
import os
from requests import post, get
import json
from datetime import datetime
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import BatchHttpRequest
from googleapiclient.errors import HttpError


# load the .env file from the dir, wich contain the client id and passwrd to request the token
load_dotenv()

# import the key from the .env file 
api_key = os.getenv("api_key")
# set the language_code TODO: set language selection
language_code = "en"

MEN_2023_SEASON_ID = "sr:stage:1023889"


# ╔═════════ Season info ═════════╗

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
                print("fetched season data from local cache")
        except(FileNotFoundError, json.JSONDecodeError):
            print("No season local cache found") 
            season_data = None

    if not season_data:
        print("Fetching new season local data, with api request")
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


    return format_season_info(season_data)




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
def format_season_info(season):
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

                    # special color are apply for the giro, tour de france, and vuelta (the ifs statement are in this order)
                    stage_detail = {
                            "id" : stage_id, 
                            "title": description +" "+ stage_description, 
                            "date" : stage_date,
                            "backgroundColor" : "#ED6F92" if id == "sr:stage:1052217" else ("#e8c713" if id == "sr:stage:1023895" else ( "#ff0000" if id == "sr:stage:1052491" else "green")) 
                            }

                    race_detail["stages"].append(stage_detail)


            # some races do not have stages entry even though they should (problem from the api provider)
            except:
                print(f"no stages detail for {description}")

                

        races_info.append(race_detail)

    return races_info 


# ╔═════════ Race info ═════════╗

# fetch race or stage data either from local cache or api request
def fetch_race_data(stage_id, year = "2023", language_code = "en", update: bool = False):

    # all stage cache file should follow this naming convention 
    formated_id = stage_id.replace(":","")
    stage_cache = "data/race/" + formated_id + ".json"

    # if update true, an api request will be execute
    if update:
        stage_data = None
    else:
        try:
            with open(stage_cache, 'r') as file:
                stage_data = json.load(file)
                print("fetched race data from local cache")
        except(FileNotFoundError, json.JSONDecodeError):
            print("No race local cache found") 
            stage_data = None

    if not stage_data:
        print("Fetching new race local data, with api request")
        # make api request, if it fails, it will return none and the backup will be use instead
        stage_data = get_race_info(stage_id, year=year,language_code=language_code) 

        if not stage_data:
            print("Api request failed")
            stage_data = None
        
        else:
            # write the request in the json cache file, if it is not from the backup
            with open(stage_cache, 'w') as file:
                json.dump(stage_data, file)


    return stage_data

# api request that return detail about a race or stage
def get_race_info(stage_id, api_key = api_key, year = "2023", language_code = "en"):
    url = "https://api.sportradar.us/cycling/trial/v2"
    langue = language_code 
    stage = stage_id
    key = api_key
    
    final_url = f"{url}/{langue}/sport_events/{stage}/summary.json?api_key={key}" 

    result = get(final_url)
    json_result = json.loads(result.content)

    return json_result 

def format_race_info(race_json):
    race_info = []

    for race in race_json["stages"][0]["stages"]:
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
                    "single_event" : single_event
                     }

# find if a given stage is in the json database, if not create an entry by making an api request
def retrive_race_data(stage_id, update=False):
    # all stage cache file should follow this naming convention 
    json_stages_file = "data/json_stages/stages.json"

    # open the data file
    with open(json_stages_file,'r') as file:
        try:
            json_stages_data = json.load(file)
        except:
            print("no data in json file")
            # json_stages_data = {}
        
        # check if the given stage is in the json file
        try:
            requested_stage_info = json_stages_data[stage_id]
        except:
            print("stages not in json file, requesting new data")
            requested_stage_info = None
    
    # if the stage is not in the file, an api request is made and the file is updated with the new data
    if requested_stage_info == None or update == True:
        print("api request for stage")
        stage_info = get_race_info(stage_id)

        json_stages_data[stage_id] = {
                "description": stage_info["stage"].get("description", "Undefined"), 
                "scheduled": stage_info["stage"].get("scheduled", "Undefined"), 
                "distance": stage_info["stage"].get("distance", "Undefined"), 
                "departure_city": stage_info["stage"].get("departure_city", "Undefined"), 
                "arrival_city": stage_info["stage"].get("arrival_city", "Undefined"), 
                "classification": stage_info["stage"].get("classification", "Undefined"), 
                "single_event": stage_info["stage"].get("single_event", "Undefined"), 
                }
        requested_stage_info = json_stages_data[stage_id]

        with open(json_stages_file, 'w') as file:
            json.dump(json_stages_data, file)
        

    return requested_stage_info

# ╔═════════ Google functionality ═════════╗

# add all races to the user calendar
def add_event_user_calendar(credentials):

    service = build('calendar','v3',credentials=credentials)

    # get the season races
    season_data = fetch_season_data(MEN_2023_SEASON_ID)


    for race in season_data:
        if race["single_event"]:
            race_info = {
                    'summary': race["title"],
                    'start': { 'date': race["date"] },
                    'end': { 'date': race["date"] },
                    } 
            try:
                service.events().insert(calendarId='primary', body=race_info).execute()
                print(f"added {race['title']}")
            except:
                print(f"failed to add {race['title']}")

        else:
            # special color are apply for the giro, tour de france, and vuelta (the ifs statement are in this order)
            id = race['id']
            for stage in race["stages"]:
                stage_info = {
                    'summary': stage["title"],
                    'start': { 'date': stage["date"] },
                    'end': { 'date': stage["date"] },
                    "colorId" : 4 if id == "sr:stage:1052217" else (5 if id == "sr:stage:1023895" else ( 11 if id == "sr:stage:1052491" else 10)),
                    } 
                try:
                    service.events().insert(calendarId='primary', body=stage_info).execute()
                    print(f"added {stage['title']}")
                except:
                    print(f"failed to add {stage['title']}")



# ╔═════════ Other ═════════╗

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
