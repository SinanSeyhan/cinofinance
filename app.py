import streamlit as st
from datetime import datetime
from cinofinance.portfolio import Portfolio

# Get the Portfolio
portfolio = Portfolio().get_portfolio_dividend()

# Get the current month income
current_year = datetime.now().strftime('%Y')
current_month = datetime.now().strftime('%m')
current_time = current_year + '-' + current_month
monthly_income = round(sum(portfolio[current_time]), 2)
a = portfolio.sum(axis=0, numeric_only=True)

# Streamlit
st.header('The Portfolio:')
st.subheader(f'Total Dividend income for {current_time} is: {monthly_income} €')
st.table(a)
st.table(portfolio)
