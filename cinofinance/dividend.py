import pandas as pd
import datetime as dt
import os

import yfinance as yf
from forex_python.converter import CurrencyRates


class Dividend():
    def __init__(self):
        my_path = os.path.abspath(os.path.dirname(__file__))
        global TICKER_PATH_TOTAL
        self.TICKER_PATH_TOTAL = os.path.join(my_path, '../raw_data/nasdaq_screener.csv')

    def usd2eur(self, amount):
        '''
        Function that converts US Dollars to EUR

        amount: float, US Dollars to convert
        '''
        brutto2netto = 0.855
        return (amount * brutto2netto) * CurrencyRates().get_rates('USD')['EUR']

    def get_dividends(self):



        df = pd.read_csv(self.TICKER_PATH_TOTAL)

        divs = []
        for key in df['ACT Symbol']:
            temp = yf.Ticker(key)
            temp.history(period='1y')
            divs.append(temp.dividends)
        return divs

    def get_portfolio_dividends(self, portfolio):
        '''
        Function that gives you the dividends, names of passed dictionary.

        portfolio: dict, with tickers as keys and lot size as values.
        '''

        # Load the portfolio
        df = pd.DataFrame([portfolio]).T
        df.rename({0:'Lot'}, axis=1, inplace=True)

        # get the names of stocks
        df_tickers = pd.read_csv(self.TICKER_PATH_TOTAL)
        names = df_tickers[df_tickers['Symbol'].isin(list(portfolio.keys()))].iloc[:, 0:2].set_index('Symbol')
        df = df.join(names)

        # Get the Dividends
        divs = []
        for key, value in portfolio.items():
            temp = yf.Ticker(key)
            temp.history(period='1y')
            divs.append(self.usd2eur(temp.dividends * value))
        df2 = pd.DataFrame(divs, index=portfolio)
        df2.columns = df2.columns.month
        df2 = df2.groupby(df2.columns, axis=1).sum()
        df2.columns = [dt.date(1900,i,1).strftime('%b') for i in df2.columns]
        # Merge the dataframes
        result = df.merge(df2, left_index=True, right_index=True)

        #get price information
        price = [yf.download(i, period='1d')['Adj Close'].values[0] for i in portfolio.keys()]
        result['Price'] = price
        return result


if __name__=='__main__':
    # portfolio = {
    #             'NVDA': 2, # NVIDIA
    #             'STAG': 9, # STAG
    #             'MCO': 1, # MOODY'S
    #             'MSFT': 1, # MICROSOFT
    #             'AGNC': 20, # AGNC INVESTMENT
    #             'V': 1, # VISA
    #             'BNTX': 1, # BIONTECH
    #             }

    # df = Dividend().get_portfolio_dividends(portfolio)
    # print(df)
    df = Dividend().get_dividends()
    print(df.columns)
