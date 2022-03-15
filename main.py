# from urllib.request import urlopen
import requests
import pandas as pd
from bs4 import BeautifulSoup
from nltk.sentiment import vader
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import time as t


def print_full_dataframe(df, head):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        if head:
            print(df.head())
        else:
            print(df)


def run_script():
    url = 'https://finviz.com/quote.ashx?t='
    ticker = 'TSLA'
    news_tables = {}

    # Get data for all tickers
    url = url + ticker
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36'

    # opening up connection and grabbing page
    response = requests.get(url, headers={
        'User-Agent': user_agent})
    html = BeautifulSoup(response.content, "html.parser")

    # Parse response
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table  # Get each row of news data
    print("adding: ", news_tables)
    # break  # only scrape 1 ticker

    # Test output for TSLA
    # tsla_data = news_tables['TSLA']
    # tsla_rows = tsla_data.findAll('tr')
    # print(tsla_rows)

    # Parse data further
    parsed_data = []
    news_date = ""

    for ticker, news_table in news_tables.items():
        for row in news_table.find_all('tr'):
            title = row.a.text
            date = row.td.text.split(' ')

            if len(date) == 1:
                time = date[0]
                date = news_date
            else:
                news_date = date[0]
                date = date[0]
                if len(date[1]) == 1:
                    time = row.td.text.split(' ')[1]

            parsed_data.append([ticker, date, time, title])

    # Get sentiment analysis
    df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title'])
    sentiment = SentimentIntensityAnalyzer()
    f = lambda title: sentiment.polarity_scores(title)['compound']
    df['compound'] = df['title'].apply(f)

    # Modify date column
    df['date'] = pd.to_datetime(df.date).dt.date  # String -> Date format

    # Get mean compound scores
    mean_df = df.groupby(["ticker", 'date']).mean()
    print_full_dataframe(mean_df, True)

    # Chart average compound scores with matplotlib
    mean_df = mean_df.unstack()
    mean_df = mean_df.xs('compound', axis="columns").transpose()
    mean_df.plot(kind='bar')
    plt.show()

    # print_full_dataframe(df, False)


if __name__ == '__main__':
    run_script()
