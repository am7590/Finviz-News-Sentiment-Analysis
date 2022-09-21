from matplotlib import pyplot as plt
from app import *
import requests
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import datetime
from itertools import groupby
from operator import itemgetter
from collections import Counter


def print_full_dataframe(df, head):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        # Display just the last few lines or the whole df?
        if head:
            print(df.head())
        else:
            print(df)


def chart_mean_compound_scores(mean_df):
    # Chart average compound scores with matplotlib
    mean_df = mean_df.unstack()
    mean_df = mean_df.xs('compound', axis="columns").transpose()
    mean_df.plot(kind='bar')
    plt.show()


def get_date(s):
    return datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f')


def consecutive_groups(iterable, ordering=lambda x: x):
    for k, g in groupby(enumerate(iterable), key=lambda x: x[0] - ordering(x[1])):
        yield map(itemgetter(1), g)


def flatten(l):
    return [item for sublist in l for item in sublist]


def get_final_data(ticker):
    url = f'https://cloud.iexapis.com/stable/stock/{ticker}/news/last/100/?token={token}'
    data = requests.get(url).json()
    print(data)
    sentiment = SentimentIntensityAnalyzer()

    date_list = []
    for item in data:
        date_list.append(item['datetime'])

    dates = [get_date(i/1000) for i in date_list]
    print(dates)

    day_lists = [[] for _ in range(5)]  # [[], [], ..., []]
    hour_lists = [[] for _ in range(10)]
    current_date = ''
    current_list_index = 0
    key_count = len(Counter([item.split('-')[1] for item in dates]).keys())
    print(key_count)
    if key_count < 5:
        print("splitting dates by hour of last day")
        for item in dates:
            if len(current_date) == 0:
                current_date = item.split(' ')[1][0:3]
                hour_lists[current_list_index].append(item)
            elif current_date == item.split(' ')[1][0:3]:
                hour_lists[current_list_index].append(item)
            else:
                current_list_index += 1
                if current_list_index > 4:
                    break
                current_date = item.split(' ')[1][0:3]
                hour_lists[current_list_index].append(item)
    else:
        print("split by date")
        for item in dates:
            if len(current_date) == 0:
                 current_date = item.split('-')[1]+item.split('-')[2][0:3]
                 day_lists[current_list_index].append(item)
            elif current_date == item.split('-')[1]+item.split('-')[2][0:3]:
                day_lists[current_list_index].append(item)
            else:
                current_list_index += 1
                if current_list_index > 4:
                    break
                current_date = item.split('-')[1]+item.split('-')[2][0:3]
                day_lists[current_list_index].append(item)

    print(hour_lists)
    print(day_lists)

    find_sentiment_list = []

    for item in data:
        for hour_list in hour_lists:
            for hour in hour_list:
            # print(get_date(item['datetime']/1000))
            # print(hour)
                if get_date(item['datetime']/1000) == hour:
                    find_sentiment_list.append(item)
                    print(item)

    for item in data:
        for day_list in day_lists:
            for day in day_list:
                if get_date(item['datetime'] / 1000) == day:
                    find_sentiment_list.append(item)
                    print(item)

    sentiment_score_list = []
    for item in find_sentiment_list:
        sentiment_score_list.append(sentiment.polarity_scores(item['summary'])['compound'])

    print(sentiment_score_list)
    # print([len(x) for x in sentiment_score_list])

    final_score_list = []
    type = ''
    if len(hour_lists[0]) > 0:
        final_score_list = hour_lists
        type = 'hours'
    else:
        final_score_list = day_lists
        type = "days"

    print(final_score_list)
    print([len(x) for x in final_score_list])

    return dict(zip(flatten(final_score_list), sentiment_score_list)), type


if __name__ == '__main__':
    get_final_data('TSLA')

