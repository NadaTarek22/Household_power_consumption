#!/usr/bin/env python
# coding: utf-8

# In[51]:


# import libraries
import pandas as pd
import numpy as np
from datetime import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns


# ## **Load the data into the main dataframe and print out a few lines.**
# 

# In[52]:



df = pd.read_csv('02 Household Power Consumption.zip', sep=';', 
                 header=[0],
                 low_memory=False, na_values=['nan','?',''])


# In[53]:


#show the first 5 columns in the Dataframe
df.head()


# In[54]:


# Add date and time coulmn named Snapshot Date
# Add day name coulmn named Week Day as string type
#Add Month Name coulmn named Month Name


# In[55]:


df['Snapshot Date'] = df.Date.astype(str) + ' ' + df.Time.astype(str)
df['Snapshot Date'] = pd.to_datetime(df['Snapshot Date'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
df.drop(['Date', 'Time'], axis=1, inplace=True)

df['Week Day']=pd.to_datetime(df['Snapshot Date']).dt.day_name()

df['Month Name']=pd.to_datetime(df['Snapshot Date']).dt.month_name()

df['Week Day'].astype(str)


# In[56]:


# Rename Dataset Columns 
df.rename(columns={'Global_active_power':'Global_active_power','Sub_metering_1': 'Kitchen_Consumption','Sub_metering_2':'Laundry_Room_Consumption','Sub_metering_3':'Heater_Air_Condition_Consumption'}, inplace=True)


# In[57]:


#show the first 5 columns in the Dataframe
df.head()


# In[58]:


# Dataframe dimension
df.shape


# In[59]:


# print dataframe columns' types
df.dtypes


# In[60]:


#convert columns of the dataframe to float 
def function():
    for i in ['Global_active_power', 'Voltage',
       'Global_intensity']:
            df[i]=pd.to_numeric(df[i],errors='coerce')
    df['Other Power'] =  df['Global_active_power'] * 1000/60 - df['Laundry_Room_Consumption'] - df['Kitchen_Consumption'] - df['Heater_Air_Condition_Consumption']
    
function()




# In[61]:


#check for the datatype of the dataframe 

df.dtypes


# In[62]:


#show ALl columns
df.columns


# In[63]:


#show ALl columns

df.head()


# In[64]:


# Check for the range of the values of the Snapshot Date column

minValue =df['Snapshot Date'].min()
print(minValue)
maxValue =df['Snapshot Date'].max()
print(maxValue)


# In[65]:


# Check for the null values of the Global_active_power column
res = pd.isnull(df['Global_active_power'])
res.shape


# ## **Check How Many Rows have Null Values for Each Column/Row

# In[66]:


# Function for finding all columns that have nan:

def getNanColumns ():
    droping_list_all=[]
    for j in range(0,7):
        if not df.iloc[:, j].notnull().all():
            droping_list_all.append(j) 
        
    return (droping_list_all)


# In[67]:


# call function and using the set
vNullColumns = getNanColumns()
print(vNullColumns)

vNullColumnsSet=set(vNullColumns)
print("vNullColumnsSet ", vNullColumnsSet)


# In[68]:


# Removing rows contain null values for all its cells
#df= df.dropna(axis=0, how='all')


# In[69]:


#Checking for Nan values num in each column
df.isnull().sum()


# # **Remove Null Values within our dataframe

# In[70]:


#filling nan value with mean 

def FillnaValue():
    for j in range(0,7):    
        df.iloc[:,j]=df.iloc[:,j].fillna(df.iloc[:,j].mean())
    x = df["Other Power"].mean()
    df["Other Power"].fillna(x, inplace = True)
    df["Week Day"].fillna('Friday', inplace = True)
    df["Month Name"].fillna('January', inplace = True)
    df["Snapshot Date"].fillna(df['Snapshot Date'].min(), inplace = True)  

FillnaValue()


# In[71]:


#check null
df.isnull().sum()


# In[72]:


# Check duplicates
df.duplicated('Snapshot Date').sum


# In[73]:


##**Conclusion:
#    We don't have duplicate snapshots based on the date time 
   


# In[74]:


# The nunique() method returns the number of unique values for each column.

print(df.nunique());


# In[75]:


# show some statistic measures on the dataframe values
df.describe()


# # Visulalization and Conclusions

# In[76]:


# Plot box plot to show the values distribution
fig, axes = plt.subplots(3, 2,figsize=(10,10))
sns.boxplot(ax=axes[0, 0], data=df, y='Global_active_power')
sns.boxplot(ax=axes[0, 1], data=df, y='Kitchen_Consumption')
sns.boxplot(ax=axes[1, 0], data=df, y='Laundry_Room_Consumption')
sns.boxplot(ax=axes[1, 1], data=df, y='Heater_Air_Condition_Consumption')
sns.boxplot(ax=axes[2, 0], data=df, y='Voltage')
sns.boxplot(ax=axes[2, 1], data=df, y='Global_reactive_power')
#sns.boxplot(y=df['Global_active_power'])


# In[77]:


# It can be concluded from the figue that there are outliers that should be taken under consideration


# In[78]:


#plot histgram for df columns to show the values distribution
fig, axes = plt.subplots(3, 2,figsize=(15,15))
sns.histplot(ax=axes[0, 0], data=df, x='Global_active_power', bins=15, kde=True)
sns.histplot(ax=axes[0, 1], data=df, x='Kitchen_Consumption', bins=15, kde=True)
sns.histplot(ax=axes[1, 0], data=df, x='Laundry_Room_Consumption', bins=15, kde=True)
sns.histplot(ax=axes[1, 1], data=df, x='Heater_Air_Condition_Consumption', bins=15, kde=True)
sns.histplot(ax=axes[2, 0], data=df, x='Voltage', bins=15, kde=True)
sns.histplot(ax=axes[2, 1], data=df, x='Global_reactive_power', bins=15, kde=True)

plt.show()


# In[79]:


df.hist(figsize = (12,14))


# ## **Compare the Consumption of Every Meter per Week Day

# In[80]:



d_weekday_power_df = df.groupby(['Week Day'], as_index=0).agg({  'Kitchen_Consumption':'mean','Laundry_Room_Consumption':'mean' ,'Heater_Air_Condition_Consumption':'mean','Other Power':'mean'})

d_weekday_power_df.set_index('Week Day').plot.bar(rot='vertical', title='Power Consumption per Week Day', figsize=(12,6), fontsize=12)


# ### **Conclusion
# The mean power consumption during the weekend days (Saturday and Sunday) are the highest, which means that people mostly stay at home and use the electrical devices
# 
# The Other power metering is the highest one over all days, unfortunately we are not able to tell the reasone because we don't have details about the electrical devices being used.
# 
# The laundry room is often used on Sunday.
# 

# ## **Compare the Consumption of Every Meter per Month

# In[81]:


d_month_power_df = df.groupby(['Month Name'], as_index=0).agg({ 'Kitchen_Consumption':'mean','Laundry_Room_Consumption':'mean' ,'Heater_Air_Condition_Consumption':'mean','Other Power':'mean'})

print('\n', d_weekday_power_df)

d_month_power_df.set_index('Month Name').plot.bar(rot='vertical', title='Power Consumption per Month', figsize=(12,6), fontsize=12)


# ### **Conclusion
# The higest power consumption are during the winter months (December, January and February nad March).
# 
# During the winter months (December, January and February nad March), the use of heater, air condition is increased by around 35-40% compared with April
# 
# The Other power metering is the highest one over all months specially in winter, unfortunately we are not able to tell the reasone because we don't have details about the electrical devices being used.
# 

# In[82]:


# Copy the dataframe and Reset the index value of it to answer our questions
dfn= df
dfn.reset_index(drop=True)
dfn.set_index('Snapshot Date',inplace=True)
print(dfn)


# In[83]:


#'Global_Consumption per month averaged over month
dfn['Global_active_power'].resample('M').mean().plot(figsize=(15,5),kind='bar')
plt.xticks(rotation=90)
plt.ylabel('Global_active_power')
plt.title('Global_Consumption per month (averaged over month)')
plt.show()


# **Conclusion
# 
# The mean power consumption during December was the highest which means that people mostly stay at home and use the electrical devices
# heavely so they need to take care of their usage 
# 

# In[85]:


#'Global_Consumption per month (averaged over month
dfn['Global_active_power'].resample('Q').mean().plot(figsize=(15,5),kind='bar')
plt.xticks(rotation=90)
plt.ylabel('Global_active_power')
plt.title('Global_Consumption Global_active_power per quarter (averaged over quarter)')
plt.show()


# **Conclusion
# Note: Assuming that the data is correct and complete for the whole year, the following can be observed:
# 
# The mean power consumption during the seconed quarter of year 2007 was the best and people in the house should take care of their usage of electrinic devices during the first quarter of the year because it was the highest which means that people mostly stay at home and use the electrical devices
# heavely so they need to take care of their usage 

# In[87]:


## resampling over week and computing mean
dfn.Global_active_power.resample('W').mean().plot(figsize=(20,10),color='y', legend=True)
dfn.Global_intensity.resample('W').mean().plot(figsize=(20,10),color='r', legend=True)
#dfn.Kitchen_Consumption.resample('W').mean().plot(figsize=(20,10),color='b', legend=True)
#dfn.Laundry_Room_Consumption.resample('W').mean().plot(figsize=(20,10),color='pink', legend=True)
#dfn.Heater_Air_Condition_Consumption.resample('W').mean().plot(figsize=(20,10),color='brown', legend=True)
#dfn.Voltage.resample('W').mean().plot(figsize=(20,10),color='g', legend=True)
plt.suptitle("metrics resampled over Week")
plt.show()


# **Conclusion
# 
# There is a direct relationship between the weekly consumption of energy and the global intensity. 
# It can be noted that it was the lowest during March and the highest during February, so we advise people at home to review their consumption during February

# In[89]:


## resampling over week and computing mean
dfn.Global_active_power.resample('W').mean().plot(figsize=(20,10),color='y', legend=True)
#dfn.Global_intensity.resample('W').mean().plot(figsize=(20,10),color='r', legend=True)
#dfn.Kitchen_Consumption.resample('W').mean().plot(figsize=(20,10),color='b', legend=True)
#dfn.Laundry_Room_Consumption.resample('W').mean().plot(figsize=(20,10),color='pink', legend=True)
#dfn.Heater_Air_Condition_Consumption.resample('W').mean().plot(figsize=(20,10),color='brown', legend=True)
dfn.Voltage.resample('W').mean().plot(figsize=(20,10),color='g', legend=True)
plt.suptitle("metrics resampled over Week")
plt.show()


# **Conclusion
# 
# There is a direct relationship between the weekly consumption of energy and the global voltage. 
# 

# In[91]:


## resampling over week and computing mean
dfn.Global_active_power.resample('W').mean().plot(figsize=(20,10),color='y', legend=True)
#dfn.Global_intensity.resample('W').mean().plot(figsize=(20,10),color='r', legend=True)
dfn.Kitchen_Consumption.resample('W').mean().plot(figsize=(20,10),color='b', legend=True)
dfn.Laundry_Room_Consumption.resample('W').mean().plot(figsize=(20,10),color='pink', legend=True)
dfn.Heater_Air_Condition_Consumption.resample('W').mean().plot(figsize=(20,10),color='brown', legend=True)
#dfn.Voltage.resample('W').mean().plot(figsize=(20,10),color='g', legend=True)
plt.suptitle("metrics resampled over Week")
plt.show()


# **Conclusion:
# 
# There is a direct relationship between the weekly consumption of energy and the global intensity, voltage and other measures. 
# It can be noted that it was the the use of heater and air condition was the highest during February thus power consumption was also the highest in this month.
# heater and air condition companies can take a benifet of this note and make more offers during February. 
# It can be noted that it was the the use of laundery was the highest during Mars weeks thus power consumption was also in this month.
# heater and air condition companies can take a benifet of this note and make more offers during February. 
# Laundry soap and washing machine companies can take a a benifet of this note too.
# In overall taking a benefit of noticeing that people stay more at home during march and february.
