# from urllib.request import urlopen
import requests
import pandas as pd
from bs4 import BeautifulSoup
from nltk.sentiment import vader
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import time as t

from flask import Flask, request
from flask_cors import CORS
import json, time
from datetime import datetime

app = Flask(__name__)
CORS(app)


# Default GET
@app.route('/', methods=['GET'])
def default():
    current_time = datetime.now()
    hour_min_sec = "%s:%s.%s" % (current_time.hour, current_time.minute, str(current_time.second)[:2])

    data_set = {'type': 'none', 'content': 'Loaded the Finviz News Sentiment Analysis API', 'time_called': hour_min_sec}
    json_dump = json.dumps(data_set)

    return json_dump


@app.route('/news/', methods=['GET'])
def news():
    current_time = datetime.now()
    hour_min_sec = "%s:%s.%s" % (current_time.hour, current_time.minute, str(current_time.second)[:2])

    user_ticker = request.args.get('ticker', None)
    html = get_html_for_ticker(user_ticker)
    parsed_data = parse_data(user_ticker, html)
    df = make_dataframe_from_last_100_news_posts(parsed_data)

    data_set = {'ticker': user_ticker, 'content': parsed_data, 'time_called': hour_min_sec}
    json_dump = json.dumps(data_set)

    return json_dump


@app.route('/sentiment/', methods=['GET'])
def get_average_compound():
    current_time = datetime.now()
    hour_min_sec = "%s:%s.%s" % (current_time.hour, current_time.minute, str(current_time.second)[:2])

    user_ticker = request.args.get('ticker', None)
    html = get_html_for_ticker(user_ticker)
    parsed_data = parse_data(user_ticker, html)
    df = make_dataframe_from_last_100_news_posts(parsed_data)
    mean_df = get_mean_compound_scores(df)

    data_set = {'ticker': user_ticker, 'content': mean_df.to_json(), 'time_called': hour_min_sec}
    json_dump = json.dumps(data_set)

    return json_dump



def print_full_dataframe(df, head):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        if head:
            print(df.head())
        else:
            print(df)


def get_html_for_ticker(ticker):
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
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table  # Get each row of news data

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

    return parsed_data


def make_dataframe_from_last_100_news_posts(parsed_data):
    # Get sentiment analysis
    df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title'])
    sentiment = SentimentIntensityAnalyzer()
    f = lambda title: sentiment.polarity_scores(title)['compound']
    df['compound'] = df['title'].apply(f)

    # Modify date column
    df['date'] = pd.to_datetime(df.date).dt.date  # String -> Date format

    return df


def get_mean_compound_scores(df):
    # Get mean compound scores
    mean_df = df.groupby(["ticker", 'date']).mean()
    # rint_full_dataframe(mean_df, True)
    return mean_df


def chart_mean_compound_scores(mean_df):
    # Chart average compound scores with matplotlib
    mean_df = mean_df.unstack()
    mean_df = mean_df.xs('compound', axis="columns").transpose()
    mean_df.plot(kind='bar')
    plt.show()


def get_mean_data(ticker):
    html = get_html_for_ticker(ticker)
    parsed_data = parse_data(ticker, html)
    df = make_dataframe_from_last_100_news_posts(parsed_data)
    print_full_dataframe(df, False)

    mean_df = get_mean_compound_scores(df)
    print_full_dataframe(mean_df, False)
    chart_mean_compound_scores(mean_df)

    # print_full_dataframe(df, False)


if __name__ == '__main__':
    data = get_mean_data('GME')
    # app.run(host='0.0.0.0', port=8910)
