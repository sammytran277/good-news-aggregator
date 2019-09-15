"""Scraping script for today.com"""

from bs4 import BeautifulSoup
from helper import fix_title

import requests
import sqlite3


def get_articles(url):
    """Returns article links, images, and titles as a list of dictionaries"""

    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, features="html.parser")

    posts = soup.find_all("a", {"class": "vilynx_disabled"})

    # Create a variable to store all article links
    post_links = []

    # Iterate through each anchor tag
    for post in posts:

        # Check that the anchor tag is indeed an article link
        if is_article(post_links, post):
            post_links.append(post["href"])

    articles = []

    # Iterate through each link to get the post image and title from the links
    for link in post_links:
        page = requests.get(link)
        page_content = page.content
        soup = BeautifulSoup(page_content, features="html.parser")\

        image = soup.find("meta", {"property": "og:image"})["content"]
        title = fix_title(soup.find("title").text)

        articles.append({"link": link, "image": image, "title": title})

    return articles


def is_article(post_links, post):
    """Checks that an article is valid and returns a bool"""

    # Return false if post is a section of today.com
    if post["href"].count("-") < 4:
        return False

    # Return False if post is a video
    elif "video" in post["href"]:
        return False

    # Return False if post is already in post_links
    elif post["href"] in post_links:
        return False

    # If all checks pass, return True
    else:
        return True


if __name__ == "__main__":
    conn = sqlite3.connect("aggregator.db")
    c = conn.cursor()

    url = "https://www.today.com/news/good-news"
    articles = get_articles(url)

    # Iterate through articles and insert into database if not a duplicate
    for article in articles:
        parameters = (2, article["link"], article["image"], article["title"])

        # Catch sqlite3 exception if duplicate is found
        try:
            c.execute("""INSERT INTO articles (id, link, image, title)
                        VALUES (?,?,?,?)""", parameters)

        except sqlite3.IntegrityError:
            continue

    conn.commit()
    print("Scraping complete!")
