"""Scraping script for thehappybroadcast.com"""

from bs4 import BeautifulSoup

import requests
import sqlite3


def get_articles(url):
    """Returns article links and images as a list of dictionaries"""

    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, features="html.parser")

    # Find the photo divs, which have the article links and images
    posts = soup.find_all("div", {"class": "photo"})

    articles = []

    # Iterate through each photo div to get each article link and image
    for post in posts:
        link = post.find("div", {"class": "to_post"}).find("a")["href"]
        image = post.find("img")["src"]

        articles.append({"link": link, "image": image})

    return articles


if __name__ == "__main__":
    conn = sqlite3.connect("aggregator.db")
    c = conn.cursor()

    # Iterate through the first 20 pages of the site and scrape their articles
    for i in range(1, 21):
        url = "https://www.thehappybroadcast.com/page/{}".format(i)
        articles = get_articles(url)

        # Catch sqlite3 exception if duplicate is found
        for article in articles:
            try:
                parameters = (1, article["link"], article["image"])
                c.execute("""INSERT INTO articles (id, link, image)
                             VALUES (?,?,?)""", parameters)

            except sqlite3.IntegrityError:
                continue

    conn.commit()
    print("Scraping complete!")
