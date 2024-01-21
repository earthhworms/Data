# # 911 Calls Capstone Project

# For this capstone project we will be analyzing some 911 call data from [Kaggle](https://www.kaggle.com/mchirico/montcoalert). The data contains the following fields:
# 
# * lat : String variable, Latitude
# * lng: String variable, Longitude
# * desc: String variable, Description of the Emergency Call
# * zip: String variable, Zipcode
# * title: String variable, Title
# * timeStamp: String variable, YYYY-MM-DD HH:MM:SS
# * twp: String variable, Township
# * addr: String variable, Address
# * e: String variable, Dummy variable (always 1)

# TO SEE A MORE DETAILED VIEW, INCLUDING GRAPHS SEE 
' https://salgadomichael.com/911-project '

# ## Data and Setup
# Importing numpy and pandas

# In[2]:
import numpy as np
import pandas as pd


# ** Importing visualization libraries **

# In[19]:
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# Reading in the csv file as a dataframe called df 

# In[5]:
df = pd.read_csv('911.csv')


# Checking the information of the df 

# In[94]:
df.info()


# Checking the head of df 

# In[6]:
df.head()


# ## Basic Analysis

# What are the top 5 zipcodes for 911 calls? 

# In[7]:
df.groupby(df['zip'])['zip'].count().sort_values(ascending = False).head()


# What are the top 5 townships (twp) for 911 calls?

# In[9]:
df.groupby(df['twp'])['twp'].count().sort_values(ascending=False).head()


# How many unique title codes are there? 

# In[10]:
df['title'].nunique()


# ## Creating new features

# In the titles column there are "Reasons/Departments" specified before the title code. These are EMS, Fire, and Traffic. Using a lambda expression, we will make a new column for the reasons.

# In[15]:
df['reasons'] = df['title'].apply(lambda x: x.split(':')[0])


# What is the most common Reason for a 911 call based off of this new column? 

# In[18]:
df.groupby(df['reasons'])['reasons'].count().sort_values(ascending=False)


# Creating a countplot of 911 calls by Reason. 

# In[20]:
sns.countplot(data=df, x='reasons')

# What is the data type of the objects in the timeStamp column? 

# In[140]:
type(df['timeStamp'].iloc[0])


# ** Converting the column from string to DateTime objects **

# In[21]:
df['timeStamp'] = pd.to_datetime(df['timeStamp'])


# ** Grabbing specific attributes and creating specific columns for each date time object:**

# In[89]:
df['hour'] = df['timeStamp'].apply(lambda x: x.hour)
df['month'] = df['timeStamp'].apply(lambda x: x.month)
df['day_of_week'] = df['timeStamp'].apply(lambda x: x.dayofweek)

df.head()


# ** Notice how the Day of Week is an integer 0-6. Using a dictionary, we will turn these numbers into string names for days of the week: **

# In[90]:
dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}


# In[91]:
df['day_of_week'] = df['day_of_week'].map(dmap)
df['day_of_week'].head()


# ** Creating a countplot of the Day of Week column with the hue based off of the reason column. **

# In[92]:
sns.countplot(data = df, x='day_of_week', hue='reasons')


# **Now doing the same for Month:**

# In[93]:
sns.countplot(data = df, x = 'month', hue='reasons')


# ** You should have noticed it was missing some Months, let's see if we can maybe fill in this information by plotting the information in another way, possibly a simple line plot that fills in the missing months, in order to do this, we'll need to do some work with pandas... **

# ** Let's create a gropuby object called byMonth, where we group the DataFrame by the month column and use the count() method for aggregation. **

# In[47]:
byMonth = df.groupby(df['month']).count()
byMonth.head()


# ** Now let's create a simple plot off of the dataframe indicating the count of calls per month. **

# In[48]:
sns.lineplot(data=byMonth,x='month',y='reasons')


# ** Now let's see if we can use lmplot() to create a linear fit on the number of calls per month. **

# In[51]:
sns.lmplot(data=byMonth.reset_index(), x='month', y='reasons')


# **Creating a new column called 'Date' that contains the date from the timeStamp column. ** 

# In[98]:
df['date'] = df['timeStamp'].apply(lambda x: x.date())


# ** Now let's groupby this Date column with the count() aggregate and create a plot of counts of 911 calls.**

# In[100]:
df.groupby(df['date']).count()['twp'].plot()
plt.tight_layout()


# ** Now let's recreate this plot but create 3 separate plots with each plot representing a Reason for the 911 call**

# In[110]:
df[df['reasons'] == 'Traffic'].groupby(['date'])['date'].count().plot().set_title('Traffic')
plt.tight_layout()


# In[56]:
df[df['reasons'] == 'Fire'].groupby('date')['date'].count().plot().set_title('Fire')
plt.tight_layout()


# In[59]:
df[df['reasons'] == 'EMS'].groupby(['date'])['reasons'].count().plot().set_title('EMS')
plt.tight_layout()


# ** Now let's move on to creating  heatmaps with ur data. We'll first need to restructure the dataframe so that the columns become the Hours and the Index becomes the Day of the Week.**

# In[72]:
df_dow = df.groupby(['day_of_week', 'hour']).count()['reasons'].unstack(1)


# ** Now lets create a HeatMap using this new DataFrame. **

# In[102]:
plt.figure(figsize=(12,6))
sns.heatmap(df_dow, cmap='coolwarm')


# ** Lets create a clustermap using this DataFrame. **

# In[103]:
sns.clustermap(df_dow, cmap = 'coolwarm')


# ** Now we'll these same plots and operations, for a DataFrame that shows the Month as the column. **

# In[104]:
df5 = df.groupby(['day_of_week', 'month']).count()['reasons'].unstack(1)
df5.head()


# In[108]:
plt.figure(figsize=(12,5))
sns.heatmap(df5, cmap = 'viridis')


# In[107]:
sns.clustermap(df5, cmap='viridis')


