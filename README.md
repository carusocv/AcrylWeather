# Chris Caruso <> Acryl Coding Challenge

## Setup

Requires Python 3

### Create and activate a virtual env

Navigate into the root directory ex: `cd ~/Dev/git/AcrylWeather`

Create a virtual env ex: `python3 -m venv acrylvenv`

Activate via `source acrylvenv/bin/activate`

(Deactivate when complete with `deactivate`)

### Install requirements

With the venv active, install with `pip3 install -r requirements.txt`


### Set Secret

Use this link from [OneTimeSecret](https://onetimesecret.com/secret/4v2xt843u3oiq88kqegkzawmnw989oh). Note this will only be valid once.

Add the secret to `client_secret` value in `credentails.json`

## Run

### Open Google Sheets

[Open Google Sheet](https://docs.google.com/spreadsheets/d/1umyzcVkMwqaPWeAHVwi8Dhy7kJE7uXLsFtvijPfhO4I/edit#gid=0)

### Run

Run the script from the root directory with `python3 main.py`

## Notes

I tried to keep the directory structure as simple as possible for quick clone and testing.

Otherwise I would've probably built out more diretories for the supporting methods, as well as testing files.

Note, the first time you run the application, you will need to sign in via Google. Upon successfull authentication, a `token.json` file will be created.

Also please ensure you are not running anything on `:8080` prior to running this application.

**This project and all work is by Chris Caruso and has been shared with Acryl Data as a coding challenge**
