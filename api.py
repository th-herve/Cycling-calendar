from dotenv import load_dotenv
import os
from requests import get
import json
from datetime import datetime
from googleapiclient.discovery import build

load_dotenv()
api_key = os.getenv("api_key")

# set the language_code TODO: set language selection
language_code = "en"

MEN_2023_SEASON_ID = "sr:stage:1023889"


# ╔═══════════════════════════════╗
# ║          Season info          ║
# ╚═══════════════════════════════╝

# return the season_data either from cache or api request                       source: indently (yt), Caching your api requests 
def fetch_season_data(event_id, year = "2023", language_code = "en", update: bool = False):
    # all seasons cache file should follow this naming convention 
    formated_id = event_id.replace(":","")
    event_cache_json = "data/" + formated_id + ".json"

    if update:
        event_data = None
    else:
        event_data = get_json_data(event_cache_json)

    if not event_data:
        print("Fetching new event local data, with api request")
        # make api request, if it fails, it will return none and the backup will be used instead
        event_data = event_api_request(event_id,'season', year, language_code) 

        if not event_data:
            backup = "data/backup_srstage1023889.json"
            event_data = get_json_data(backup)
        
        else:
            # write the request in the json cache file, if it is not from the backup
            write_data_in_json(event_cache_json, event_data)

    return event_data

# take a season as arg and return a list of dict with each race and their info
def format_season_info(season):
    races_info = []

    for race in season["stages"][0]["stages"]:
        race_detail = {
                    "id" : race["id"], 
                    "title" : race["description"],  # title of the event in calendar
                    "date" : format_dateTime_to_time(race["scheduled"]),
                    "backgroundColor" : "green",
                    "single_event" : race["single_event"]
                     }

        # add the stages if any
        if not race["single_event"]: 
            id = race["id"];
            try:
                race_detail["stages"] = []
                for stage in race["stages"]:
                    stage_detail = {
                            "id" : stage["id"],
                            "title": race["description"] +" "+ stage["description"], 
                            "date" : format_dateTime_to_time(stage["scheduled"]),
                            "backgroundColor" : "#ED6F92" if id == "sr:stage:1052217"           # pink bg for the Giro 
                                                else ("#e8c713" if id == "sr:stage:1023895"     # yellow bg for the Tour De France
                                                else ( "#ff0000" if id == "sr:stage:1052491"    # red bg for the Vuelta
                                                else "green"))                                  
                            }

                    race_detail["stages"].append(stage_detail)


            # some races do not have stages entry even though they should (problem from the api provider)
            except:
                print(f"no stages detail for {race['description']} or failed to retrive it")
        
        races_info.append(race_detail)

    # write the content in a json
    write_data_in_json("data/formated_season.json", races_info) 

    return races_info 

# ╔═══════════════════════════════╗
# ║          Race info            ║
# ╚═══════════════════════════════╝

# find if a given stage is in the json database, if not create an entry by making an api request
def retrive_race_data(stage_id, update=False):
    stages_cache_file = "data/json_stages/stages.json"

    json_stages_data = get_json_data(stages_cache_file)

    if stage_id in json_stages_data and not update:
        return json_stages_data[stage_id]
    else:
        print("stages not in json file, requesting new data")
        stage_info = event_api_request(stage_id, 'race')

        json_stages_data = update_stages_cache_json(stages_cache_file, json_stages_data, stage_info, stage_id)

        return json_stages_data[stage_id]
        
# add an entry to the stages cache file
def update_stages_cache_json(stages_cache_file, json_stages_data, stage_info, stage_id):
    json_stages_data[stage_id] = {
            "description": stage_info["stage"].get("description", "Undefined"), 
            "scheduled": stage_info["stage"].get("scheduled", "Undefined"), 
            "distance": stage_info["stage"].get("distance", "Undefined"), 
            "departure_city": stage_info["stage"].get("departure_city", "Undefined"), 
            "arrival_city": stage_info["stage"].get("arrival_city", "Undefined"), 
            "classification": stage_info["stage"].get("classification", "Undefined"), 
            "single_event": stage_info["stage"].get("single_event", "Undefined"), 
            }
    write_data_in_json(stages_cache_file, json_stages_data)
    return json_stages_data

# ╔═══════════════════════════════╗
# ║          Api request          ║
# ╚═══════════════════════════════╝

# api call to get the info of a given season
def event_api_request(event_id, event_type, api_key = api_key, year = "2023", language_code = "en"):
    url = "https://api.sportradar.us/cycling/trial/v2"

    if event_type == 'season':
        type_code = 'schedule'
    elif event_type == 'race':
        type_code = 'summary'

    final_url = f"{url}/{language_code}/sport_events/{event_id}/{type_code}.json?api_key={api_key}" 

    # try to retrive the api
    try:
        result = get(final_url)
        json_result = json.loads(result.content)
    except:
        print('api request failed')
        json_result = None

    return json_result
        

# ╔═══════════════════════════════╗
# ║  Google calendar integration  ║
# ╚═══════════════════════════════╝

# add all races to the user calendar
def add_event_user_calendar(credentials, season_data):
    service = build('calendar','v3',credentials=credentials)

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
            # special color are apply for the giro, tour de france, and vuelta (the if statements are in this order)
            id = race['id']
            for stage in race["stages"]:
                stage_info = {
                    'summary': stage["title"],
                    'start': { 'date': stage["date"] },
                    'end': { 'date': stage["date"] },
                    "colorId" : 4 if id == "sr:stage:1052217" 
                                else (5 if id == "sr:stage:1023895" 
                                else ( 11 if id == "sr:stage:1052491" 
                                else 10)),
                    } 
                try:
                    service.events().insert(calendarId='primary', body=stage_info).execute()
                    # print(f"added {stage['title']}")
                except:
                    print(f"failed to add {stage['title']}")


# ╔═══════════════════════════════╗
# ║           Utilities           ║
# ╚═══════════════════════════════╝

# take a datetime format and convert it to just date
def format_dateTime_to_time(date_time):
    date_time_object = datetime.fromisoformat(date_time) 

    date_only = date_time_object.date()
    date_only_string = date_only.isoformat()

    return date_only_string

def get_json_data(json_file):
    try:
        with open(json_file,'r') as file:
            return json.load(file)
    except(FileNotFoundError, json.JSONDecodeError):
        return None

def write_data_in_json(json_file, data):
    with open(json_file, 'w') as file:
        json.dump(data, file)


# events = fetch_season_data(MEN_2023_SEASON_ID, api_key)
# data = format_season_info(events)
