from calendar import month
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
        return amount * CurrencyRates().get_rates('USD')['EUR']

    def get_dividends(self):



        df = pd.read_csv(self.TICKER_PATH_TOTAL)
        # df = df.sample(n=10)
        symbol = list(df['Symbol'])
        divs = []
        for key in symbol:
            try:
                temp = yf.Ticker(key)
                temp.history(period='1y')
                divs.append((temp.dividends))
            except:
                print('No data found in Yahoo Finance')
        df2 = pd.DataFrame(divs, index=symbol)
        df2.columns = df2.columns.month
        df2 = df2.groupby(df2.columns, axis=1).sum()
        df2.columns = [dt.date(1900,i,1).strftime('%b') for i in df2.columns]

        price = [yf.download(i, period='1d')['Adj Close'].values[0] for i in symbol]
        df2['Price'] = price
        total_columns = list(df2.columns)
        month_columns = total_columns[:-1]

        df2[total_columns] = df2[total_columns].apply(self.usd2eur)
        brutto2netto = 0.855
        df2[month_columns] = df2[month_columns] * brutto2netto
        df2['ROI, annual'] = df2[month_columns].sum(axis=1) / df2['Price']
        df2 = df2.sort_values('ROI, annual', ascending=False)


        return df2

    def get_portfolio_dividends(self, portfolio):
        '''
        Function that gives you a dataframe of the dividends, names and ROI of passed dictionary.

        portfolio: dict, with tickers as keys and lot size as values.
        '''
        total_columns = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Price']
        month_columns = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

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
            divs.append(temp.dividends) # * value)) --> For getting the lot size
        df2 = pd.DataFrame(divs, index=portfolio)
        df2.columns = df2.columns.month
        df2 = df2.groupby(df2.columns, axis=1).sum()
        df2.columns = [dt.date(1900,i,1).strftime('%b') for i in df2.columns]
        # Merge the dataframes
        result = df.merge(df2, left_index=True, right_index=True)

        #get price information
        price = [yf.download(i, period='1d')['Adj Close'].values[0] for i in portfolio.keys()]
        result['Price'] = price

        # Convert to EUR
        result[total_columns] = result[total_columns].apply(self.usd2eur)
        brutto2netto = 0.855
        result[month_columns] = result[month_columns] * brutto2netto
        result
        result['ROI, annual'] = result[month_columns].sum(axis=1) / result['Price']
        result = result.sort_values('ROI, annual', ascending=False)

        return round(result, 5)


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
