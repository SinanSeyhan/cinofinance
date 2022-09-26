import os
import pandas as pd
from openpyxl import load_workbook


class Portfolio():
    def __init__(self) -> None:
        my_path = os.path.abspath(os.path.dirname(__file__))
        self.PORTFOLIO_PATH = os.path.join(my_path, '../raw_data/portfolio.xlsx')

    def get_portfolio(self):
        global portfolio
        portfolio = []
        # Load the workbook, from the filename, setting read_only to False
        wb = load_workbook(filename=self.PORTFOLIO_PATH, read_only=False, keep_vba=False, data_only=True, keep_links=False)

        # Initialize the dictionary of tables
        tables_dict = {}

        # Go through each worksheet in the workbook
        for ws_name in wb.sheetnames:

            ws = wb[ws_name]

            # Get each table in the worksheet
            for tbl in ws.tables.values():
                # First, add some info about the table to the dictionary
                tables_dict[tbl.name] = {
                        'table_name': tbl.name,
                        'worksheet': ws_name,
                        'num_cols': len(tbl.tableColumns),
                        'table_range': tbl.ref}

                # Grab the 'data' from the table
                data = ws[tbl.ref]

                # Now convert the table 'data' to a Pandas DataFrame
                # First get a list of all rows, including the first header row
                rows_list = []
                for row in data:
                    # Get a list of all columns in each row
                    cols = []
                    for col in row:
                        cols.append(col.value)
                    rows_list.append(cols)

                # Create a pandas dataframe from the rows_list.
                # The first row is the column names
                df = pd.DataFrame(data=rows_list[1:], index=None, columns=rows_list[0])

                # Add the dataframe to the dictionary of tables
                tables_dict[tbl.name]['dataframe'] = df
        # a dictionary of all tables in the Excel workbook
        portfolio = tables_dict['Table1']['dataframe']
        portfolio = portfolio.set_index('Tickers').dropna(axis='columns', how='all')
        return portfolio



if __name__=='__main__':
    df = Portfolio().get_portfolio()
    print(df)
