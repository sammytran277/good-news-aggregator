from flask import Flask, render_template, request, flash
from random import shuffle

import sqlite3

app = Flask(__name__)


@app.route("/")
def index():
    """Landing page with all the scraped news articles"""

    # Get articles and random quote by calling their respective functions
    articles = lookup_articles()
    quote = get_quote()

    return render_template("index.html", quote=quote, articles=articles)


@app.route("/about")
def about():
    """About page with basic information about the app"""

    return render_template("about.html")


@app.route("/search")
def search():
    """Search results page with filtered content"""

    keyword = request.args.get("q")
    all_articles = lookup_articles()
    filtered_articles = []

    # Iterate through all articles and check if keyword is in the title
    for article in all_articles:
        title = article["title"]

        # Compare keyword to each word in the article's title
        if keyword in title.split() or keyword.capitalize() in title.split():
            filtered_articles.append(article)

    return render_template("search.html",
                           num_of_articles=len(filtered_articles),
                           keyword=keyword,
                           articles=filtered_articles)


def lookup_articles():
    """Looks up articles from the database"""

    # Connect to SQLite database
    conn = sqlite3.connect("aggregator.db")
    c = conn.cursor()

    articles = []

    # Add each article as a dictionary to the articles list
    for article in c.execute("SELECT link, image, title FROM articles"):
        articles.append({"link": article[0],
                         "image": article[1],
                         "title": article[2]})

    shuffle(articles)
    return articles


def get_quote():
    """Returns a random quote to be displayed on the page"""

    # Connect to SQLite database
    conn = sqlite3.connect("aggregator.db")
    c = conn.cursor()

    # Get a random quote from the database and return it
    for quote in c.execute("SELECT quote FROM quotes ORDER BY RANDOM() LIMIT 1"):
        return quote[0]
