from datetime import datetime
import parsedatetime as pdt

cal = pdt.Calendar()


print(type(cal.parseDT("Friday 16th September 2022")[0]))