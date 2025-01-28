#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 08:13:11 2024

@author: JiM
routine to plot eMOLT time series
"""
site='Mars 110'

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import timedelta as td
from conversions import fth2m

#MASS DMF csv file
df=pd.read_csv('MA_Ocean_Bottom_Temperature_Sensor_Data.csv',index_col='DATE')
df.index=pd.to_datetime(df.index,format='%m/%d/%Y %I:%M:%S %p')#-td(6*365/12)
#df['DateT']=pd.to_datetime(df['DATE'],format='%m/%d/%Y %I:%M:%S %p')-td(6*365/12)# where we need to center the year
#df=df.set_index('DateT')

# make time series plot
fig=plt.figure(figsize=(10,8))
ax=fig.add_subplot(111)
ax.plot(df[site],label='bi-hourly temperatures')

# make annual mean & plot
#df['Year_mean'] = df.groupby(df.index.year)[site].transform('mean')# value for each day (ie step function)
dfa=df[site].resample('YE-JUN').mean() # centered around June?
ax.plot(dfa.index[2:-2],dfa[2:-2],linewidth=4,label='annual mean')# step function


# add another axis for Fahrenheit & label
ax.set_ylabel('degC',fontsize=18)
ax4=ax.twinx()
ax4.set_ylabel('degF',fontsize=18)
mint=np.nanmin(df[site].values)
maxt=np.nanmax(df[site].values)
#ax4.set_ylim((mint-32)/1.8,(maxt-32)/1.8)
ax4.set_ylim(mint*1.8+32,maxt*1.8+32)
ax.set_ylim(mint,maxt)

ax.legend()
plt.title('example Mass DMF data from shipwreck '+site+' feet ('+'%0.1f' % fth2m(float(site[-3:])/6)+' meters)')
plt.savefig(site)





