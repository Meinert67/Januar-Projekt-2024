import matplotlib.pyplot as plt
import numpy as np
import math
import scipy

def calcConfInt(data, mean, std):
    # Calculates 95% confidence interval
    u = scipy.stats.norm.ppf(0.975) * math.sqrt(std**2/len(data))
    print("Standard error:", math.sqrt(std**2/len(data)))
    return round(mean - u, 5), round(mean + u, 5)

def plotStockRaw(stock, data, show=True):
    # For plotting the raw data from bot
    x_coords = []
    daysAboveZero = []
    daysBelowZero = []
    daysZero = []

    length = len(data[0]['pRatios'])

    for i in range(length):
        x_coords.append(i+1)
        daysAboveZero.append(0)
        daysBelowZero.append(0)
        daysZero.append(0)

    plt.xticks(x_coords)
    plt.axhline(y=0, linestyle='--')

    aboveZero = 0
    belowZero = 0
    zero = 0

    for rating in data:
        for i, val in enumerate(rating['pRatios']):
            if val > 0:
                aboveZero += 1
                daysAboveZero[i] += 1
            elif val < 0:
                belowZero += 1
                daysBelowZero[i] += 1
            else:
                zero += 1
                daysZero[i] += 1
        plt.plot(x_coords, rating['pRatios'], "o")

    plt.xlabel("Trading days since article")
    plt.ylabel("Rating & Price-Change Connection")
    if show:
        for i in range(len(daysAboveZero)):
            print(f"Day {i+1} - Above: {daysAboveZero[i]}   Below: {daysBelowZero[i]}   Zero: {daysZero[i]}")
        plt.title(f"> {stock} <: {len(data)} articles.   Positive: {aboveZero}   Negative: {belowZero}   Zero: {zero}")
        plt.show()





def plotStockAverage(stock, data, show=True, confInt=False, doLinReg=False):
    # calculates and plots averages
    x_coords = []
    days = []

    length = len(data[0]['pRatios'])

    for i in range(length):
        x_coords.append(i + 1)
        days.append([])

    plt.xticks(x_coords)
    plt.axhline(y=0, linestyle='--')

    for rating in data:
        for i in range(len(rating['pRatios'])):
            days[i].append(rating['pRatios'][i])

    averages = []
    stds = []


    for day in days:
        mean = round(float(np.mean(day)), 5)
        averages.append(mean)
        std = round(float(np.std(day)), 5)
        stds.append(std)
        if confInt:

            print("Day confint:", calcConfInt(day, mean, std))

    if confInt:
        print("Means:", averages)
        print("STDS:", stds)
        print("------------------------------------")





    plt.plot(x_coords, averages, "o")

    if doLinReg:
        slope, intercept, r, p, std_err = scipy.stats.linregress(x_coords, averages)
        line_y = []
        for x in x_coords:
            line_y.append(slope * x + intercept)
        plt.plot(x_coords, line_y)
        plt.title(f"Averages: Slope: {round(slope, 3)}, Intercept: {round(intercept, 3)}, R^2: {round(r, 3)}")

    plt.xlabel("Trading days since article")
    plt.ylabel("Average Rating & Price-Change Connection")

    if show:
        if not doLinReg:
            plt.title(f"> {stock} <: {len(data)} articles AVERAGES")
        plt.show()




def plotAll(total_ratings, articleAmount):
    ratings_combined = []

    for stock, ratings in total_ratings.items():
        ratings_combined += list(ratings.values())

    plotStockRaw("ALL DATA", ratings_combined)

    for stock, ratings in total_ratings.items():
        plotStockAverage(stock, list(ratings.values()), show=False)
    plt.title(f"> ALL DATA INDIVIDUAL AVERAGES <: {len(total_ratings)} Stocks with {articleAmount} amount of articles")
    plt.show()

    plotStockAverage("ALL DATA COMBINED AVERAGES", ratings_combined, confInt=True)

    plotStockAverage("ALL DATA COMBINED AVERAGES + LINREG", ratings_combined, doLinReg=True)



if __name__ == "__main__":
    plotStockRaw("GE", {"H": {'pRatios': [0.05, -0.06, -0.32, -0.62, -0.52]}}, 5)