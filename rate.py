import pysentiment2 as ps



class articleRater(object):
    def __init__(self):
        # We use this to rate articles

        # Specify that we want to use the Loughran-McDonald Dictionary
        self.lm = ps.LM()

    def rate_article(self, text):
        # We use this function to rate article texts

        # Tokenize the text by using a nltk stemmer and removing redundant words with stoplists
        tokens = self.lm.tokenize(text)

        # Now run the modified text through the Loughran-McDonald Dictionary and calculate score based on negative and positive words
        score = self.lm.get_score(tokens)
        return round(score['Polarity'], 2)


if __name__ == "__main__":
    rater = articleRater()
    text = "US stock futures tipped higher on Thursday, eyeing a rebound from recent losses as investors looked to fresh quarterly earnings for inspiration amid dwindling hopes for an early 2024 interest rate cut. S&P 500 (^GSPC) futures added around 0.4%, while those on the tech-heavy Nasdaq 100 (^NDX) jumped 0.7%. Dow Jones Industrial Average (^DJI) futures hugged the flatline. Techs are in the vanguard after a bullish AI-fueled revenue outlook from TSMC (TSM), a key supplier to Apple (APPL) and Nvidia (NVDA). The Taiwanese contract chipmaker's profit fell but beat Wall Street estimates. Shares of AMD (AMD) and other chipmakers stepped higher in premarket as TSMC put on almost 7%. Stocks are still struggling to get off the ground this year as central bankers' comments and mixed economic data put investors' faith in a Federal Reserve pivot to the test. The odds of a rate cut in March as seen by traders have dropped 10 percentage points from a week ago, per the CME FedWatch Tool."
    print(rater.rate_article(text))