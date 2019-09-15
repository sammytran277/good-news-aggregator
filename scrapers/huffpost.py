"""Scraping script for positive.news"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from time import sleep
from helper import fix_title

import sqlite3


def get_links(url):
    """Returns article links as a list of dictionaries"""

    # Accept the certificate from huffpost.com to avoid errors
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    WebDriverWait(driver, 10)

    # Click the load more button 3 times to load more articles to scrape
    for i in range(3):
        driver.find_element_by_css_selector(".see-more").click()
        sleep(1.5)

    zones = driver.find_elements_by_css_selector(".zone__content")

    article_links = []

    # Iterate through the first and third zone, which has the articles we want
    for i in range(3):
        # Skip the second zone, which is the trending articles zone
        if i == 1:
            continue

        cards = zones[i].find_elements_by_css_selector(".card__image__link")

        # Get the link for each article in the zone
        for card in cards:
            link = card.get_attribute("href")
            article_links.append(link)

    driver.quit()
    return article_links


def get_articles(links):
    """Given article links, scrape info and return a list of dictionaries"""

    articles = []

    for link in links:

        #  Disguise request so we do not run into a 403 error
        req = Request(link, headers={"User-Agent": "Mozilla/5.0"})

        # Read HTML of the webpage
        try:
            webpage = urlopen(req).read()

        except HTTPError:
            exit("This URL caused an error:", link)

        soup = BeautifulSoup(webpage, "html.parser")

        image = soup.find("meta", {"property": "og:image"})["content"]
        title = fix_title(soup.find("meta", {"property": "og:title"})["content"])

        articles.append({"link": link, "image": image, "title": title})

    return articles


if __name__ == "__main__":
    conn = sqlite3.connect("aggregator.db")
    c = conn.cursor()

    url = "https://www.huffpost.com/impact/topic/good-news"
    links = get_links(url)
    articles = get_articles(links)

    # Catch sqlite3 exception if duplicate is found
    for article in articles:
        parameters = (6, article["link"], article["image"], article["title"])

        try:
            c.execute("""INSERT INTO articles (id, link, image, title)
                            VALUES (?,?,?,?)""", parameters)

        except sqlite3.IntegrityError:
            continue

    conn.commit()
    print("Scraping complete!")
