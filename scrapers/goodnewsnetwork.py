"""Scraping script for goodnewsnetwork.com"""

from bs4 import BeautifulSoup

import requests
import sqlite3


def get_articles(url):
    """Returns article links, images, and titles as a list of dictionaries"""

    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, features="html.parser")

    posts = soup.find_all("div", {"class": "td-block-span6"})

    articles = []

    # Scrape the relevant data from the page
    for post in posts:
        link = post.find("a")["href"]
        image = post.find("img")["src"]
        title = post.find("a")["title"]

        articles.append({"link": link, "image": image, "title": title})

    return articles


if __name__ == "__main__":
    conn = sqlite3.connect("aggregator.db")
    c = conn.cursor()

    # Iterate through the most recent 200 articles (10 pages) and scrape
    for i in range(1, 11):
        url = "https://www.goodnewsnetwork.org/category/news/usa/page/{}/".format(i)
        articles = get_articles(url)

        # Catch sqlite3 exception if duplicate is found
        for article in articles:
            parameters = (4, article["link"], article["image"], article["title"])

            try:
                c.execute("""INSERT INTO articles (id, link, image, title)
                             VALUES (?,?,?,?)""", parameters)

            except sqlite3.IntegrityError:
                continue

    conn.commit()
    print("Scraping complete!")
