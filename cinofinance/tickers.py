import pandas as pd
from params import TICKER_PATH_NYSE, TICKER_PATH_OTHER, TICKER_PATH_TOTAL

df1 = pd.read_csv(TICKER_PATH_NYSE)
df2 = pd.read_csv(TICKER_PATH_OTHER)
drop_columns = ['Security Name', 'Exchange', 'CQS Symbol', 'ETF', 'Round Lot Size', 'Test Issue', 'NASDAQ Symbol']
df2.drop(columns=drop_columns, axis=1, inplace=True)
result = df1.append(df2)
pd.DataFrame.to_csv(result, TICKER_PATH_TOTAL)
