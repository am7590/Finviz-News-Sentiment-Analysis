import requests
import pandas as pd
from bs4 import BeautifulSoup


def scrape_html_for_ticker(ticker):
    url = 'https://finviz.com/quote.ashx?t='

    # Get data for all tickers
    url = url + ticker
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36'

    # opening up connection and grabbing page
    response = requests.get(url, headers={
        'User-Agent': user_agent})
    html = BeautifulSoup(response.content, "html.parser")
    return html


def parse_data(ticker, html):
    # Parse response
    news_tables = {}
    # print(html)
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table  # Get each row of news data

    # Parse data further
    parsed_data = []
    news_date = ""
    # print(news_tables.items())

    for ticker, news_table in news_tables.items():
        href_url = ""

        for row in news_table.find_all('tr'):
            title = row.a.text
            date = row.td.text.split(' ')

            # Get time, date
            if len(date) == 1:
                time = date[0]
                date = news_date
            else:
                news_date = date[0]
                date = date[0]
                if len(date[1]) == 1:
                    time = row.td.text.split(' ')[1]

            # Get href link
            href_url = row.a["href"]

            # Get news Source
            span_text = row.span.getText()
            length = len(row.span.getText())
            source = span_text[:length:].strip()

            parsed_data.append([ticker, date, time, title, source, href_url])

    return parsed_data
