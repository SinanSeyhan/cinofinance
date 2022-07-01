import os

my_path = os.path.abspath(os.path.dirname(__file__))



TICKER_PATH_NYSE = os.path.join(my_path, '../raw_data/nyse-listed.csv')

TICKER_PATH_OTHER = os.path.join(my_path, '../raw_data/other-listed.csv')

TICKER_PATH_TOTAL = os.path.join(my_path, '../raw_data/total_tickers.csv')
