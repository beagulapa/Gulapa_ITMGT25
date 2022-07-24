#cleaning data
#import needed libraries/tools
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import string

#load data and turn into dataframe
with open("transaction-data-adhoc-analysis.json","r") as f:
    data = json.load(f)
    
dataframe = pd.DataFrame(data)

#get transaction month
date = dataframe[['transaction_date']].squeeze()
date = pd.to_datetime(date)
month = date.dt.month_name()

dataframe['Month of Transaction'] = month

#split items in each order using split and explode to create new dataset to use
dataframe['item_list'] = dataframe['transaction_items'].str.split(';')
items = dataframe.explode("item_list")

#turn number of items sold into its own column
def itemamount(item):
    number = int(item[(item.index('('))+2:][:-1])
    return number

items['number_items'] = items['item_list'].apply(itemamount)

#isolate character names
def itemname(item):
    name = item[:(item.index('('))-1]
    return name
    
items['Item Sold'] = items['item_list'].apply(itemname)

#creating tables - table 1: breakdown of the count of each item sold per month
#create pivot table for tb1
tb1table = pd.pivot_table(items, index='Item Sold', columns='Month of Transaction', values='number_items',aggfunc=sum)

#Put months in correct order 
from calendar import month_name
month_dtype = pd.CategoricalDtype(categories=list(month_name),ordered=True)
tb1table.columns = tb1table.columns.get_level_values(0).astype(month_dtype)
tb1table = tb1table.sort_index(axis=1, level=[1,0])

#creating tables - table 2: breakdown of the total sale value per item per month
#Getting price per item
gummyworms = items.loc[:,'Item Sold']=='Candy City,Gummy Worms'
orangebeans = items.loc[:,'Item Sold']=='Candy City,Orange Beans'
beefchicharon = items.loc[:,'Item Sold']=='Exotic Extras,Beef Chicharon'
kimchiseaweed = items.loc[:,'Item Sold']=='Exotic Extras,Kimchi and Seaweed'
gummyvitamins = items.loc[:,'Item Sold']=='HealthyKid 3+,Gummy Vitamins'
nutrionalmilk = items.loc[:,'Item Sold']=='HealthyKid 3+,Nutrional Milk'
yummyvegetables = items.loc[:,'Item Sold']=='HealthyKid 3+,Yummy Vegetables'

Prices = {'Candy City,Gummy Worms':list(items.loc[gummyworms,:].min(numeric_only=True))[0],
          'Candy City,Orange Beans':list(items.loc[orangebeans,:].min(numeric_only=True))[0],
          'Exotic Extras,Beef Chicharon':list(items.loc[beefchicharon,:].min(numeric_only=True))[0],
          'Exotic Extras,Kimchi and Seaweed':list(items.loc[kimchiseaweed,:].min(numeric_only=True))[0],
          'HealthyKid 3+,Gummy Vitamins':list(items.loc[gummyvitamins,:].min(numeric_only=True))[0],
          'HealthyKid 3+,Nutrional Milk':list(items.loc[nutrionalmilk,:].min(numeric_only=True))[0],
          'HealthyKid 3+,Yummy Vegetables':list(items.loc[yummyvegetables,:].min(numeric_only=True))[0]
         }

#Create a column with the price of the product 
def priceofproduct(product): 
    price = Prices[product]
    return price

items['Product Price'] = items['Item Sold'].apply(priceofproduct) 

#Multiply previously created column with the number_items 
items["Value Per Item"] = items["number_items"] * items["Product Price"]

#create pivot table for tb2
tb2table = pd.pivot_table(items, index='Item Sold', columns='Month of Transaction', values='Value Per Item',aggfunc=sum)

#Put months in correct order 
from calendar import month_name
month_dtype = pd.CategoricalDtype(categories=list(month_name),ordered=True)
tb2table.columns = tb1table.columns.get_level_values(0).astype(month_dtype)
tb2table = tb2table.sort_index(axis=1, level=[1,0])

#creating tables - table 3: repeaters, inactives, engaged customers
#create pivot table for months for customer activity
monthtable = dataframe.pivot_table('mail', index='name', columns='Month of Transaction',aggfunc='count', fill_value = 0)

#Put months in correct order 
from calendar import month_name
month_dtype = pd.CategoricalDtype(categories=list(month_name),ordered=True)
monthtable.columns = monthtable.columns.get_level_values(0).astype(month_dtype)
monthtable = monthtable.sort_index(axis=1, level=[1,0])

