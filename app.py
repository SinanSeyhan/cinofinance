import streamlit as st
from cinofinance.portfolio import Portfolio

# Get the Portfolio
portfolio = Portfolio().get_portfolio()


st.header('The Portfolio:')
st.table(portfolio)
