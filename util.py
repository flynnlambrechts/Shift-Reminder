from datetime import datetime

def strip_string_list(list):
    result = []
    for item in list:
        if isinstance(item, str):
            item = item.strip()
        result.append(item)
    return result



def dt_to_string(datetime_object):
    # '2015-05-28T09:00:00-07:00'
    # return datetime_object.strftime("%Y-%m-%dT%H:%M:%S+11:00")
    return datetime_object.isoformat() + "+11:00"

def date_to_dt(date):
    error = None
    try:
        # 'Friday, 20 May2022'
        return datetime.strptime(date, "%A, %d %B%Y").date()
    except Exception as err:
        error = err
        pass

    try:
        # Friday 16th September 2022
        return datetime.strptime(date, "%A %d %B %Y").date()
    except Exception as err:
        error = err
        pass

    print(f"Bad Date Read Of: {date}")
    print(err)
    return date


def time_to_dt(time):
    # time = "12:00" if time == "TBC" else time
    if time == None:
        return "None"
    # '19:35'
    try:
        return datetime.strptime(time, "%H:%M").time()
    except ValueError:
        return time
    except TypeError:
        return "Type Error"


if __name__ == "__main__":
    print(datetime.now().isoformat())
    print(dt_to_string(datetime.now()))
