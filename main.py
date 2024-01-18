from get_stocks import getDefaultStocks, getBigAmericaStocks
from read_news import get_news_ratings
from get_stock_data import getData
from display_data import plotStockRaw, plotStockAverage, plotAll
from save_data import saveData, loadData
from calculate_covarians import calculateCovarians
import time



class AktieProjekt():
    def __init__(self, stockAmount=5, articleAmount=5, testDays=10):
        self.stockAmount = stockAmount # Stock amount for test (between 1-600)
        self.articleAmount = articleAmount # Article amount for test (recommended 5-20)
        self.testDays = testDays # Number of trading days to test on (between 1-15)

    def evaluateStock(self, stocks):
        # Finds and evaluates articles. Gives ratings and finds trading data
        print("Evaluating stocks...")
        total_ratings = get_news_ratings(stocks, self.articleAmount, self.stockAmount, days=self.testDays)
        for stock, ratings in total_ratings.items():
            print("Getting trade-data for", stock)
            for url, rating in ratings.items():
                data = getData(stock, rating['date'], self.testDays, rating['r'])
                total_ratings[stock][url].update(data)
                time.sleep(0.2)

        print("Saving data")
        saveData(total_ratings)
        print("Data saved")
        self.displayData(total_ratings)

    def displayData(self, total_ratings):
        # Just displays data in graphs and statistics
        plotAll(total_ratings, self.articleAmount)
        for stock, ratings in total_ratings.items():
            print(f"----- {stock} -----")
            for url, rating in ratings.items():
                print(f"\t {rating['date']}: R={rating['r']}, pChanges={rating['pChanges']} pRatios={rating['pRatios']}   -   {url}")
            print("\n")
            plotStockRaw(stock, list(ratings.values()))
            plotStockAverage(stock, list(ratings.values()), confInt=True)

    def displayPreviousData(self, file_name):
        data = loadData(file_name)
        covarianses = calculateCovarians(data)
        print("SAMLET:", covarianses['SAMLET'], "  ALL:", covarianses)
        self.displayData(data)

    def run(self):
        print(f"Starting bot with parameters: {self.stockAmount} amount of stocks, with {self.articleAmount} articles each over {self.testDays} days.")
        print("Gathering stock names...")
        stocks = getBigAmericaStocks()
        print("Stocks found:")
        print(stocks)
        self.evaluateStock(stocks)

if __name__ == "__main__":
    bot = AktieProjekt()
    #bot.displayPreviousData("2024-01-11_17-34-52.json") # Run this to display previous data. Use filename of previous run
    bot.run() # Run this to run the test