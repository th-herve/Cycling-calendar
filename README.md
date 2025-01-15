# Cycling-calendar

My first programming project, a straightforward web application that presents professional cycling races scheduled for the 2023 season in a calendar format. You can also add the races to your google calendar.

**[Go to the live website.](https://cycling.th-herve.fr)** 
`!!` Some functionalities do not work anymore due to a change in the sportradar api.

## Screenshots

<details>
  <summary>Image 1</summary>
  <img src="./static/Images/screenshots/main.png" name="main-page">
</details>
<details>
  <summary>Image 2</summary>
  <img src="./static/Images/screenshots/modal.png" name="modal">
</details>

## Resources used

<div align="left">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" height="40" alt="python logo"  />
  <img [width](width.md)="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg" height="40" alt="flask logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" height="40" alt="javascript logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" height="40" alt="html5 logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" height="40" alt="css3 logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/google/google-original.svg" height="40" alt="google logo"  />
</div>

###

- **[Flask](https://github.com/pallets/flask/)**: Python backend framework.
- **[Sport radar api](https://developer.sportradar.com/)**: To retrieve the data.
- **[FullCalendar](https://fullcalendar.io/)**: JavaScript library for creating the calendar view.
- **Google api**: Integration for adding races to the user's calendar. Google OAuth2 is used for authentication with the Google Calendar API.

## How to run in dev environment

### Optional: install python 3.12 along another version on the system

Can fix problem with packages failing to install with newer version.

```bash
# install pyenv
sudo pacman -S pyenv

# install python 3.12
pyenv install 3.12.0

# check if installed
pyenv versions # it should list a 3.12 version along the system version
```

It install another version of python with its binary in `~/.pyenv/versions/3.12.0/bin/python`
Now when creating the virtual env, user this binary.

### Create a virtual env

```bash
python -m venv .venv --clear

# or if using pyenv
~/.pyenv/versions/3.12.0/bin/python -m venv .venv --clear
```

### Launch the env and install requirement

```bash
source .venv/bin/activate

pip install -r requirements.txt 
```

### Launch flask

```bash
# in the venv
flask run
```
