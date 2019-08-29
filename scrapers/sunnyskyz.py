"""Scraping script for sunnyskyz.com"""

from bs4 import BeautifulSoup

import requests
import sqlite3


def get_articles(url):
    """Returns article links, images, and titles as a list of dictionaries"""

    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, features="html.parser")

    posts = soup.find_all("a", {"class": "newslist"})

    articles = []

    # Scrape the relevant data from the page
    for post in posts:
        link = "https://www.sunnyskyz.com" + post["href"]
        image = post.find("img")["src"]
        title = post.find("p", {"class": "titlenews"}).text

        articles.append({"link": link, "image": image, "title": title})

    return articles


if __name__ == "__main__":
    conn = sqlite3.connect("aggregator.db")
    c = conn.cursor()

    # Iterate through the most recent 176 articles (11 pages) and scrape
    for i in range(0, 161, 16):
        url = "https://www.sunnyskyz.com/positive-good-news.php?week=pastweek&start={}".format(i)
        articles = get_articles(url)

        # Catch sqlite3 exception if duplicate is found
        for article in articles:
            parameters = (3, article["link"], article["image"], article["title"])

            try:
                c.execute("""INSERT INTO articles (id, link, image, title)
                             VALUES (?,?,?,?)""", parameters)

            except sqlite3.IntegrityError:
                continue

    conn.commit()
    print("Scraping complete!")
