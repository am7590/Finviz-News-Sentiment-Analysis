from matplotlib import pyplot as plt
from app import *
from service import *


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


def get_final_data(ticker):
    html = scrape_html_for_ticker(ticker)
    parsed_data = parse_data(ticker, html)
    df = make_dataframe_from_last_100_news_posts(parsed_data)
    # print_full_dataframe(df, False)

    mean_df = get_mean_compound_scores(df)
    print_full_dataframe(mean_df, False)
    chart_mean_compound_scores(mean_df)

    print_full_dataframe(df, False)


if __name__ == '__main__':
    get_final_data('GME')

