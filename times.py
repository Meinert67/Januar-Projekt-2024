import pandas_market_calendars as mcal
from datetime import date
from datetime import datetime

def getDate():
    date = datetime.now()
    return date

def marketDaysOpen(startDate, endDate="Now"):
    # Finds number of trading days between 2 dates
    if endDate == "Now":
        endDate = date.today()
    nyse = mcal.get_calendar('NYSE')
    open = nyse.valid_days(startDate, endDate)

    return len(open)


if __name__ == "__main__":
    print(marketDaysOpen("2023-12-23"))