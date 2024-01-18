def calculateConnectionScore(rating, pChange):
    if rating != 0:
        ratio = round(pChange * rating, 2)
    else:
        ratio = 0
    return ratio

if __name__ == "__main__":
    print(calculateConnectionScore(0.9, 0.1))