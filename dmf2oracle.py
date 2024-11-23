# routine to process dmf shipwreck temps
import numpy as np
from datetime import datetime,timedelta
from pandas import read_csv,DataFrame,read_excel
sites=['Cleveland Ledge','Buzzards Bay Barge','Rocky Point','Manomet Boulders','Wreck of the Mars','Martins Ledge','Sippiwisset Rock','Scortons Ledge','Cuttyhunk']
#BUZ	BUZ	    CCB	    CCB	    CCB	    CCB	    BOS	         BUZ	    BOS	     CCB	      BUZ
#CLEV   TOWR  	RCKY	MNMT	ENDC	MARS	RMNC/Martins	 Sipp	Sculpin	 Scortons CUTTY
# 7     6       5       4       3       2       1            10     8         9       11
#directory='/net/data5/jmanning/newt/mass_dmf/2015/'
directory='' # puts input and output file in same directory as code
wsite=[7,6,5,4,2,1,10,9,11]# site code associated with "sites" above (note: 3 ENDC in 13.5Fa & 8 Sculpin in 3Fa not here anymore)
#depths=[4.2,13.7,6.4,9.3,18.5,14.5,3,2,999] # water depth in fathoms based on 2020 from Derek
depths=[4.2,11.6,7.5,9.2,18.3,11.6,3.0,5.0,3.0] # water depth in fathoms based on 2023 data from Alex
depth_i=depths # instrument depth
inputfile='DMF Temp Update ERRDAP 2023_scorton_fixed.xlsx' # file sent by ALex B in jan 2023
def parse(datet1,datet2):
    ''' parses a few date columms that we have combined inside read_csv'''
    #dt = datetime.strptime(datet1[0:8],'%Y-%m-%d')
    print(datet1,datet2)
    dt=datet1
    #delta = timedelta(hours=int(datet2[20:22]))
    delta=datet2
    return dt + delta
#tso=read_csv(directory+'tempsall.csv',parse_dates={'datet':['DATE','HR']},index_col='datet',date_parser=parse,skiprows=0,header=1)
#numsites=tso.shape[1]
numsites=9
#orig_name=tso.columns.values
for k in [7]:#range(numsites): # if you want specific one like "ROCKY" specify "k in [2]:", for example
    print(sites[k])
    # create a dataframe for this site
    #tsdf=DataFrame(tso[orig_name[k]],index=tso.index)
    #tsdf=read_excel(directory+inputfile,parse_dates={'datet':['Date','Time']},index_col='datet',date_parser=parse,converters={'Date':str,'Time':str},sheet_name=sites[k])
    colnames=['SITE','Date','Time','Latitude','Longitude','Depth','Sea_Water_Temperature']# column as shown in the first tab
    tsdf=read_excel(directory+inputfile,sheet_name=sites[k],header=None,skiprows=1,names=colnames)
    try:
        tsdf['hour']=tsdf['Time'].dt.hour # most often the case where time is formatted as datetime
    except:
        # case where the "time" column is no all datetimes as in the case of Scorton Ledge (float) and Martins Ledge where I formatted to "time"           
        hr=[]
        for kk in range(len(tsdf)):
            if type(tsdf['Time'][kk])==np.float64: # Scorton Ledge
                hr.append(tsdf['Time'][kk])
            else: # Martins ledge case where it is formatted as "time" 
                hr.append(tsdf['Time'][kk].hour)
        tsdf['hour']=hr    
    datet=[]
    for j in range(len(tsdf)): 
        if (tsdf['Date'][j]>datetime(2019,9,29,0,0,0)) and (k==7): # special case for Scortons ledge
            datet.append(tsdf['Date'][j])
        else:
            datet.append(tsdf['Date'][j]+timedelta(hours=int(tsdf['hour'].values[j])))
    tsdf['datet']=datet
    tsdf=tsdf.set_index('datet')
    # at some point in the future we may want to call "getemolt_temp" to determine the last date of the oracle for this site and then delimit the dataframe for that period only
    formatted_date,temp=[],[]
    for i in range(len(tsdf)):
      formatted_date.append(tsdf.index[i].strftime('%d-%b-%Y:%H:%M')) #get date in the format wanted by our Oracle loading routine
      temp.append(float(1.8*tsdf['Sea_Water_Temperature'].values[i]+32.)) # converts to degF
    tsdf['fd']=formatted_date
    tsdf['yd']=tsdf.index.dayofyear+tsdf.index.hour/24.+tsdf.index.minute/60./24.-1.0 #creates a yrday0 field
    tsdf['temp']=temp
    tsdf['salt']=-99.999
    #tsdf['depth_i']=int(round(depth_i[k]))
    tsdf['depth_i']=depth_i[k]
    if wsite[k]<10:
        tsdf['site']='DMF'+str(wsite[k])
    else:
        tsdf['site']='MA'+str(wsite[k])
    tsdf['sn']=999
    tsdf['probe_setting']=0
    output_fmt=['site','sn','probe_setting','fd','yd','temp','salt','depth_i']
    tsdfp=tsdf.reindex(columns=output_fmt)
    if wsite[k]<10:
       tsdfp.to_csv(directory+'mabihourly_pre_oracle_DMF'+str(wsite[k])+'_2023.csv',index=False,header=False,float_format='%10.4f')
    else:
       tsdfp.to_csv(directory+'mabihourly_pre_oracle_MA'+str(wsite[k])+'_2023.csv',index=False,header=False,float_format='%10.4f')
      
