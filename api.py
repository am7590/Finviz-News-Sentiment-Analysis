from flask import Flask, request
import json, time
from datetime import datetime
from main import *
from scraper import *
from service import *


# How to the API locally from the terminal:
# export FLASK_APP=api.py
# python3 -m flask run

app = Flask(__name__)


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
    parsed_data = get_news_data(user_ticker)

    data_set = {'ticker': user_ticker, 'content': parsed_data, 'time_called': hour_min_sec}
    json_dump = json.dumps(data_set)

    return json_dump


@app.route('/sentiment/', methods=['GET'])
def get_average_compound():
    current_time = datetime.now()
    hour_min_sec = "%s:%s.%s" % (current_time.hour, current_time.minute, str(current_time.second)[:2])

    user_ticker = request.args.get('ticker', None)
    mean_df = get_sentiment_data(user_ticker)

    data_set = {'ticker': user_ticker, 'content': mean_df, 'time_called': hour_min_sec}
    json_dump = json.dumps(data_set)

    return json_dump
