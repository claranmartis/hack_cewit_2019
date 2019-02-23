#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 22:21:46 2019

@author: claran
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data_full = pd.read_csv('CheckedIn.csv')
data = pd.read_csv('LIRR.csv')
data = data[:10]
station_list = pd.read_csv('stops.csv')


#function to convert the station code from a string of numbers
#mixed with different characters to a list of station codes as integers
def station_no(a):
    lst = []
    for i in a:
        if((i == ',') | (i.isdigit())):
            lst.append(i)
            
    x = 0
    l = []
    
    for j in lst:
        if(j!=','):
            x = (x * 10) + int(j)
        else:
            l.append(x)
            x = 0
    return l


    
#counts the numbers of app users taking this service
user_count = data_full.groupby('agencyId').count()
A = pd.Series(user_count['installationId'])
A.to_csv('city_users_count.csv')
A_head = A.nlargest(10)
sns.barplot(A_head.index, A_head.values)
plt.xticks(rotation=-45)
plt.title('Users taking differnt services')
plt.show()

count = {}
stops_col = data['tripStopIds']

#stops_col = stops_col[1]
for row in stops_col:
    row = station_no(row)
    for stop in row:
        stop = station_list['stop_name'].loc[station_list['stop_id'] == stop]
        try:
            stp = str(stop.values[0])
            if stp in count:
                count[stp] = count[stp] + 1
            else:
                count[stp] = 1
        except:
            pass

#plt.bar(count.keys(), count.values())
#plt.show()

S = pd.Series(count)
S_head = S.nlargest(10)
sns.barplot(list(S_head.index), list(S_head.values))
plt.title('Train traffic at the Station')
plt.xticks(rotation=-45)
plt.show()

S.to_csv('station_traffic.csv')


route = {}
for row in stops_col:
    row = station_no(row)
    prev_stop = row[0]
    for stop in row:
        if(prev_stop == stop):
            continue
        if(prev_stop > stop):
            temp = stop
            stop = prev_stop
            prev_stop = temp
        x = station_list['stop_name'].loc[station_list['stop_id'] == prev_stop]
        y = station_list['stop_name'].loc[station_list['stop_id'] == stop]
        try:
            key = str(x.values[0]) + str(" - ") + str(y.values[0])
            
            if key in route:
                route[key] = route[key] + 1
            else:
                route[key] = 1
        except:
            pass
            #key = str(x.values) + str(y.values)
            #print(x.values,y.values)
        #key = generate_key(prev_stop, stop) #str(prev_stop) + str(stop)
        #print(key)
        

#print(route)

#plt.bar(route.keys(), route.values())
#plt.show()



s = pd.Series(route)
s_head = s.nlargest(10)
sns.barplot(list(s_head.index), list(s_head.values))
plt.title('Train traffic in different routes')
plt.xticks(rotation=-45)
plt.show()
s.to_csv('route_traffic_3.csv')










