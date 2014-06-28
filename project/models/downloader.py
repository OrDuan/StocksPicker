import urllib
import datetime
from project.models.db_helper import save
from project.models.history import History
import timeit

__author__ = 'Or Duan'

interval_seconds = 86400
symbol = "GOOG"
url_string = "http://www.google.com/finance/getprices?q=" + symbol + "&i=86400&p=1Y&f=d,c,h,l,o,v"
data = urllib.urlopen(url_string).readlines()
i = 0

for row in xrange(7, len(data)):
    i += 1
    if data[row].count(',') != 5:
        continue

    offset, close, high, low, open_, volume = data[row].split(',')
    if offset[0] == 'a':
        day = float(offset[1:])
        offset = 0
    else:
        offset = float(offset)
    open_, high, low, close = [float(x) for x in [open_, high, low, close]]
    dt = datetime.datetime.fromtimestamp(day + (interval_seconds * offset))
    h = History(symbol=symbol,
                date=dt,
                open=open_,
                high=high,
                low=low,
                close=close,
                volume=volume.replace("\n", ""))
    save(h)
    print "Saved " + symbol + " Date: " + str(dt.day) + "/" + str(dt.month) + "/" + str(dt.year)
print i