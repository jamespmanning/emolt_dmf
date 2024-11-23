#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 05:24:06 2024
spot checking DMF data
@author: user
"""
site="DMF7"
import pandas as pd
import numpy as np
import conversions
from matplotlib import pyplot as plt
import warnings
warnings.filterwarnings("ignore")

def getsite_latlon(site):
    df=pd.read_csv('/home/user/emolt_non_realtime/emolt/emolt_site.csv')
    df1=df[df['SITE']==site]
    return df1['LAT_DDMM'].values[0],df1['LON_DDMM'].values[0]

def getobs_tempdepth_latlon(lat,lon):
    """
    Function written by Jim Manning to get emolt data from url, return datetime, depth, and temperature.
    this version needed in early 2023 when "site" was no longer served via ERDDAP
    """
    url = 'https://comet.nefsc.noaa.gov/erddap/tabledap/eMOLT.csvp?time,depth,sea_water_temperature&latitude='+str(lat)+'&longitude='+str(lon)+'+&orderBy(%22time%22)'
    df=pd.read_csv(url,skiprows=[1])
    df['time']=df['time (UTC)']
    temp=1.8 * df['sea_water_temperature (degree_C)'].values + 32 #converts to degF
    depth=df['depth (m)'].values
    #time=[];
    #for k in range(len(df)):
    #        time.append(parse(df.time[k]))
    #print('using erddap') 
    time=df['time'].values      
    dfnew=pd.DataFrame({'temp':temp,'depth (m)':depth,'latitude (degrees_north)':lat,'longitude (degrees_east)':lon},index=time)
    return dfnew

for k in [1,2,3,4,5,6,7,8,9,10,11]:
    if k<10:
        site='DMF'+str(k)
    else:
        site='MA'+str(k)
    [lat,lon]=getsite_latlon(site)
    df=getobs_tempdepth_latlon(lat,lon)
    df.dropna(subset=["temp"], inplace=True)
    print(site+' Last_time: '+max(df.index))
    print(site+' Lat/Lon: '+str(df['latitude (degrees_north)'][0])+'N '+str(df['longitude (degrees_east)'][0])+'W')
    print(site+' mean_depth: '+'%0.1f' %np.mean(df['depth (m)'])+' meters')
    print(site+' min_depth: '+'%0.1f' %np.min(df['depth (m)'])+' meters')
    print(site+' max_depth: '+'%0.1f' %np.max(df['depth (m)'])+' meters\n')
    fig = plt.figure()
    df['depth (m)'].plot()
    plt.title(site+'_depths in meters')
    fig.autofmt_xdate()
    fig.savefig(site+'_depths.png')
