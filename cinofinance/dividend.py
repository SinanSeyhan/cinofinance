import pandas as pd
import datetime as dt
from datetime import datetime
import os
import numpy as np
from cinofinance.portfolio import Portfolio
import yfinance as yf
from forex_python.converter import CurrencyRates

from paths import *


class Dividend():
    def __init__(self):

        self.TICKER_PATH_TOTAL = TICKER_PATH_TOTAL
        self.POOL_PATH = POOL_PATH
        self.POOL_FINAL = POOL_FINAL


        # Pool for Stock picking
        tickers = pd.read_csv(self.POOL_PATH).to_dict('list')['Tickers']


        self.pool = dict(zip(tickers, [1] * len(tickers)))

    def get_dividends(self, portfolio):
        '''
        Function that gives you a dataframe of the dividends, names and ROI of passed dictionary.

        portfolio: dict, with tickers as keys and lot size as values as user input.
        '''
        global month_columns
        total_columns = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Price']
        month_columns = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        brutto2netto = 0.855

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

        # Add TAX
        result[month_columns] = result[month_columns] * brutto2netto

        # Convert $ to €
        rate = CurrencyRates().get_rate(base_cur='USD', dest_cur='EUR')
        result[month_columns] = result[month_columns] * rate


        # Add annual Dividends and ROI
        result['Dividend, annual'] = result[month_columns].sum(axis=1)
        result['ROI, annual'] = result['Dividend, annual'] / result['Price']

        # Sort the dataframe
        result = result.sort_values('ROI, annual', ascending=False)

        return round(result, 5)

    def get_portfolio_dividends(self, portfolio):
        '''
        Gives a dataframe that is multiplicated with Lot size.

        portfolio: Dictionary
        '''
        df = self.get_dividends(portfolio)


        # Multiplying the Lot Size
        df[month_columns] = df[month_columns].multiply(df['Lot'], axis='index')
        df['Dividend, annual'] = df[month_columns].sum(axis=1)

        # Total Row
        df.loc["Total"] = df.sum(numeric_only=True)
        df.loc["Total", 'Price'] = 0
        df.loc["Total", 'Lot'] = 0
        df.loc["Total", 'ROI, annual'] = 0
        df.fillna(0, inplace=True)

        # Total income of the portfolio
        total = round(df.loc['Total', 'Dividend, annual'], 2)
        print(' ')
        print('#'*70)
        print(f'# The Total Annual Dividend Income of the portfolio is: {total} EUR     #')
        print('#'*70)
        print(' ')

        # Total Montly income
        current_month = datetime.now().strftime('%h')
        monthly = round(df.loc['Total', current_month], 2)
        print(' ')
        print('#'*70)
        print(f'# The Total Dividend Income for {current_month} of the portfolio is: {monthly} EUR      #')
        print('#'*70)
        print(' ')


        return df

    def get_dividend_pool(self, capital):

        '''
        Gives a dataframe from the pool
        '''
        df = self.get_dividends(self.pool)
        df['Lot'] = (capital / df['Price'])
        df['Lot'] = df['Lot'].apply(np.floor)

        month_columns = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        df[month_columns] = df[month_columns].multiply(df['Lot'], axis='index')
        df['Dividend, annual'] = df[month_columns].sum(axis=1)


        df.sort_values('Dividend, annual', ascending=False)
        df.to_csv(self.POOL_FINAL)
        return df

    def get_final_pool(self):
        df = pd.read_csv(self.POOL_FINAL)
        return df

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

    import portfolio

    portfolio_data = portfolio.Portfolio().get_portfolio()[['2023-05']]

    portfolio_dict = portfolio_data['2023-05'].to_dict()

    print(portfolio_dict)
    df = Dividend().get_portfolio_dividends(portfolio_dict)
    print(df)
    rate = CurrencyRates().get_rate(base_cur='USD', dest_cur='EUR')
    print(rate)
    # df = Dividend().get_dividend_pool(100)
    # print(df.columns)
