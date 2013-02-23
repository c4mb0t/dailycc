import csv
import datetime
from dateutil import relativedelta

totals = dict()
cutoffs = {'Chase Card': 23, 'BOA Card': 10, 'JetBlue Card': 14}
today = datetime.date.today()
with open('data.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    # Skip first line (it's a header)
    next(reader)
    for row in reader:
        card = row[6]
        if card not in cutoffs:
            continue
        rawdate = row[0]
        date = datetime.datetime.strptime(rawdate, "%m/%d/%Y").date()
        charge = float(row[3])
        transtype = row[4]
        if not card in totals:
            totals[card] = 0
        endtime = datetime.date(today.year, today.month+1, cutoffs[card])
        starttime = endtime - relativedelta.relativedelta(months=1)
        if transtype == "debit" and date > starttime and date < endtime:
            totals[card] = totals[card] + charge
            #if card == "BOA Card":
            #    print "S: %s, E: %s, Card: %s, Date: %s, Charge: %f, Total: %f" % (starttime, endtime, card, date, charge, totals[card])
print totals
