import datetime
from project import db
from project.models.history import History

stock = [285.88, 290.59, 291.53, 292.33, 299.66, 307.55, 306.57, 306.87, 308.69, 304.11, 305.23, 303.48, 301.06,
         298.94, 303.4, 312.01, 306.1, 302.41, 301.22, 305.57, 304.21, 300.99, 300.75, 296.91, 295.74, 297.26, 296.69,
         293.97, 291.34, 286.47, 284.82, 285.57, 287.09, 284.57, 289.73, 290.01, 286.21, 280.93, 281.58, 283.98,
         280.98, 288.8, 293.64, 294.1, 295.86, 299.71, 300.36, 299.64, 298.86, 297.92, 296.06, 304.17, 312.034, 312.06,
         316.34, 311.49, 314.13, 312.65, 318.12, 316.01, 312.64, 320.95, 320.51, 314.76, 319.04, 310.03, 303.23,
         298.23, 305.174, 310.889, 310.7, 306.4, 310.49, 310.77, 328.931, 326.44, 332.54, 326.756, 332.21, 363.39,
         358.16, 362.7, 361.08, 364.03, 359.002, 358.74, 358.892, 356.18, 343.56, 350.31, 354.378, 349.53, 356.22,
         367.396, 369.17, 366.18, 364.94, 362.57, 368.92, 372.31, 376.64, 381.37, 386.71, 393.62, 392.3, 384.66,
         385.96, 384.49, 386.95, 384.89, 387.78, 382.19, 381.25, 384.24, 388.97, 387.65, 395.96, 395.19, 402.2, 402.92,
         399.2, 404.39, 398.08, 393.37, 398.79, 397.97, 396.44, 393.63, 398.03, 401.92, 401.01, 397.66, 390.98, 397.54,
         395.87, 395.8, 399.61, 407.05, 404.54, 399.87, 387.6, 386.28, 394.43, 384.2, 403.01, 358.69, 346.15, 347.95,
         346.45, 354.59, 361.08, 360.87, 361.79, 349.25, 357.2, 357.35, 353.65, 347.38, 349.8, 346.76, 351.78, 358.32,
         359.8, 360.13, 362.1, 359.78, 363.9, 372.37, 372.16, 372.06, 370.53, 368.82, 370.64, 371.51, 373.74, 375.04,
         378.77, 373.23, 368.97, 360.62, 351.85, 354.71, 343.41, 338.47, 338.29, 336.365, 342.99, 341.96, 333.62, 323,
         317.76, 327.07, 331.805, 317.11, 311.73, 315.91, 316.08, 323.68, 324.91, 330.87, 329.32, 324.58, 337.15,
         303.83, 296.58, 300.38, 304.13, 307.89, 308.01, 310.05, 297.38, 292.71, 288.32, 292.24, 302.86, 304.64,
         297.62, 295.19, 297.7, 296.755, 301.19, 305.01, 304.91, 312.24, 310.82, 310.16, 313.78, 312.55, 308.84,
         307.19, 306.78, 323.57, 329.67, 327.5, 332.41, 335.2, 325.91, 326.27, 327.62, 325.62, 334.38, 327, 324.2,
         327.24, 324.16, 327.44, 325.69, 324.57, 324.78, 332.39, 332.85, 337.492]

period = 5


def calc_sma(index):
    """
    Calculate the SMA - Simple Moving Average of the last +period+ days from +index+
    """
    return sum(stock[index - period:index]) / period


def get_percentage_change(_from, _to):
    """
    return percentage of the change between +from+ to +to+
    """
    return ((_to - _from) / _to) * 100


def duan_sma_rank():
    global rank, x, sma5, percentage_sma5, flag, avg, p
    rank = 0
    sma5 = [calc_sma(stock.index(x)) for x in stock[period:]]
    percentage_sma5 = []
    flag = False
    print sma5
    for avg in sma5:
        if not flag:
            flag = True
            continue
        p = get_percentage_change(sma5[sma5.index(avg) - 1], avg)
        percentage_sma5.append(p)
        rank += abs(p) - 0.555
        print p, " - ", rank
    print percentage_sma5


# duan_sma_rank()

def find_behavior(symbol, weeks):
    """
    iterate over closep and look for technical behaviors
    """
    days_period = 7  # The days differences between the 3 points.
    highlighted_dates = []  # We will append dates that chosen by change rate.

    start_date = datetime.datetime.now() - datetime.timedelta(weeks=weeks)

    # Get all the stocks from start_date
    stocks = db.query(History).filter((History.symbol == symbol) & (History.date > start_date)).all()

    for index, stock in enumerate(stocks):
        # Check we don't get out of list size
        if index < days_period or index > len(stocks) - days_period-1: continue

        # define 3 points: +- *days_period* days from current day
        close_left = stocks[index - days_period].close
        close_right = stocks[index + days_period].close
        close_center = stocks[index].close

        # Get the percentage change between all the points
        left_per = get_percentage_change(close_left, close_center)
        right_per = get_percentage_change(close_right, close_center)
        # print "left-val: {}, center-val: {}, right-val: {}".format(close_left, close_center, close_right)

        # Find points where the change from the center is 4 or -4 percentages
        if (left_per > 4 and right_per > 4) or (left_per < -4 and right_per < -4):
            highlighted_dates.append(stock)

        if len(highlighted_dates) > 2:
            print "#########################################################"
            print "FOUND IT! left:{}, center:{}, right:{}".format(close_left, close_center, close_right)
            print "percentage-left: {}, percentage-right: {}".format(left_per, right_per)
            print highlighted_dates
            highlighted_dates = []

        # Drop old date from highlghteds!
        if highlighted_dates and highlighted_dates[0].date < stock.date - datetime.timedelta(weeks=10):
            del highlighted_dates[0]



find_behavior("A", 30)