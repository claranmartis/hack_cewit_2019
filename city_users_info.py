#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 22:21:46 2019

@author: claran
"""

import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('LIRR.csv')
station_list = pd.read_csv('stops.csv')

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

def generate_key(a,b):
    x = station_list['stop_name'].loc[station_list['stop_id'] == a]
    y = station_list['stop_name'].loc[station_list['stop_id'] == b]
    key = x.values + y.values
    return key
    
    

count = data.groupby('agencyId').count()
S = pd.Series(count['installationId'])
S.to_csv('city_users_count.csv')


count = {}
stops_col = data['tripStopIds']

#stops_col = stops_col[1]
for row in stops_col:
    row = station_no(row)
    for stop in row:
        if stop in count:
            count[stop] = count[stop] + 1
        else:
            count[stop] = 1

#plt.bar(count.keys(), count.values())
#plt.show()

S = pd.Series(count)
S.to_csv('station_traffic.csv')

route = {}
for row in stops_col:
    row = station_no(row)
    prev_stop = row[0]
    for stop in row:
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
s.to_csv('route_traffic_3.csv')











