import threading
from time import sleep, time
import urllib2
import datetime
from project import db
from project.models.helper import make_tuple
from project.models.history import History
from project.models.stock import Stock

symbols = Stock.get_all_stocks_symbols()
dict_of_temp_stocks = {}


def first_downloader_get_data(symbol):
    """
    Gets a stock's symbol and append the data to the dict_of_temp_stocks
    """
    try:
        url_string = 'http://www.google.com/finance/getprices?q=' + symbol + '&i=86400&p=1Y&f=d,c,h,l,o,v'
        dict_of_temp_stocks[symbol] = [urllib2.urlopen(url_string).readlines()]
        print 'Downloaded list_of_datas for ' + symbol
    except:
        print '@@@@@@@@Failed to download data for ' + symbol + '@@@@@@@@'
        print 'Trying again in 5 secs...'

        # Wait 5 secs and then call again
        sleep(5)
        first_downloader_get_data(symbol)


def create_history_object(**kwargs):
    stock = make_tuple(kwargs)
    stock.open_, stock.high, stock.low, stock.close = [float(x) for x in
                                                       [stock.open_, stock.high, stock.low, stock.close]]
    all_stock_dates = set(db.query(History.date).filter_by(symbol=stock.symbol).all())

    # Lets check if we already have that day's data
    have_data = True if (stock.dt,) in all_stock_dates else False
    if have_data:
        print 'Already have the data for this date! Updated!'
        # continue
        h = db.query(History).filter_by(date=stock.dt).first()
        h.__dict__ = History(kwargs).__dict__.copy()


    # init new object and add it to the db session
    h = History(symbol=stock.symbol,
                date=stock.dt,
                open=stock.open_,
                high=stock.high,
                low=stock.low,
                close=stock.close,
                volume=stock.volume.replace('\n', ''))
    return h


def save_data(symbol):
    try:
        for stock in dict_of_temp_stocks[symbol]:
            for row in xrange(7, len(stock)):
                if stock[row].count(',') != 5:
                    continue

                offset, close, high, low, open_, volume = stock[row].split(',')
                if offset[0] == 'a':
                    day = float(offset[1:])
                    offset = 0
                else:
                    offset = float(offset)

                dt = datetime.datetime.fromtimestamp(day + (86400 * offset))
                h = create_history_object(dt=dt, close=close, high=high, low=low, offset=offset, open_=open_,
                                          symbol=symbol, volume=volume)

                db.add(h)

            db.commit()
    except:
        print 'Failed to save the data to ' + symbol


def first_looper(start, end):
    if end != 0:
        for symbol in symbols[start:end]:
            first_downloader_get_data(symbol)
    else:
        for symbol in symbols[start:]:
            first_downloader_get_data(symbol)


def run_first_downloader():
    time0 = time()
    # Download last year data
    t1 = threading.Thread(target=first_looper, args=(0, 2))
    # t2 = threading.Thread(target=first_looper, args=(101, 200))
    # t3 = threading.Thread(target=first_looper, args=(201, 300))
    # t4 = threading.Thread(target=first_looper, args=(301, 400))
    # t5 = threading.Thread(target=first_looper, args=(401, 0))
    t1.start()
    # t2.start()
    # t3.start()
    # t4.start()
    # t5.start()
    t1.join()
    # t2.join()
    # t3.join()
    # t4.join()
    # t5.join()

    # Save the data into the db
    for save_symbol in symbols:
        save_data(save_symbol)

    print 'DONE run_first_donloader! Overall time:' + str(time() - time0)


run_first_downloader()