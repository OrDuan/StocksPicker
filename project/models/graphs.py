import time
import matplotlib.pyplot as plt
import matplotlib.ticker as mticket
import matplotlib.dates as mdates
from matplotlib.finance import candlestick
from project import db
from project.models.history import History
t0 = time.time()
import matplotlib
matplotlib.rcParams.update({'font.size': 9})

symbol = 'A'
stocks = db.query(History.date, History.open, History.close, History.high, History.low, History.volume).filter_by(symbol=symbol).all()
stocks_list = [list(tup) for tup in stocks]
# stocks_list = [for x in stocks_list if stocks_list.index(x) == 1]


dates = [stock[0] for stock in stocks]
opens = [stock[1] for stock in stocks]
closes = [stock[2] for stock in stocks]
highs = [stock[3] for stock in stocks]
lows = [stock[4] for stock in stocks]
volumes = [stock[5] for stock in stocks]

x = 0
y = len(dates)
newAr = []
while x < y:
    appendLine = mdates.date2num(dates[x]), opens[x], closes[x], highs[x], lows[x], volumes[x]
    newAr.append(appendLine)
    x += 1

fig = plt.figure()
ax1 = plt.subplot2grid((5, 4), (0, 0), rowspan=4, colspan=4)

# candlestick(ax1, newAr, width=0.85, colorup='g', colordown='r')
ax1.plot(dates, closes)

plt.ylabel('Stock Price')
ax1.grid(True)


ax2 = plt.subplot2grid((5, 4), (4, 0), sharex=ax1, rowspan=1, colspan=4)
ax2.bar(dates, volumes)
ax2.axes.yaxis.set_ticklabels([])
plt.ylabel('Volume')
ax2.grid(True)
plt.xlabel('Date')

plt.suptitle(symbol + ' Stock')
plt.subplots_adjust(left=0.09, bottom=0.20, right=0.97, top=0.95, hspace=0)
ax1.xaxis.set_major_locator(mticket.MaxNLocator(10))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))

for label in ax1.xaxis.get_ticklabels():
    label.set_rotation(90)

for label in ax2.xaxis.get_ticklabels():
    label.set_rotation(45)

plt.setp(ax1.get_xticklabels(), visible=False)
print "DONE IN " + str(time.time() - t0)

plt.show()