import streamlit as st
from datetime import date
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import yfinance as yf

from PIL import Image

st.set_page_config( page_title='Stock Dashboard' , page_icon="📈", layout="centered", initial_sidebar_state="auto", menu_items=None)

st.sidebar.info('This App is created to keep track of Stock Prices and Returns')

st.title('Stock Dashboard Application')
image = Image.open('stock_market_img.jpg')
resized_img = image.resize((800, 300))
st.image(resized_img)

stocks = ('GOOG', 'MSFT', 'DAR', 'AMD', 'ADBE','ABBV','AMZN','PG','PYPL','MU','NEE')
dropdown =st.multiselect('Select at least two stocks', stocks, default = ['GOOG', 'MSFT', 'DAR', 'AMD', 'ADBE','ABBV','AMZN','PG','PYPL','MU','NEE'])

start_date = pd.to_datetime('2020-01-01')
today = pd.to_datetime('today')

start = st.date_input('Start', value =start_date)
end = st.date_input('End', value =today)

if len(dropdown)>=1:
	data_close = yf.download(dropdown, start, end)['Adj Close']
	data_for_table = data_close

# Adj-Close Prices Table
st.subheader(' Adj-Close Prices')
st.dataframe(data=data_for_table) # inlcudes the index 0,1,... in the Table

# normalize data to 100 (Pt/P0)*100
norm_data = data_close/data_close.iloc[0]*100
st.subheader('Prices Normalized to 100')
st.line_chart(norm_data)

# calculate simple returns and plot -> (P1-P0)/P0
returns = (data_close / data_close.shift(1))-1
st.subheader('Daily Returns')
st.line_chart(returns)
## Histogram
st.subheader('Histogram of Daily Returns and Summary Statistics')
dropdown_2 =st.selectbox('Select your stocks', dropdown)
sns.set_style("darkgrid")
fig = plt.figure(figsize=(12, 8))
sns.histplot(returns[dropdown_2], kde = True)
st.pyplot()
st.set_option('deprecation.showPyplotGlobalUse', False)

statistics = returns[dropdown_2].describe().to_frame().transpose()
st.dataframe(data=statistics)

#Cumulative returns : https://www.investopedia.com/terms/c/cumulativereturn.asp, https://community.alteryx.com/t5/Alteryx-Designer-Discussions/Calculation-of-cumulative-returns/td-p/398284
def relative_returns(data_):
	rel = data_.pct_change()
	cumret= round( ((1+rel).cumprod()-1) *100,2)
	cumret = cumret.fillna(0)
	return cumret
st.subheader('Cumulative Returns')
st.line_chart(relative_returns(data_close))

# correlation between the stock returns
st.subheader('Stock Returns Correlations')
fig = plt.figure(figsize=(12, 8))
sns.heatmap(returns.corr(), cmap="YlGnBu", linewidths=.5,annot=True, linecolor='black')
st.pyplot(fig)