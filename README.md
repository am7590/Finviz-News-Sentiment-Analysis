# Finviz-News-Sentiment-Analysis-API
Uses Finviz to scrape the last 100 news articles for any stock ticker and performs sentiment analysis on their titles using Natural Language Toolkit- Vader.
It finds the compound score, which is a normalized value between -1 (negative) and 1 (positive). 

# Example News get request: /news/?ticker=tsla
```{"ticker": "tsla", 
  "content": [
    ["tsla", "Mar-15-22", "12:18AM", "UPDATE 2-Tesla raises China, U.S. prices for second time within a week", "Reuters", "https://finance.yahoo.com/news/1-tesla-increases-prices-china-041832881.html"], 
    ["tsla", "Mar-14-22", "11:45PM", "Tesla raises China, U.S. prices for second time within a week", "Reuters", "https://finance.yahoo.com/news/tesla-raises-prices-china-made-034550995.html"], 
    ["tsla", "Mar-14-22", "10:37PM", "Dow Jones Futures: Nasdaq Breaks Lower; China Covid Shutdowns Are New X Factor", "Investor's Business Daily", "https://www.investors.com/market-trend/stock-market-today/dow-jones-futures-nasdaq-breaks-lower-amid-china-covid-shutdowns-what-to-do-now/?src=A00220"], 
    ... 97 more rows...
   ], 
   "time_called": "2:25.54"
 }
```

# Example Sentiment get request: /sentiment/?ticker=tsla
```{"ticker": "tsla", 
  "content": {
    "Mar-15-22": 0.0, 
    "Mar-14-22": -0.1027, 
    "Mar-13-22": 0.1779, 
    "Mar-12-22": 0.743, 
    "Mar-11-22": 0.0772, 
    "Mar-10-22": 0.0, 
    "Mar-09-22": -0.1531
   }, 
   "time_called": "2:28.18"}
```

# Run locally (Flask)
1. ```export FLASK_APP=api.py```
2. ```python3 -m flask run```
