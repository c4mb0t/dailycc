import csv
import datetime
from dateutil import relativedelta
from email.mime.text import MIMEText
from subprocess import Popen, PIPE


totals = dict()
cutoffs = {'Chase Card': 23, 'BOA Card': 10, 'JetBlue Card': 14, 'Nordstrom Card': 26}
pretty_cutoffs = dict()
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
        endtime = datetime.date(today.year, today.month, cutoffs[card])
        if today.day > cutoffs[card]:
            endtime = endtime + relativedelta.relativedelta(months=1)
        starttime = endtime - relativedelta.relativedelta(months=1)
        if not card in pretty_cutoffs:
            pretty_cutoffs[card] = "%d/%d" % (endtime.month, endtime.day)
        if transtype == "debit" and date > starttime and date < endtime:
            totals[card] = round(totals[card] + charge, 2)
            #if card == "BOA Card":
            #    print "S: %s, E: %s, Card: %s, Date: %s, Charge: %f, Total: %f" % (starttime, endtime, card, date, charge, totals[card])
print totals
print pretty_cutoffs
msg = MIMEText("Credit card totals: \n%s\nCredit card cutoffs:\n%s" % (totals, pretty_cutoffs))
msg["From"] = ""
msg["To"] = ""
msg["Cc"] = ""
msg["Subject"] = "Daily CC Report"
p = Popen(["/usr/sbin/sendmail", "-t"], stdin=PIPE)
p.communicate(msg.as_string())
