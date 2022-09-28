from flask import Flask, request
import requests
import json, time
from datetime import datetime
import nltk
from keys import token
from main import *

app = Flask(__name__)


# Default GET
@app.route('/', methods=['GET'])
def default():
    data_set = {'type': 'none', 'content': 'Loaded the Finviz News Sentiment Analysis API'}
    json_dump = json.dumps(data_set)

    return json_dump


@app.route('/news/', methods=['GET'])
def news():
    ticker = request.args.get('ticker', None)
    url = f'https://cloud.iexapis.com/stable/stock/{ticker}/news/last/100/?token={token}'
    return json.dumps(requests.get(url).json())


@app.route('/sentiment/', methods=['GET'])
def get_average_compound():
    ticker = request.args.get('ticker', None)
    print(get_final_data(ticker)[0])
    print(get_final_data(ticker)[1])
    data_set = {'content': get_final_data(ticker)[0], 'type': get_final_data(ticker)[1]}
    return json.dumps(data_set)


@app.route('/welcome/', methods=['GET'])
def get_welcome_page_data():
    date = request.args.get('date', None)
    calendar = welcome_status(date)[1]
    print(calendar.date)

    data_set = {'status': welcome_status(date)[0],
                'open-date': calendar.date.strftime("%m/%d/%Y"),
                'open-time': calendar.open.strftime("%H:%M:%S"),
                'open-close': calendar.close.strftime("%H:%M:%S")
                }

    print(data_set)
    print(json.dumps(data_set))
    return json.dumps(data_set)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
