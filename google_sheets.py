
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Importing the scopes.
# If you are changing or testing the scopes, you need to delete the token.json file to reset the scopes.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1umyzcVkMwqaPWeAHVwi8Dhy7kJE7uXLsFtvijPfhO4I"

# This is pulled mostly from the google API with a few changes.
# I pulled out the google credentials since this is done for both read and write but needs to be set with the right scopes.
def get_google_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=8080)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def read_coordinates():
    # After getting creds I wanted to make the query able to handle different ranges.
    # Although the assignment had the preset 4 rows, this helps dynamically get the rows and handle all of them
    try:
        creds = get_google_credentials()
        service = build("sheets", "v4", credentials=creds)
        
        # Find the last row with data in column A
        result = service.spreadsheets().values().get(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range="A:A",
        ).execute()
        values = result.get('values', [])

        # Very light in script handling here of no values. 
        # If this was deployed, there would be a return up to main bubble up with error handling.
        if not values:
            print("No values found in column A.")
            return []
        
        # Here I am just setting the ultimate range to query.
        range_name = f"A3:B{len(values) }" 

        # Actual google sheets call. Once again, mostly boilerplate
        result = service.spreadsheets().values().get(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=range_name,
        ).execute()
        values = result.get('values', [])
        
        return values

    except HttpError as error:
       print(f"An error occurred while fetching values: {error}") 
       return []

    
# Once we have the weather data, we want to write it back to the google sheet.
# Mostly boilerplate again.    
def write_weather_data(values):
    creds = get_google_credentials()
    service = build("sheets", "v4", credentials=creds)

    # This is writing C3 through E - would need to be more flexible if we were going to write more than 3 columns
    try:
        service = build("sheets", "v4", credentials=creds)

        body = {"values": values}
        result = (
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range="C3:E",
                valueInputOption="USER_ENTERED", # Want to apply this to fomat as if user entered data
                body=body,
            )
            .execute()
        )
        print(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as err:
        print(f"An error occurred: {err}")
        return err


