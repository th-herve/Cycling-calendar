from flask import Flask, render_template, redirect, request, url_for
import requests
from dotenv import load_dotenv
import os
import json

from api import fetch_season_data, retrive_race_data

# load the .env file from the dir, wich contain the client id and passwrd to request the token
load_dotenv()


app = Flask("Cycling calendar")

# import the sport radar key from the .env file 
api_key = os.getenv("api_key")


# set the language_code TODO: set language selection
language_code = "en"

MEN_2023_SEASON_ID = "sr:stage:1023889"

events = fetch_season_data(MEN_2023_SEASON_ID, api_key)

@app.route('/')
def home():
    return render_template("index.html", events=events)

@app.route('/race_data/<stage_id>')
def race_data(stage_id):
    data = retrive_race_data(stage_id)
    return data

# app.run(debug=True)
