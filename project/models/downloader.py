import Queue
import threading
from time import sleep, time
import urllib2
import datetime
from project import db
from project.models.history import History
from project.models.stock import Stock

symbols = Stock.get_all_stocks_symbols()
list_of_datas = {}


def get_data(symbol):
    try:
        url_string = "http://www.google.com/finance/getprices?q=" + symbol + "&i=86400&p=1Y&f=d,c,h,l,o,v"
        list_of_datas[symbol] = [urllib2.urlopen(url_string).readlines()]
        print "Downloaded list_of_datas for " + symbol
    except:
        print "@@@@@@@@Failed to download data for " + symbol + "@@@@@@@@"
        print "Trying again in 5 secs..."
        sleep(5)
        get_data(symbol)


def save_data(symbol):
    try:
        for data in list_of_datas[symbol]:
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
                db.add(h)

                print "Saved " + symbol + " Date: " + str(dt.day) + "/" + str(dt.month) + "/" + str(dt.year)
            db.commit()
    except:
        print "Failed to save the data to " + symbol


def looper(start, end):
    if end != 0:
        for symbol in symbols[start:end]:
            get_data(symbol)
    else:
        for symbol in symbols[start:]:
            get_data(symbol)
time0 = time()
# Download last year data
t1 = threading.Thread(target=looper, args=(0, 100))
t2 = threading.Thread(target=looper, args=(101, 200))
t3 = threading.Thread(target=looper, args=(201, 300))
t4 = threading.Thread(target=looper, args=(301, 400))
t5 = threading.Thread(target=looper, args=(401, 0))
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t1.join()
t2.join()
t3.join()
t4.join()
t5.join()

# Save the data into the db
for save_symbol in symbols:
    save_data(save_symbol)

print "DONE! Overall time:" + str(time()-time0)