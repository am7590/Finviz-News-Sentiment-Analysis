from main import *
from scraper import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from scraper import scrape_html_for_ticker, parse_data


def make_dataframe_from_last_100_news_posts(parsed_data):
    # Get sentiment analysis
    df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title', 'source', 'href_url'])
    sentiment = SentimentIntensityAnalyzer()
    f = lambda title: sentiment.polarity_scores(title)['compound']
    df['compound'] = df['title'].apply(f)

    # Modify date column
    # df['date'] = pd.to_datetime(df.date).dt.date  # String -> Date format

    return df


def get_mean_compound_scores(df):
    # Get mean compound scores
    mean_df = df.groupby(["ticker", 'date']).mean()
    # rint_full_dataframe(mean_df, True)
    return mean_df


def get_news_data(user_ticker):
    html = scrape_html_for_ticker(user_ticker)
    parsed_data = parse_data(user_ticker, html)
    for item in parsed_data:
        item[2] = item[2].strip()

    return parsed_data


def get_sentiment_data(user_ticker):
    html = scrape_html_for_ticker(user_ticker)
    parsed_data = parse_data(user_ticker, html)
    df = make_dataframe_from_last_100_news_posts(parsed_data)
    # mean_df = get_mean_compound_scores(df)

    list_of_dates = df['date'].tolist()
    list_of_compound = df['compound'].tolist()

    return dict(zip(list_of_dates, list_of_compound))
