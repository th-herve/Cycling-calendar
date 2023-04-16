from flask import Flask, render_template
from dotenv import load_dotenv
import os

from api import get_season_info 

app = Flask("Cycling calendar")

# load the .env file from the dir, wich contain the client id and passwrd to request the token
load_dotenv()

# import the key from the .env file 
api_key = os.getenv("api_key")


# set the language_code TODO: set language selection
language_code = "en"

MEN_2023_SEASON_ID = "sr:stage:1023889"

events = get_season_info(language_code,MEN_2023_SEASON_ID,api_key)
# print(races_info_2023)


@app.route('/')
def home():

    return render_template("index.html", events=events)
