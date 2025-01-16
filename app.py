from flask import Flask, redirect, render_template, request, session
from dotenv import load_dotenv
import os
from google_auth_oauthlib.flow import Flow
import threading

from api import (
    fetch_season_data,
    add_event_user_calendar,
    retrive_race_data,
    format_season_info,
)


app = Flask("Cycling calendar")

# .env loading
load_dotenv()
app.secret_key = os.getenv("APP_SECRET_KEY")
GOOGLE_ID = os.getenv("GOOGLE_ID")
GOOGLE_SECRET = os.getenv("GOOGLE_SECRET")

# google set up
flow = Flow.from_client_secrets_file(
    "google_info/client_secrets.json",
    scopes=["openid", "https://www.googleapis.com/auth/calendar.events"],
)

flow.redirect_uri = "https://cycling.th-herve.fr"


# set the language_code TODO: set language selection
language_code = "en"

MEN_2023_SEASON_ID = "sr:stage:1023889"
MEN_2024_SEASON_ID = "sr:stage:1116073"
MEN_2025_SEASON_ID = "sr:stage:1221671"

events = fetch_season_data(MEN_2025_SEASON_ID)
events = format_season_info(events)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        session["events_user_selected"] = request.form.getlist(
            "event_selection_checkbox"
        )
        return redirect("/authorize")

    # if there is a response from google, add info to user calendar
    if "code" in request.args:
        events_user_selected = session["events_user_selected"]
        authorization_response = request.url
        flow.fetch_token(authorization_response=authorization_response)

        credentials = flow.credentials

        # add the event to the user's calendar in a separate thread so it does not interrupt the program
        adding_event_thread = threading.Thread(
            target=add_event_user_calendar,
            args=(credentials, events, events_user_selected),
        )
        adding_event_thread.start()

    return render_template(
        "index.html", events=events, retrive_race_data=retrive_race_data
    )


@app.route("/race_data/<stage_id>")
def race_data(stage_id):
    data = retrive_race_data(stage_id)
    return data


@app.route("/authorize")
def authorize():
    auth_uri, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )

    return redirect(auth_uri)


if __name__ == "__main__":
    app.run(debug=False, ssl_context="adhoc")
