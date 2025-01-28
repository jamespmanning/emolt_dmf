#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 13:20:15 2025
Routine to get the last sample from each DMF site

@author: JiM
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import timedelta as td
from conversions import fth2m

df=pd.DataFrame()
columns=['site','d1','d2','datet','yd','degf','sal','dep']
dfs=pd.read_csv('../emolt_sites_extra.csv')
#for k in range(1,9):
for k in [1,2,4,5,6,7,9]:
    dmf_site=dfs[dfs['SITE']=='DMF'+str(k)]
    try:
        df1=pd.read_csv('oracle_ready/mabihourly_pre_oracle_DMF'+str(k)+'_2023.csv',header=None,names=columns)
    except:
        df1=pd.read_csv('oracle_ready/mabihourly_pre_oracle_DMF'+str(k)+'_2023_new.csv',header=None,names=columns)
    dd=max(pd.to_datetime(df1['datet'],format="%d-%b-%Y:%H:%M"))
    print(dmf_site['ORIGINAL_NAME'].values[0]+' DMF'+str(k)+' '+str(dd))
for k in [10,11]:
    dmf_site=dfs[dfs['SITE']=='MA'+str(k)]
    df1=pd.read_csv('oracle_ready/mabihourly_pre_oracle_MA'+str(k)+'_2023.csv',header=None,names=columns)
    dd=max(pd.to_datetime(df1['datet'],format="%d-%b-%Y:%H:%M"))
    print(dmf_site['ORIGINAL_NAME'].values[0]+' MA'+str(k)+' '+str(dd))    
    