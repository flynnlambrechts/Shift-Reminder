# from classes import Event
from keep_alive import keep_alive

from sheets import get_shifts
from cal import get_cal_events, calendar_service
from time import sleep


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
    service = calendar_service()
    shifts = get_shifts()

    if (len(shifts) == 0):
        exit

    events = get_cal_events(earliest_time(shifts))

    for shift in shifts:
        event_exists = search_events(shift.summary, events)
        if not event_exists:
            shift.create(service)
        else:
            shift.update(service, event_exists)


if __name__ == "__main__:
    keep_alive()
    while True:
        update_calendar()
        # Update every 6hrs
        sleep(21600)
