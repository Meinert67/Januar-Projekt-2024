import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from rate import articleRater
import time
from times import marketDaysOpen



def get_news_ratings(stocks, amount, stockAmount, days=5):
    rater = articleRater()
    driver = webdriver.Chrome()

    total_ratings = {}


    # Go through each stock, and find articles, making sure the articles have enough trading days for testing. Then rate the articles
    for i, stock in enumerate(stocks):
        print("Gathering news for", stock)
        url = f"https://finance.yahoo.com/quote/{stock}/news?p={stock}"

        driver.get(url)
        if i == 0:
            # Reject cookies
            try:
                time.sleep(1)
                driver.execute_script("window.scrollTo(0, 800)")
                time.sleep(0.5)
                driver.find_element(By.XPATH, '//*[@id="consent-page"]/div/div/div/form/div[2]/div[2]/button[2]').click()
            except:
                print("Cookies couldn't be rejected")
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, 800)")
        current = 0
        ratings = {}
        fail_counter = 0
        while fail_counter < 10:
            try:
                time.sleep(0.3)
                current += 1
                element = driver.find_element(By.XPATH, f'//*[@id="latestQuoteNewsStream-0-Stream"]/ul/li[{current}]/div/div/div[2]')
                driver.execute_script("arguments[0].scrollIntoView();", element)

                # Finds how long ago since release date
                time_ago = element.find_element(By.XPATH, 'div/span[2]').text
                save = False
                if "days ago" in time_ago:
                    num = int(time_ago.split(" ")[0])
                    if num > days:
                        save = True

                elif "months ago" in time_ago or "last month" in time_ago:
                    save = True

                if save:
                    link = element.find_element(By.XPATH, 'h3/a').get_attribute('href')

                    # Gets date and article text from read_news(link) function
                    date, text = read_news(link)
                    if len(text) > 0 and len(text.split(" ")) >= 50:
                        if marketDaysOpen(date) > days:
                            rating = rater.rate_article(text)
                            ratings[link] = {"r": rating, "date": date}


                fail_counter = 0
                if len(ratings) >= amount:
                    total_ratings[stock] = dict(ratings)
                    break

            except NoSuchElementException:
                fail_counter += 1

        if len(list(total_ratings.keys())) >= stockAmount:
            break

    # Closes chrome driver
    driver.close()

    # Return all ratings
    return total_ratings



def read_news(url):
    # Gets news-block-text and release date from article URL
    date = ""
    complete = ""

    querystring = {"shape": "((wt_{F`m{e@njvAqoaXjzjFhecJ{ebIfi}L))"}

    payload = ""
    headers = {
        'authority': "",
        'cache-control': "max-age=0",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
        'sec-fetch-site': "none",
        'sec-fetch-mode': "navigate",
        'sec-fetch-user': "?1",
        'sec-fetch-dest': "document",
        'accept-language': "en-US,en;q=0.9"
    }
    try:
        response = requests.request("GET", url, data=payload, headers=headers,
                                        params=querystring)
        soup = BeautifulSoup(response.text, 'html.parser')


        date = soup.find("div", class_="caas-attr-time-style")
        date = date.find("time")["datetime"]
        date = date.split("T")[0]
        block = soup.find("div", class_="caas-body")

        texts = block.find_all("p")

        for t in texts:
            liste = str(t.find_all())
            if "class=" in liste or "href=" in liste:
                pass
            else:
                complete += t.text + "\n"
    except:
        print(url, "could not be read")
    return (date, complete)


if __name__ == "__main__":
    rater = articleRater()
    date, text = read_news("https://finance.yahoo.com/news/disney-ties-mood-messaging-contextual-095300363.html")
    print(date, text)
    print(rater.rate_article(text))
