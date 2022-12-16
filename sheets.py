from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from datetime import datetime, timedelta
import pandas as pd
from tabulate import tabulate

from constants import SCOPES, TOKEN_PATH, SPREADSHEET_ID, NAME
from classes import Shift, Event
from util import date_to_dt, time_to_dt, strip_string_list


DATA_RANGE = "A3:J100"
SAMPLE_RANGE_NAME = 'December 2022!A3:J81'




def get_sheets_service():
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
        service = build('sheets',
                        'v4',
                        credentials=creds,
                        static_discovery=False)

    except HttpError as err:
        print(err)

    return service


def get_sheets():
    titles = []

    sheet_metadata = get_sheets_service().spreadsheets().get(
        spreadsheetId=SPREADSHEET_ID).execute()
    sheets = sheet_metadata.get('sheets', '')
    for sheet in sheets:
        titles.append(sheet.get("properties", {}).get("title", "Sheet1"))
    # title = sheets[0].get("properties", {}).get("title", "Sheet1")

    sheet_id = sheets[0].get("properties", {}).get("sheetId", 0)

    try:
        titles.remove("Notes")
    except:
        pass
    return titles


def get_future_sheets():
    sheets = get_sheets()
    future_sheets = []
    for title in sheets:
        error = None
        try:
            month = datetime.strptime(title, "%B %Y")
        except ValueError as err:
            try:
                year = datetime.strptime(title.split()[-1], "%Y")
                month = datetime(year.year, 12, 31)
            except ValueError as err:
                future_sheets.append(title)
                continue

        now = datetime.now()
        # now = datetime(2023, 1, 1)
        now = datetime(now.year, now.month, 1)
        # print(now.date(), month.date(), month.date() >= now.date(), title)
        if month.date() >= now.date():
            future_sheets.append(title)
    return future_sheets


def save_shifts(shifts):
    with open("shifts.csv", "w") as f:
        for shift in shifts:
            f.write(
                f""""{shift[1]}","{shift[3]}","{shift[0]}","{shift[2]}"\n""")
            # f.write(shift[0])
            # f.write("\n")


def row_to_event(headers, row):
    headers = strip_string_list(headers)
    row = strip_string_list(row)
    event = Event()
    date = None
    start_time = None
    end_time = None
    for i, header in enumerate(headers):
        header = header.lower()
        # print(header)
        if header == "date":
            date = date_to_dt(row[i])
        elif "event" in header and "time" not in header:
            event.summary = row[i]
        elif "venue" in header:
            event.location = row[i]
        elif "start" in header and "time" in header:
            start_time = time_to_dt(row[i])
        elif "end" in header and "time" in header:
            end_time = time_to_dt(row[i])
        elif header == None or row[i] == None:
            pass
        else:
            header = header.replace("\n", " ")
            content = row[i].replace("\n", " ")
            event.description += f"{header.capitalize()}: {content}\n"

    # print(start_time, end_time, date)
    if (isinstance(start_time, str)):
        event.description += f"Bad Start Time: {start_time}\n"
        # print("Bad Start Time", start_time)
        start_time = time_to_dt("12:00")
    if isinstance(end_time, str):
        event.description += f"Bad End Time: {end_time}\n"
        # print("Bad End Time", end_time)
        end_time = time_to_dt("23:59")

    event.start_time = datetime.combine(date, start_time)
    event.end_time = datetime.combine(date, end_time)

    event.end_time = event.start_time + timedelta(
        hours=1) if event.start_time == event.end_time else event.end_time
    event.end_time = event.end_time + timedelta(
        days=1) if event.start_time > event.end_time else event.end_time
    return event


def get_crew_from_row(row, headers):
    for i, header in enumerate(headers):
        if (header == None):
            continue
        header = header.lower()
        if "crew" in header and "name" in header:
            if row[i] == None:
                raise ValueError(f"No crew found in {row}")
            else:
                return row[i]

    raise ValueError(f"No crew found in {row}")


def get_shifts():
    shifts = []

    # Call the Sheets API
    sheet = get_sheets_service().spreadsheets()
    titles = get_future_sheets()
    print(f"""Scanning sheets:\n    '{"' '".join(titles)}'""")
    # titles = ["November 2022"]
    for title in titles:
        # print("Sheet:", title)
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=f"{title}!{DATA_RANGE}").execute()
        values = result.get('values', [])

        if not values:
            print('No data found in ', title, ".")
            return

        # Here we convert the data to pandas dataframe
        # Since otherwise empty cells are left out
        df = pd.DataFrame(values)
        df_replace = df.replace([''], [None])
        # print(tabulate(df, headers='keys', tablefmt='psql'))
        values = df_replace.values.tolist()

        headers = values[0]
        for i, row in enumerate(values[1:]):
            if row == []:
                continue
            try:
                if NAME.lower() in get_crew_from_row(row, headers).lower():
                    shifts.append(row_to_event(headers, row))
            except IndexError:
                print(f"{title} IndexError in row {i}: ", row)
            except ValueError:
                continue

    # print(shifts)
    return shifts


if __name__ == '__main__':
    print(get_shifts())
    # print(get_future_sheets())
