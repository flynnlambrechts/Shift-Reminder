from datetime import datetime
import pandas as pd
import parsedatetime as pdt
import timefhuman

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

    # now = datetime.now()
    # print("Parsing:", date)

    try:
        # 'Friday, 20 May2022'
        return datetime.strptime(date, "%A, %d %B%Y").date()
    except Exception as err:
        error = err
        pass

    try:
        # Friday 16th September 2022
        temp_date = date.split(' ', 1)[1]
        return datetime.strptime(temp_date, "%d %B %Y").date()
    except Exception as err:
        error = err
        pass
    
    try:
        # Friday 16 September 2022
        return datetime.strptime(date, "%A %d %B %Y").date()
    except Exception as err:
        error = err
        pass

    try:
        return datetime.strptime(date, "%d/%m/%Y").date()
    except Exception as err:
        error = err
        pass

    try:
        cal = pdt.Calendar()
        # print(cal.parseDT(date))
        return cal.parseDT(date)[0]
    except Exception as err:
        error = err
        pass
    
    try:
        return timefhuman(date)
    except Exception as err:
        error = err
        pass

    print(f"Bad Date Read Of: {date}")
    print(error)
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

def convert_blank_to_none(data):
    # Here we convert the data to pandas dataframe
    # Since otherwise empty cells are left out
    df = pd.DataFrame(data)
    df_replace = df.replace([''], [None])
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    data = df_replace.values.tolist()
    return data

if __name__ == "__main__":
    print(datetime.now().isoformat())
    print(dt_to_string(datetime.now()))
    