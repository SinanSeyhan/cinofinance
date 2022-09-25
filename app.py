import streamlit as st
from cinofinance.dividend import Dividend

# Get the Portfolio
portfolio = Dividend().get_portfolio()


st.header('The Portfolio:')
st.table(portfolio)