#get unique values for months
all_months = list(dataframe["Month of Transaction"].unique())

#create functions to find the number of repeater, inactive, and engaged customers respectively
#repeater
def repeaters(month):
    monthbefore = all_months[all_months.index(month)-1]
    if all_months.index(month)-1 < 0:
        return 0
    else:
        ans = monthtable[month][(monthtable[month] > 0) & (monthtable[monthbefore] > 0)].count()
        return ans

#inactive
def inactives(month):
    firstmonth = all_months[0]
    monthbefore = all_months[all_months.index(month)-1]
    if all_months.index(month)-1 < 0:
        return 0
    else:
        if month == 'January':
            ans = monthtable[month][(monthtable[month] == 0) & (monthtable.iloc[:,[0]].sum(axis=1) > 0)].count()
            return ans
        if month == 'February':
            ans = monthtable[month][(monthtable[month] == 0) & (monthtable.iloc[:,[0]].sum(axis=1) > 0)].count()
            return ans
        if month == 'March':
            ans = monthtable[month][(monthtable[month] == 0) & (monthtable.iloc[:,[0,1]].sum(axis=1) > 0)].count()
            return ans
        if month == 'April':
            ans = monthtable[month][(monthtable[month] == 0) & (monthtable.iloc[:,[0,1,2]].sum(axis=1) > 0)].count()
            return ans
        if month == 'May':
            ans = monthtable[month][(monthtable[month] == 0) & (monthtable.iloc[:,[0,1,2,3]].sum(axis=1) > 0)].count()
            return ans
        if month == 'June':
            ans = monthtable[month][(monthtable[month] == 0) & (monthtable.iloc[:,[0,1,2,3,4]].sum(axis=1) > 0)].count()
            return ans

#engaged
def engaged(month):
    firstmonth = all_months[0]
    monthbefore = all_months[all_months.index(month)-1]
    if month == 'January':
        ans = monthtable[month][(monthtable[month] > 0)].count()
        return ans
    if month == 'February':
        ans = monthtable[month][(monthtable[month] > 0) & (monthtable[all_months[all_months.index(month)-1]] > 0)].count()
        return ans
    if month == 'March':
        ans = monthtable[month][(monthtable[month] > 0) & (monthtable[all_months[all_months.index(month)-1]] > 0) 
                                & (monthtable[all_months[all_months.index(month)-2]] > 0)].count()
        return ans
    if month == 'April':
        ans = monthtable[month][(monthtable[month] > 0) & (monthtable[all_months[all_months.index(month)-1]] > 0) 
                                & (monthtable[all_months[all_months.index(month)-2]] > 0) & (monthtable[all_months[all_months.index(month)-3]] > 0)].count()
        return ans
    if month == 'May':
        ans = monthtable[month][(monthtable[month] > 0) & (monthtable[all_months[all_months.index(month)-1]] > 0) 
                                & (monthtable[all_months[all_months.index(month)-2]] > 0) & (monthtable[all_months[all_months.index(month)-3]] > 0)
                               & (monthtable[all_months[all_months.index(month)-4]] > 0)].count()
        return ans
    if month == 'June':
        ans = monthtable[month][(monthtable[month] > 0) & (monthtable[all_months[all_months.index(month)-1]] > 0) 
                                & (monthtable[all_months[all_months.index(month)-2]] > 0) & (monthtable[all_months[all_months.index(month)-3]] > 0)
                               & (monthtable[all_months[all_months.index(month)-4]] > 0) & (monthtable[all_months[all_months.index(month)-5]] > 0)].count()
        return ans

#create dataframe 
tb3table = pd.DataFrame()
tb3table['Customer_Type']=['Repeater','Inactive','Engaged']
for i in all_months:
    tb3table[i]=[repeaters(i),inactives(i),engaged(i)]
    
#create graphs for each table
#tb1table 
tb1bar = tb1table.plot(kind='bar')
plt.ylabel('Count of Each Item Sold')
plt.title('Count of Each Item Sold Per Month')
plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

#tb2table
tb2bar = tb2table.plot(kind='bar')
plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
plt.ylabel('Sale Value Per Item')
plt.title('Sale Value Per Item Per Month')

#tb3table
tb3bar = tb3table.plot4(kind='bar')
plt.xlabel('Customer Type')
plt.ylabel('Number of Customer Type')
tb3bar.set_xticklabels(tb3table.Customer_Type)
plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
plt.title('Count of Customer Types Per Month')