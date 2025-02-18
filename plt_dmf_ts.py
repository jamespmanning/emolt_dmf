#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 08:13:11 2024

@author: JiM
routine to plot MassDMF time series as extracted from either:
    -MassGIS site download
    -ready-for-oracle .dat files
    -ERDDAP
Jan 2025 added linear trend rate (taken from plt_emolt_annual.py)
"""


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import timedelta as td
from conversions import fth2m

#MASS DMF csv file
df=pd.read_csv('MA_Ocean_Bottom_Temperature_Sensor_Data.csv',index_col='DATE')
#df.dropna(inplace=True)
df.index=pd.to_datetime(df.index,format='%m/%d/%Y %I:%M:%S %p')#-td(6*365/12)
#df['DateT']=pd.to_datetime(df['DATE'],format='%m/%d/%Y %I:%M:%S %p')-td(6*365/12)# where we need to center the year
#df=df.set_index('DateT')

sites=df.columns.values
wsite=[7,6,5,4,3,2,1,10,8,9,11]#emolt codes for "sites" listed

for k in range(1,len(sites)):
#for k in [7]:    
    # make time series plot
    print(sites[k])
    fig=plt.figure(figsize=(10,8))
    ax=fig.add_subplot(111)
    ax.plot(df[sites[k]],label='MASS_GIS-served daily averages')
    
    if (wsite[k-1]!=3) and (wsite[k-1]!=8):
        # add oracle-ready files
        if wsite[k-1]<10:
            dfo=pd.read_csv('oracle_ready/mabihourly_pre_oracle_DMF'+str(wsite[k-1])+'_2025.csv',header=None,index_col=3)
        else:
            dfo=pd.read_csv('oracle_ready/mabihourly_pre_oracle_MA'+str(wsite[k-1])+'_2025.csv',header=None,index_col=3)
        dfo.index=pd.to_datetime(dfo.index,format='%d-%b-%Y:%H:%M')
        dfo['degc']=(dfo[5]-32)/1.8
        ax.plot(dfo['degc'],label='raw_pre_oracle bi-hourly')
    
    # make annual mean & plot with trend
    #df['Year_mean'] = df.groupby(df.index.year)[site].transform('mean')# value for each day (ie step function)
    dfa=df[sites[k]].resample('YE-JUN').agg(['mean', 'count'])
    # determine invalid months
    invalid = dfa['count'] <= 0.9*365 # only accepting years with at least 90% coverage
    dfa = dfa['mean']
    dfa[invalid] = np.nan
    dfa.dropna(inplace=True)
    #dfa=dfa[3:-2]
    ax.plot(dfa.index,dfa,linewidth=4,color='r',label='annual mean')# step function
    t = np.arange(0, len(dfa))
    z = np.polyfit(t, dfa.values.flatten(), 1)
    p = np.poly1d(z)
    fitpts=p(t)
    y=[fitpts[0],fitpts[-1]]
    ax.plot([dfa.index[0],dfa.index[-1]],y,'--',color='r',linewidth=6,label='warming of '+chr(0x2191)+'%0.2f' % z[0]+' degC/year')
    
    
    # add another axis for Fahrenheit & label
    ax.set_ylabel('degC',fontsize=18)
    ax4=ax.twinx()
    ax4.set_ylabel('degF',fontsize=18)
    mint=np.nanmin(df[sites[k]].values)
    maxt=np.nanmax(df[sites[k]].values)
    #ax4.set_ylim((mint-32)/1.8,(maxt-32)/1.8)
    ax4.set_ylim(mint*1.8+32,maxt*1.8+32)
    ax.set_ylim(mint,maxt)
    
    ax.legend()
    try:
        plt.title('Mass DMF data from shipwreck '+sites[k]+' feet ('+'%0.1f' % fth2m(float(sites[k][-3:])/6)+' meters)')
    except:
        plt.title('Mass DMF data from shipwreck '+sites[k])
    if wsite[k-1]<10:
        plt.savefig('plots_gis_site_data/DMF'+str(wsite[k-1])+'_jt.png')
    else:
        plt.savefig('plots_gis_site_data/MA'+str(wsite[k-1])+'_jt.png')
    





