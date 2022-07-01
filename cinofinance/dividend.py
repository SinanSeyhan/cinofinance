import yfinance as yf
import pandas as pd
import datetime as dt
from forex_python.converter import CurrencyRates

def usd2eur(amount):
    brutto2netto = 0.855
    return (amount * brutto2netto) * CurrencyRates().get_rates('USD')['EUR']

def get_dividends(tickers):
    divs = []
    for key, value in tickers.items():
        temp = yf.Ticker(key)
        temp.history(period='1y')
        divs.append(temp.dividends * value)
    df = pd.DataFrame(divs, index=tickers)
    df.columns = df.columns.month
    df = df.groupby(df.columns, axis=1).sum()
    df.columns = [dt.date(1900,i,1).strftime('%b') for i in df.columns]
    df['Lot'] = df.index.map(tickers)
    # name = [yf.Ticker(i).info['longName'] for i in tickers.keys()]
    # df['Name'] = name
    price = [yf.download(i, period='1d')['Adj Close'].values[0] for i in tickers.keys()]
    df['Price'] = price
    #df = df[['Name', 'Price', 'Lot', 'Jan', 'Feb', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]
    df = usd2eur(df.select_dtypes(include='float'))
    return df

if __name__=='__main__':
    portfolio = {
                'NVDA': 2, # NVIDIA
                'STAG': 9, # STAG
                'MCO': 1, # MOODY'S
                'MSFT': 1, # MICROSOFT
                'AGNC': 18, # AGNC INVESTMENT
                'V': 1, # VISA
                'BNTX': 1, # BIONTECH
                }

    df = get_dividends(portfolio)
    print(df)
