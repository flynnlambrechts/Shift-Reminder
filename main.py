from time import sleep
# import os

# from classes import Event
from keep_alive import keep_alive
from sheets import get_shifts
from cal import get_cal_events, calendar_service
from constants import CALENDAR_ID
from logbook import write_logbook
from datetime import datetime


# try:
#     RUNNING = os.environ["REPLIT"]
#     API_KEY = os.environ['API_KEY']
# except KeyError:
#     RUNNING = "LOCAL"
#     API_KEY = None



def search_events(name, events):
    if events == None:
        return False

    for e_id in events:
        if events[e_id] == name:
            return e_id

    return False


def earliest_time(shifts):
    earliest = shifts[0].start_time
    for event in shifts[1:]:
        if event.start_time < earliest:
            earliest = event.start_time
    return earliest


# Can have same name but on different days


def update_calendar():
    print("Updating Calendar...")

    service = calendar_service()
    shifts = get_shifts()

    if (len(shifts) == 0):
        exit

    

    events = get_cal_events(earliest_time(shifts))

    creation = False
    

    for shift in shifts:
        e_id = search_events(shift.summary, events)
        if not e_id:
            if creation == False:
                print("Created:\n    ", end="")
                creation = True
                
            shift.create(service)
            print(f"""'{shift.summary}'""", end=" ")
        else:
            events.pop(e_id)
            shift.update(service, e_id)
    
    print("", end="\n") if creation == True else 0
            
    count = 0
    for e_id in events:
        service.events().delete(calendarId=CALENDAR_ID, eventId=e_id).execute()
        count += 1
    
    if count > 0:
        print(count, "Events Deleted.")

    print("Process Completed.")




if __name__ == "__main__":
    # Test
    keep_alive()
    while True:
        print(f"""Starting at {datetime.now().strftime("%H:%M %d/%m/%Y")}""")
        update_calendar()
        print("Sleeping for 1 min.")
        sleep(60)
        write_logbook()
        print("Sleeping for 3hrs")
        # Update every 3hrs
        sleep(3 * 59 * 60)
        