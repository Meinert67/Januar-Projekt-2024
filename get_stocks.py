import requests
from bs4 import BeautifulSoup
import random


def getDefaultStocks():
    # Default stocks used for testing early versions
    return ["DIS", "V", "PANW", "BB", "MRNA", "GE"]


def getBigAmericaStocks():
    # Gets a list of top 600 USA stocks and scrambles them
    stocks = []

    querystring = {"shape": "((wt_{F`m{e@njvAqoaXjzjFhecJ{ebIfi}L))"}

    payload = ""
    headers = {
        'authority': "",
        'cache-control': "max-age=0",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'sec-fetch-site': "none",
        'sec-fetch-mode': "navigate",
        'sec-fetch-user': "?1",
        'sec-fetch-dest': "document",
        'accept-language': "en-US,en;q=0.9"
    }

    url = "https://companiesmarketcap.com/usa/largest-companies-in-the-usa-by-market-cap/?page="
    if 1:
        for i in range(1, 7):
            response = requests.request("GET", url + str(i), data=payload, headers=headers,
                                        params=querystring)

            soup = BeautifulSoup(response.text, 'html.parser')

            table = soup.find('table', class_='default-table table marketcap-table dataTable')
            tickers = table.findAll('div', class_="company-code")
            for tick in tickers:
                stocks.append(tick.text)
    random.shuffle(stocks)
    return stocks


if __name__ == "__main__":
    stocks = getBigAmericaStocks()
    print(len(stocks), stocks)