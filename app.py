from flask import Flask, redirect, render_template, request, session
from dotenv import load_dotenv
import os
from google.oauth2 import credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from api import fetch_season_data, get_season_info, add_event_user_calendar

app = Flask("Cycling calendar")

# load the .env file from the dir, wich contain the client id and passwrd to request the token
load_dotenv()


app = Flask("Cycling calendar")

# import the sport radar key from the .env file 
api_key = os.getenv("api_key")
app.secret_key = os.getenv("APP_SECRET_KEY")

GOOGLE_ID = os.getenv("GOOGLE_ID")
GOOGLE_SECRET = os.getenv("GOOGLE_SECRET")

# set the language_code TODO: set language selection
language_code = "en"

MEN_2023_SEASON_ID = "sr:stage:1023889"

events = fetch_season_data(MEN_2023_SEASON_ID, api_key)

# google set up
flow = Flow.from_client_secrets_file(
        'google_info/client_secrets.json',
        scopes=['openid',  'https://www.googleapis.com/auth/calendar.events'],)

flow.redirect_uri = 'https://127.0.0.1:5000'

print(flow)

@app.route('/')
def home():
    # if there is a response from google, add info to user calendar
    if 'code' in request.args:
        authorization_response = request.url
        flow.fetch_token(authorization_response=authorization_response)

        credentials = flow.credentials

        
        add_event_user_calendar(credentials)
        

    return render_template("index.html", events=events)



@app.route('/authorize')
def authorize():
    
    auth_uri, state = flow.authorization_url(access_type='offline', 
                        include_granted_scopes='true')

    return redirect(auth_uri)


if __name__ == "__main__":
    app.run(ssl_context='adhoc')
