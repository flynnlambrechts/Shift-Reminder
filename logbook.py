from sheets import get_shifts, get_sheets_service
from util import convert_blank_to_none, date_to_dt

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
from classes import Event
from sheets import get_sheets_service

LOGBOOK_SHEET_ID = "1FNDUSjohSDIYGPALKQ9sapgSLH2id67BAaVg3HCWfk4"
FIRST_DATA_ROW = 4

def get_values(range):
    service = get_sheets_service()
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=LOGBOOK_SHEET_ID, range=range).execute()
        rows = result.get('values', [])
        print(f"{len(rows)} rows retrieved")
        return result.get('values', [])

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

def latest_log():
    last_index = 0
    scroll_factor = 100

    start_row = FIRST_DATA_ROW
    end_row = start_row + scroll_factor
    
    check_range = f"A{start_row}:A{end_row - 1}"
    # print(get_values(check_range))
    values = get_values(check_range)
    # print(values)
    while len(values) >= scroll_factor:
        
        last_index = values[-1][0]
        start_row += scroll_factor
        end_row = start_row + scroll_factor - 1
        check_range = f"A{start_row}:A{end_row}"

        values = get_values(check_range)
        # print(values)
    
    if values != []:
        last_index = values[-1][0]

    # print(last_index)
    last_index = int(last_index)
    last_row = int(last_index) + FIRST_DATA_ROW - 1
    last_data = get_values(f"A{last_row}:D{last_row}")[0]
    # print(last_data)
    NAME_INDEX = 1
    DATE_INDEX = 3

    last_entry = {
        "name": last_data[NAME_INDEX],
        "date": date_to_dt(last_data[DATE_INDEX]),
        "number": last_index,
        "index": last_row
    }

    # print(last_entry)
    return last_entry

    
def generate_values():
    values = []
    last_entry = latest_log()

    date_from = last_entry["date"] + timedelta(days=1)
    number = last_entry["number"] + 1
    # print(date_from)

    shifts = get_shifts(date_from)
    # print(shifts)
    for shift in shifts:
        if shift.start_time < datetime.now():
            values.append([number, shift.summary, shift.location, shift.start_time.strftime("%d/%m/%Y")])
            number += 1
            
    # print(values)
    return {"values" : values, "starting_at" : last_entry["index"] + 1}

def write_logbook():
    print("Writing to logbook...")
    values = generate_values()
    service = get_sheets_service()

    body = {
        "values" : values["values"]
    }
    try:
        result = service.spreadsheets().values().update(
            spreadsheetId=LOGBOOK_SHEET_ID, range=f'Sheet1!A{values["starting_at"]}',
            valueInputOption="USER_ENTERED", body=body).execute()
        # print(result)
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error
    
    print(f"""{len(values["values"])} rows added to logbook.""")
    



if __name__ == '__main__':
    # generate_values()
    write_logbook()
    
    
