!/usr/bin/env python
# coding: utf-8

# # Finance Data Project 
# 
# In this data project we will focus on exploratory data analysis of stock prices.
# We'll focus on bank stocks and see how they progressed throughout the [financial crisis](https://en.wikipedia.org/wiki/Financial_crisis_of_2007%E2%80%9308) all the way to early 2016.

# TO SEE A MORE DETAILED VIEW, SEE 
' https://salgadomichael.com/finance-project '

# ## Getting the Data
# In this section we will use pandas to directly read data from Yahoo finance using pandas

# ### The Imports

# In[128]:
from pandas_datareader import data, wb
import pandas as pd
import numpy as np
from datetime import datetime
import yfinance as yf
import os
yf.pdr_override()
get_ipython().run_line_magic('matplotlib', 'inline')

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
get_ipython().run_line_magic('matplotlib', 'inline')

import plotly
import cufflinks as cf
cf.go_offline()


# ## Data

# We need to get data using pandas datareader. We will get stock information for the following banks:
# *  Bank of America
# * CitiGroup
# * Goldman Sachs
# * JPMorgan Chase
# * Morgan Stanley
# * Wells Fargo

# Initializing start and end datetime constants

# In[129]:
start = datetime(2006, 1, 1)
end = datetime(2016, 1, 1)


# Importing data for each stock

# In[150]:
BAC = data.get_data_yahoo('BAC', start, end)
C = data.get_data_yahoo('BAC', start, end)
GS = data.get_data_yahoo('GS', start, end)
JPM = data.get_data_yahoo('JPM', start, end)
MS = data.get_data_yahoo('MS', start, end)
WF = data.get_data_yahoo('WFC', start, end)


# Checking the head

# In[156]:
BAC.head()

# In[157]:
C.head()


# We'll create a list of the ticker symbols (as strings) in alphabetical order.

# In[158]:
tickers = ['BAC','C','GS','JPM','MS','WF']


# We'll concatenate the bank dataframes together to a single data frame called bank_stocks. Then, we'll set the keys argument equal to the tickers list.

# In[159]:
bank_stocks = pd.concat(keys=tickers, axis=1, objs=[BAC, C, GS, JPM, MS, WF])


# Setting the column name levels

# In[160]:
bank_stocks.columns.names = ['Bank Ticker','Stock Info']


# Checking the head of the bank_stocks dataframe

# In[161]:
bank_stocks.head()


# # Exploratory Data Analysis
# 
# Let's explore the data a bit.
# 
# We'll figure out the max close price for each bank's stock throughout the time period

# In[162]:
bank_stocks.xs(key='Close', axis=1, level=1).max()


# Let's create a new empty DataFrame called returns. This dataframe will contain the returns for each bank's stock.

# In[163]:
returns = pd.DataFrame()


# We can use pandas pct_change() method on the Close column to create a column representing this return value, then create a for loop that goes and for each Bank Stock Ticker creates this returns column and set's it as a column in the returns DataFrame.

# In[164]:
for i in tickers:
    returns[i + ' Returns'] = bank_stocks[i]['Close'].pct_change()
returns.head()


# Creating a pairplot using seaborn of the returns dataframe.
# 
# As we can see there is one stock that stands out.

# In[165]:
sns.pairplot(returns)


# Using this returns DataFrame, let's figure out on what dates each bank stock had the best and worst single day returns. 
# 
# Noticeably, 4 of the banks share the same day for the worst drop. January 20th, 2009, or Inauguration day.

# In[166]:
returns.idxmin()


# In[167]:
returns.idxmax()


# We also notice that Citigroup's largest drop and biggest gain were close to eachother. This was because Citigroup had a stock split
# When we take a look at the standard deviation of the returns, Citigroup seems to be the riskiest

# In[168]:
returns.std()


# In[169]:
returns.loc['2015-01-01':'2015-12-31'].std()


# Let's create a distplot using seaborn of the 2015 returns for Morgan Stanley

# In[170]:
sns.distplot(returns.loc['2015-01-01':'2015-12-31']['MS Returns'], bins=100, color='green')


# Let's create a distplot using seaborn of the 2008 returns for CitiGroup

# In[171]:
sns.distplot(returns.loc['2008-01-01':'2008-12-31']['C Returns'], bins=100, color='red')


# # More Visualization
# Let's create a line plot showing Close price for each bank for the entire index of time.

# In[174]:
bank_stocks.xs(key='Close', axis=1, level=1).plot(figsize=(12,4))


# In[173]:
bank_stocks.xs('Close', 1, 1).plot()


# ## Moving Averages
# Let's analyze the moving averages for these stocks in the year 2008 and plot the rolling 30 day average against the Close Price for Bank Of America's stock for the year 2008

# In[175]:
plt.figure(figsize=(12,4))
BAC['Close'].loc['2008-01-01':'2009-01-01'].rolling(window=30).mean().plot(label='30 Day Avg')
BAC['Close'].loc['2008-01-01':'2009-01-01'].plot(label='BAC Close')
plt.legend()


# Now let's create a heatmap of the correlation between the stocks Close Price.

# In[176]:
sns.heatmap(bank_stocks.xs('Close', 1, 1).corr(), annot=True, cmap='flare')


# In[177]:
sns.clustermap(bank_stocks.xs('Close', 1, 1).corr(), annot=True, cmap='flare')


# Let's create a candle plot of Bank of America's stock from Jan 1st 2015 to Jan 1st 2016.

# In[178]:
BAC.loc['2015-01-01':'2016-01-01'].iplot(kind='candle')


# And now a Simple Moving Averages plot of Morgan Stanley for the year 2015.

# In[179]:
MS.loc['2015-01-01':'2015-12-31']['Close'].ta_plot(study='sma', periods=[13,21,55], title='Simple Moving Averages')


# Finally, let's create a Bollinger Band Plot for Bank of America for the year 2015.

# In[180]:
BAC.loc['2015-01-01':'2015-12-31']['Close'].ta_plot(study='boll')
