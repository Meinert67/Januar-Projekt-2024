import yfinance as yf
from datetime import datetime
from datetime import timedelta
from calculate_connection_score import calculateConnectionScore

def getData(ticker, startDate, amount, rating):
    # Downloads trading data for stock
    beginDate = datetime.strptime(startDate, "%Y-%m-%d")
    data = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers=ticker,

        progress=False,

        start=startDate,

        end=beginDate + timedelta(days=30),

        interval='1d',

        group_by='ticker',

        auto_adjust=False,

        threads=True,
    )
    data = data.reset_index()

    return handleData(data, startDate, amount, rating)


def handleData(data, startDate, amount, rating):
    dates = list(data["Date"])
    for i, date in enumerate(dates):
        dates[i] = str(date).split(" ")[0]

    opens = list(data["Open"])
    closes = list(data["Close"])


    if str(dates[0]) == startDate:
        pass

    startPrice = opens[0]
    priceChanges = []
    priceRatios = []
    for i in range(amount):
        pChange = round(closes[i]/startPrice*100-100, 2)
        priceChanges.append(pChange)
        priceRatios.append(calculateConnectionScore(rating, pChange))


    return {"startPrice": startPrice, "pChanges": priceChanges, "pRatios": priceRatios}


if __name__ == "__main__":
    print(getData("MRNA", "2023-12-25", 5, 0.9))