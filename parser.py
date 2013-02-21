import csv
import datetime
from dateutil import relativedelta

totals = dict()
cutoffs = {'MC': 20, 'VISA': 23}
today = datetime.date.today()
with open('test.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    # Skip first line (it's a header)
    next(reader)
    for row in reader:
        rawdate = row[0]
        date = datetime.datetime.strptime(rawdate, "%m/%d/%Y").date()
        card = row[1]
        charge = float(row[2])
        if not card in totals:
            totals[card] = 0
        endtime = datetime.date(today.year, today.month, cutoffs[card])
        starttime = endtime - relativedelta.relativedelta(months=1)
        if date > starttime and date < endtime:
            totals[card] = totals[card] + charge
print totals
