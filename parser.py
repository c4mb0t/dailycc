import csv
import datetime
from dateutil import relativedelta

totals = dict()
cutoffs = {'CREDIT CARD': 20, 'BankAmericard Cash Rewards Platinum Plus MasterCard': 23, 'JetBlue Card': 14}
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
        if not card in totals:
            totals[card] = 0
        endtime = datetime.date(today.year, today.month, cutoffs[card])
        starttime = endtime - relativedelta.relativedelta(months=1)
        if date > starttime and date < endtime:
            totals[card] = totals[card] + charge
print totals
