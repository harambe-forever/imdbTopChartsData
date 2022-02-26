import requests
from bs4 import BeautifulSoup as soup
import pandas as pd


def main():
    doc = get_page("https://www.imdb.com/chart/top/")
    data = get_data(doc)
    plot(data)


def get_page(url):
    page = requests.get(url, headers={
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'})
    doc = soup(page.content, "html.parser")
    return doc


def get_data(doc):
    body = doc.body
    wrapper = body.find(id="wrapper")
    main = wrapper.find(id="main")
    article = main.find(class_="article")
    lister = article.find(class_="lister")
    table = lister.table
    tbody = table.tbody
    titleDir = tbody.find_all(class_="titleColumn")
    titleRank = tbody.find_all(class_="ratingColumn imdbRating")
    titleData = {}
    for i in range(len(titleDir)):
        movieTitle = titleDir[i].a.string
        movieYear = titleDir[i].find(class_="secondaryInfo").string
        movieRank = titleRank[i].strong.string
        """print("title:", movieTitle, " year:",
              movieYear, " movie rank:", movieRank)"""
        key = movieTitle + " " + movieYear
        titleData[key] = movieRank
    return titleData


def plot(titleData):
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    df = pd.DataFrame(list(titleData.items()), columns=["Movie", "Rank"])
    print(df)


main()
