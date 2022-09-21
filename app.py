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
    # print(get_final_data(ticker))
    data_set = {'content': get_final_data(ticker)[0], 'type': get_final_data(ticker)[1]}
    return json.dumps(data_set)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4200)
