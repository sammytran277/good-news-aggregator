"""Scraping script for positive.news"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from string import capwords

import sqlite3


def get_articles(url):
    """Returns article links, images, and titles as a list of dictionaries"""

    # Set up driver, open URL, and wait for page to load
    driver = webdriver.Chrome()
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    # Get rid of the pop-up ad that blocks the load more button
    driver.find_element_by_css_selector(".btn--dismiss").click()

    # Press the load more button 19 times (120 articles in total)
    for i in range(19):
        driver.find_element_by_css_selector(".btn").click()
        sleep(1.5)

    # Find all the articles on the page
    posts = driver.find_elements_by_css_selector(".column.card")

    articles = []

    # Iterate through the articles and print the article link
    for post in posts:
        card_title = post.find_element_by_css_selector(".card__title")

        # Handle exception raised by partnered/featured articles
        try:
            img_element = post.find_element_by_css_selector(".card__image")

        except NoSuchElementException:
            img_element = post.find_element_by_css_selector(".featured__image")

        link = card_title.get_attribute("href")
        image = img_element.get_attribute("src")
        title = capwords(card_title.get_attribute("innerHTML"))

        # Fix title capitalization if the title starts with an apostrophe
        if title.startswith("‘"):
            title = fix_title(title)

        articles.append({"link": link, "image": image, "title": title})

    driver.quit()
    return articles


def fix_title(title):
    """Capitalize the first letter after a quotation mark"""

    fixed_title = []

    for letter in title:
        fixed_title.append(letter)

    # Capitalize the letter after the apostrophe
    fixed_title[1] = fixed_title[1].upper()

    return "".join(fixed_title)


if __name__ == "__main__":
    conn = sqlite3.connect("aggregator.db")
    c = conn.cursor()

    url = "https://www.positive.news/articles/"
    articles = get_articles(url)

    # Catch sqlite3 exception if duplicate is found
    for article in articles:
        parameters = (5, article["link"], article["image"], article["title"])

        try:
            c.execute("""INSERT INTO articles (id, link, image, title)
                            VALUES (?,?,?,?)""", parameters)

        except sqlite3.IntegrityError:
            continue

    conn.commit()
    print("Scraping complete!")
