from datetime import datetime, timedelta

from googleapiclient.errors import HttpError

from util import dt_to_string
from constants import TIMEZONE_STR, CALENDAR_ID

class Shift:
    def __init__(self, headers, data):
        print(dict(zip(headers, data)))



class User:
    def __init__(self, name):
        self.name = name

class Event:
    def __init__(self, name="Blank Event", 
                       location = "", 
                       description = "", 
                       start_time = datetime.now(),
                       end_time = datetime.now() + timedelta(hours=1)):
        self.summary = name
        self.location = location
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        # print(self.end_time)
    def __eq__(self, other):
        if self.summary == other.summary:
            return True
        else:
            return False
    def get(self):
        event = {
            'summary': self.summary,
            'location': self.location,
            'description': self.description,
            'start': {
                'dateTime': dt_to_string(self.start_time),
                'timeZone': TIMEZONE_STR,
            },
            'end': {
                'dateTime': dt_to_string(self.end_time),
                'timeZone': TIMEZONE_STR,
            },
            # 'recurrence': [
            #     # 'RRULE:FREQ=DAILY;COUNT=2'
            # ],
            # 'attendees': [
            #     # {'email': 'lpage@example.com'},
            #     # {'email': 'sbrin@example.com'},
            # ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                # {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 12 * 60},
                {'method': 'popup', 'minutes': 5},
                {'method': 'popup', 'minutes': 60},
                ],
            },
        }
        return event
    def create(self, service):
        service.events().insert(calendarId=CALENDAR_ID, body=self.get()).execute()

    def update(self, service, e_id):
        
        try:
            existing_event = service.events().get(calendarId=CALENDAR_ID, eventId=e_id).execute()
            if (existing_event['description'] == self.description and
                existing_event['location'] == self.location and
                existing_event['start'].get('dateTime', existing_event['start'].get('date')) == dt_to_string(self.start_time) and
                existing_event['end'].get('dateTime', existing_event['end'].get('date')) == dt_to_string(self.end_time)):
                # print("Update not required for")
                return

            # print("Updating ", self.summary)
            print(f"""'{self.summary}'*""", end=" ")
            service.events().update(calendarId = CALENDAR_ID, eventId=e_id,
                                    body=self.get()).execute()
        except HttpError as err:
            if err._get_reason() == "Not Found":
                print("Event update requested for was not found, creating instead...")
                self.create(service)
            else:
                raise
    def __str__(self):
        return f"{self.summary}: \n\tAt: {self.location} \n\tStarting: {self.start_time} \n\tEnding: {self.end_time}\n"
    def __repr__(self):
        return self.__str__()


'''
event = {
  'summary': 'Google I/O 2015',
  'location': '800 Howard St., San Francisco, CA 94103',
  'description': 'A chance to hear more about Google\'s developer products.',
  'start': {
    'dateTime': '2015-05-28T09:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': '2015-05-28T17:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=2'
  ],
  'attendees': [
    {'email': 'lpage@example.com'},
    {'email': 'sbrin@example.com'},
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}
'''