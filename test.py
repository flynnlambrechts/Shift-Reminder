from datetime import datetime, timedelta


start = datetime.now()
end = datetime.now() + timedelta(hours=1.5)
difference = end - start
print(round(difference.seconds/(60*60) * 34.5, 2))