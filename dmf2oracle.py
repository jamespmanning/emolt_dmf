# routine to process dmf shipwreck temps
# since the data comes in different formats every year, the code needs to deal with various input options
# sometimes DMF sends us the data with multiple columns and sometimes it comes in multiple sheets
# Most recently, in 2025, it is the later with each site is stored in a separate sheet
import numpy as np
from datetime import datetime,timedelta
from pandas import read_csv,DataFrame,read_excel
yr=2025 # year of processing
#sites=['Cleveland Ledge','Buzzards Bay Barge','Rocky Point','Manomet Boulders','Wreck of the Mars','Martins Ledge','Sippiwisset Rock','Scortons Ledge','Cuttyhunk']

#BUZ	    BUZ	        CCB	 CCB	    CCB	    CCB	    BOS	         BUZ	    BOS	     CCB	      BUZ
#CLEV   TOWR/Barge  	RCKY	 MNMT	ENDC 	MARS 	RMNC/Martins	 Sipp	Sculpin	 Scortons CUTTY
# 7     6           5    4      3        2       1            10     8         9       11
#directory='/net/data5/jmanning/newt/mass_dmf/2015/' #originally stored data here
directory='' # puts input and output file in same directory as code
# site code associated with "sites" above (note: 3 ENDC in 13.5Fa & 8 Sculpin in 3Fa not here anymore)
#depths=[4.2,13.7,6.4,9.3,18.5,14.5,3,2,999] # water depth in fathoms based on 2020 from Derek
 # water depth in fathoms based on 2023 data from Alex

if yr==2024:
    inputfile='DMF Temp Update ERRDAP 2023_scorton_fixed.xlsx' # file sent by ALex B in jan 2023
    colnames=['SITE','Date','Time','Latitude','Longitude','Depth','Sea_Water_Temperature']
    sites=['Cleveland','Barge','Rocky Point','Manomet','Mars','Martins','Sippiwissett','Scortons','Cuttyhunk']
    wsite=[7,6,5,4,2,1,10,9,11]
    depths=[4.2,11.6,7.5,9.2,18.3,11.6,3.0,5.0,3.0] # depths from Alex
elif yr==2025:
    inputfile='2025NOAATempUpdateforJM_JD.xlsx' # file sent by Jake/Jacob Doherty
    colnames=['SITE','Date','Hour','Latitude','Longitude','Depth','Sea_Water_Temperature']
    sites=['Cleveland','Barge','Rocky Point','Manomet','Mars','Martins','Scortons','Sippiwissett','Cuttyhunk']
    wsite=[7,6,5,4,2,1,9,10,11]# note 9 & 10 are switched relative to 2024 processing
    depths=[4.2,11.6,7.5,9.2,18.3,11.6,5.0,3.0,3.0]
def parse(datet1,datet2):
    ''' parses a few date columms that we have combined inside read_csv'''
    dt = datetime.strptime(datet1[0:8],'%Y-%m-%d')
    print(datet1,datet2)
    dt=datet1
    #delta = timedelta(hours=int(datet2[20:22]))
    delta=datet2
    return dt + delta
depth_i=depths # instrument depth
#tso=read_csv(directory+'tempsall.csv',parse_dates={'datet':['DATE','HR']},index_col='datet',date_parser=parse,skiprows=0,header=1)
#numsites=tso.shape[1]
numsites=9
#orig_name=tso.columns.values
for k in range(numsites): # if you want specific one like "ROCKY" specify "k in [2]:", for example
    print(sites[k])
    # create a dataframe for this site
    #tsdf=DataFrame(tso[orig_name[k]],index=tso.index)
    #tsdf=read_excel(directory+inputfile,parse_dates={'datet':['Date','Hour']},index_col='datet',date_parser=parse,converters={'Date':str,'Hour':str},sheet_name=sites[k])
    #tsdf=read_excel(directory+inputfile,parse_dates={'datet':['Date','Hour']},index_col='datet',date_parser=parse,converters={'Date':str,'Hour':str},sheet_name=sites[k])
    tsdf=read_excel(directory+inputfile,sheet_name=sites[k],header=None,skiprows=1,names=colnames)
    # noticed in Fen 2025 that this automatically interprets date and time as datetime objects
    tsdf.dropna(inplace=True)
    if yr==2025:
        tsdf.rename(columns={'Hour':'Time'},inplace=True) # to be consistent with previous years
    #try:
    tsdf['hour']=tsdf['Time']#.dt.hour # most often the case where time is formatted as datetime
    '''
    except:
        # 2024 processing special case needed as in the case of Scorton Ledge (float) and Martins Ledge where I formatted to "time"           
        hr=[]
        for kk in range(len(tsdf)):
            if type(tsdf['Time'][kk])==np.float64: # Scorton Ledge
                hr.append(tsdf['Time'][kk])
            else: # Martins ledge case where it is formatted as "time" 
                hr.append(tsdf['Time'][kk].hour)
        tsdf['hour']=hr    
    '''
    datet=[]
    
    for j in range(len(tsdf)): # here's where we combine date and hour to make a datetime
        '''
        if (tsdf['Date'][j]>datetime(2019,9,29,0,0,0)) and (k==7) and (yr!=2025): # special 2024 case for Scortons ledge
            datet.append(tsdf['Date'][j])
        else:
            '''
        try:
            datet.append(tsdf['Date'][j]+timedelta(hours=tsdf['hour'][j].hour))
        except:
            datet.append(np.nan)# this was needed in the case of Cuttyhunk having missing data 
            print(sites[k]+' has trouble at ',tsdf.Date[j-1])

    tsdf['datet']=datet
    tsdf.dropna(inplace=True)
    tsdf=tsdf.set_index('datet')
    # at some point in the future we may want to call "getemolt_temp" to determine the last date of the oracle for this site and then delimit the dataframe for that period only
    formatted_date,temp=[],[]
    for i in range(len(tsdf)):
      formatted_date.append(tsdf.index[i].strftime('%d-%b-%Y:%H:%M')) #get date in the format wanted by our Oracle loading routine
      try:
          temp.append(float(1.8*tsdf['Sea_Water_Temperature'].values[i]+32.)) # converts to degF
      except:
          print(sites[k]+' has trouble at ',tsdf.index[i].strftime('%d-%b-%Y:%H:%M'))
          temp.append(np.nan)
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
       tsdfp.to_csv('oracle_ready/mabihourly_pre_oracle_DMF'+str(wsite[k])+'_'+str(yr)+'.csv',index=False,header=False,float_format='%10.4f')
    else:
       tsdfp.to_csv('oracle_ready/mabihourly_pre_oracle_MA'+str(wsite[k])+'_'+str(yr)+'.csv',index=False,header=False,float_format='%10.4f')
      
