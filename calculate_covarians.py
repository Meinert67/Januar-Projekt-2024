

def calculateCovarians(total_ratings):
    covarianses = {}
    for stock, articles in total_ratings.items():
        averages = []
        ratings = []
        average_total = []
        for article in list(articles.values()):
            averages.append(sum(article['pChanges'])/len(article['pChanges']))
            average_total += article['pChanges']
            ratings.append(article['r'])
        average_rating = sum(ratings)/len(ratings)
        average_total = sum(average_total)/len(average_total)

        sum_ = 0
        for rating, price_average in zip(ratings, averages):
            sum_ += (rating - average_rating) * (price_average - average_total)

        sum_ = sum_ / (len(ratings) - 1)
        covarianses[stock] = sum_

    covarianses["SAMLET"] = sum(list(covarianses.values())) / len(list(covarianses.values()))

    return covarianses
