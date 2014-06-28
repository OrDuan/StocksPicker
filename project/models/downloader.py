import urllib
import datetime
from project.models.db_helper import save
from project.models.history import History
import timeit

symbols = ["GOOG", "AAPL"]
list_of_datas = []

def get_data():
    for symbol in symbols:
        url_string = "http://www.google.com/finance/getprices?q=" + symbol + "&i=86400&p=1Y&f=d,c,h,l,o,v"
        list_of_datas.append(urllib.urlopen(url_string).readlines())
        print "Downloaded list_of_datas for " + symbol


def save_data():
    for symbol, data in zip(symbols, list_of_datas):
        for row in xrange(7, len(data)):
            if data[row].count(',') != 5:
                continue

            offset, close, high, low, open_, volume = data[row].split(',')
            if offset[0] == 'a':
                day = float(offset[1:])
                offset = 0
            else:
                offset = float(offset)
            open_, high, low, close = [float(x) for x in [open_, high, low, close]]
            dt = datetime.datetime.fromtimestamp(day + (86400 * offset))
            h = History(symbol=symbol,
                        date=dt,
                        open=open_,
                        high=high,
                        low=low,
                        close=close,
                        volume=volume.replace("\n", ""))
            save(h)
            print "Saved " + symbol + " Date: " + str(dt.day) + "/" + str(dt.month) + "/" + str(dt.year)

get_data()
save_data()