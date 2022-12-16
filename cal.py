from __future__ import print_function

from datetime import datetime
import dateutil.parser
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from constants import SCOPES, TOKEN_PATH, CALENDAR_ID
from classes import Event
from util import dt_to_string



def calendar_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
    except HttpError as error:
        print('An error occurred: %s' % error)
    
    return service

def create_event(event):
    # https://developers.google.com/calendar/api/guides/create-events
    event = calendar_service().events().insert(calendarId=CALENDAR_ID, body=event.get()).execute()


def get_cal_events(from_time = datetime.now()):
    service = calendar_service()
    # now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming events')
    events_result = service.events().list(calendarId=CALENDAR_ID, 
                                          timeMin=dt_to_string(from_time),
                                        #   maxResults=10, 
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    # print(events_result)   
                                      
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return

    events_list = {}

    for event in events:
        
        events_list[event.get('id')] = event['summary']
        # # start = event['start'].get('dateTime', event['start'].get('date'))
        # # end = event['end'].get('dateTime', event['end'].get('date'))
        # # e_id = event.get('id')
        # print(e_id, start, end, event['summary'])

    return events_list


def main():
    service = calendar_service()
    
    # Creates an event
    event = Event("Test Event 69", "Commbank Stadium", "This is an event")
    # create_event(event)
    event.create(service)
    # event.update(service, "69")


if __name__ == '__main__':
    # json.dumps(get_cal_events()[0], sort_keys=True, indent=4)
    # main()
    print(get_cal_events().values())