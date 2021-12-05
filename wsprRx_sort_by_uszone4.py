# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 05:26:47 2021

@author: gregg
"""

from pyhamtools.locator import locator_to_latlong
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point #,LineString,Polygon
import paramiko
from pyproj import CRS
import numpy as np

mygs = 'FN20wb'
# band = '80m'
callsign = 'WB6YAZ'
antenna = 'EW FD'
dmin = 211109
dmax = 211119
tmin = 0
tmax = 2359

figtitle = 'US zone4 WSPR Spots: ' + callsign + '(' + mygs + ')' + ' Antenna: ' + antenna + ' Dates: ' + str(dmin) + ' - ' + str(dmax)

USzone4=['EM55','EM56','EM60','EM61','EM62','EM63','EM64','EM65','EM66','EM67','EM70','EM71','EM72','EM73','EM74','EM75','EM76','EM77','EM78','EL87','EL88','EL89','EM80','EM81','EM82','EM83','EM84','EM85','EM86','EM87','EM88','EL95','EL96','EL97','EL98','EL98','EM90','EM91','EM92','EM93','EM94','EM95','EM96','FM03','FM04','FM05','FM06','FM07','FM08','FM14','FM15','FM16','FM17','FM18']


# fname = 'C:\\users\\gregg\\Documents\\Python\\wspr_analysis\\ALL_WSPR.TXT'
fname = r'C:\users\gregg\Documents\Python\wspr_analysis\ALL_WSPR_ewfd_pavel_112021.TXT'
f=open(fname)

# mygpsloc= [locator_to_latlong(mygs)]
# mypts=[Point(gpspoint[1],gpspoint[0]) for gpspoint in mygpsloc]

# d = {'myloc':[ 1 ]}
# df = pd.DataFrame(data=d)

# # crs = {'init':'epsg:4326'}
# crs = {'init':'EPSG:4326'}
# # crs='EPSG:4326'
# # crs_4326 = CRS('EPSG:4326')
# # crs = CRS('EPSG:4326')

# df=gpd.GeoDataFrame(df, crs=crs, geometry=mypts)
# # df = gpd.GeoDataFrame(df, crs=crs, geometry=mypts)


txt=f.read()
dates=[]
time=[]
n0=[]
snr=[]
drift=[]
freq=[]
call=[]
gs=[]
pwr=[]
n1=[]
n2=[]
n3=[]
n4=[]
n5=[]
i=0
n=0

allLN=txt.splitlines(); # split by row
for ln in allLN: # for every line
     tmp=ln.split()
     str_list = list(filter(None, tmp))  #remove spaces
     if(len(tmp) == 17):
         dates.append(float(str_list[0]))
         time.append(float(str_list[1]))
         snr.append(float(str_list[2]))
         drift.append(str_list[3])
         freq.append(float(str_list[4]))
         call.append(str_list[5])
         gs.append(str_list[6])
         pwr.append(str_list[7])
         n1.append(str_list[8])
         n2.append(str_list[9])
         n3.append(str_list[10])
         n4.append(str_list[11])
         n5.append(str_list[12])
     # elif(len(str_list)) < 17:
         # print('skipped line# =',i+1)
     i=i+1
print('number of datapoints =',i)
f.close()
print('Number of skipped datapoints =',i-len(n3))
                                              

# gpsloc= [locator_to_latlong(n) for n in gs]
# pts=[Point(gpspoint[1],gpspoint[0]) for gpspoint in gpsloc]
# d={'dates': dates,'time':time,'snr':snr,'drift':drift,'freq':freq,'call':call,'gs':gs,'pwr':pwr,'gpsLoc':gpsloc,'pts':pts}
d1={'dates': dates,'time':time,'snr':snr,'drift':drift,'freq':freq,'call':call,'gs':gs,'pwr':pwr}
# wspr=pd.DataFrame(data=d)
wspr1=pd.DataFrame(data=d1)

query_str='%f <= dates <= %f and %f <= time <= %f' % (dmin,dmax,tmin,tmax)
# subsetwspr=wspr.query(query_str)
subsetwspr1=wspr1.query(query_str)

wspr_zone4=[]

# for i in range(len(wspr1.gs)-1):
#     for j in range(len(USzone4)-1):
#         if subsetwspr1.gs[i][:4] == USzone4[j]:
#             wspr_zone4.append([wspr1.dates[i],wspr1.time[i],wspr1.snr[i],wspr1.freq[i],wspr1.call[i],wspr1.gs[i],wspr1.pwr[i]])
            
for i in subsetwspr1.index:
    for j in range(len(USzone4)-1):
        if subsetwspr1.gs[i][:4] == USzone4[j]:
            wspr_zone4.append([wspr1.dates[i],wspr1.time[i],wspr1.snr[i],wspr1.freq[i],wspr1.call[i],wspr1.gs[i],wspr1.pwr[i]])
            
wspr_zone4_df=pd.DataFrame(data=wspr_zone4)

wspr_zone4_df.columns = ['dates','time','snr','freq','call','gs','pwr']

zone4_160m=[]
zone4_80m=[]
zone4_60m=[]
zone4_40m=[]
zone4_30m=[]
zone4_20m=[]
zone4_15m=[]
zone4_10m=[]

for i in range(len(wspr_zone4_df.gs)):
    if (wspr_zone4_df.freq[i] < 1.9) and (wspr_zone4_df.freq[i] > 1.8):
        zone4_160m.append([wspr_zone4_df.dates[i],wspr_zone4_df.time[i],wspr_zone4_df.snr[i],wspr_zone4_df.freq[i],wspr_zone4_df.call[i],wspr_zone4_df.gs[i],wspr_zone4_df.pwr[i]])
    if (wspr_zone4_df.freq[i] < 4) and (wspr_zone4_df.freq[i] > 3.5):
        zone4_80m.append([wspr_zone4_df.dates[i],wspr_zone4_df.time[i],wspr_zone4_df.snr[i],wspr_zone4_df.freq[i],wspr_zone4_df.call[i],wspr_zone4_df.gs[i],wspr_zone4_df.pwr[i]])        
    if (wspr_zone4_df.freq[i] < 7.1) and (wspr_zone4_df.freq[i] > 6.9):
        zone4_40m.append([wspr_zone4_df.dates[i],wspr_zone4_df.time[i],wspr_zone4_df.snr[i],wspr_zone4_df.freq[i],wspr_zone4_df.call[i],wspr_zone4_df.gs[i],wspr_zone4_df.pwr[i]])
    if (wspr_zone4_df.freq[i] < 10.2) and (wspr_zone4_df.freq[i] > 10.1):
        zone4_30m.append([wspr_zone4_df.dates[i],wspr_zone4_df.time[i],wspr_zone4_df.snr[i],wspr_zone4_df.freq[i],wspr_zone4_df.call[i],wspr_zone4_df.gs[i],wspr_zone4_df.pwr[i]])
    if (wspr_zone4_df.freq[i] < 14.1) and (wspr_zone4_df.freq[i] > 13.9):
        zone4_20m.append([wspr_zone4_df.dates[i],wspr_zone4_df.time[i],wspr_zone4_df.snr[i],wspr_zone4_df.freq[i],wspr_zone4_df.call[i],wspr_zone4_df.gs[i],wspr_zone4_df.pwr[i]])
    if (wspr_zone4_df.freq[i] < 21.1) and (wspr_zone4_df.freq[i] > 21.0):
        zone4_15m.append([wspr_zone4_df.dates[i],wspr_zone4_df.time[i],wspr_zone4_df.snr[i],wspr_zone4_df.freq[i],wspr_zone4_df.call[i],wspr_zone4_df.gs[i],wspr_zone4_df.pwr[i]])
    if (wspr_zone4_df.freq[i] < 28.2) and (wspr_zone4_df.freq[i] > 28.1):
        zone4_10m.append([wspr_zone4_df.dates[i],wspr_zone4_df.time[i],wspr_zone4_df.snr[i],wspr_zone4_df.freq[i],wspr_zone4_df.call[i],wspr_zone4_df.gs[i],wspr_zone4_df.pwr[i]])


zone4_160m_df=pd.DataFrame(data=zone4_160m)
zone4_80m_df=pd.DataFrame(data=zone4_80m)
zone4_40m_df=pd.DataFrame(data=zone4_40m)
zone4_30m_df=pd.DataFrame(data=zone4_30m)
zone4_20m_df=pd.DataFrame(data=zone4_20m)
zone4_15m_df=pd.DataFrame(data=zone4_15m)
zone4_10m_df=pd.DataFrame(data=zone4_10m)

print('Number of US zone4 datapoints = %d' % (len(wspr_zone4)))


if len(zone4_160m) > 0:
    zone4_160m_df.columns = ['dates','time','snr','freq','call','gs','pwr']
    sorted_zone4_160m = zone4_160m_df.sort_values(by=['dates','time'])
    no_zone4_160m_pts = len(sorted_zone4_160m)
    max_zone4_160m_snr = max(sorted_zone4_160m.snr)
    idx_max_zone4_160m_snr = sorted_zone4_160m[sorted_zone4_160m.snr == max(sorted_zone4_160m.snr)].index[0]
    date_max_zone4_160m_snr = sorted_zone4_160m.dates[idx_max_zone4_160m_snr]
    time_max_zone4_160m_snr = sorted_zone4_160m.time[idx_max_zone4_160m_snr]
    call_max_zone4_160m_snr = sorted_zone4_160m.call[idx_max_zone4_160m_snr]
    grid_max_zone4_160m_snr = sorted_zone4_160m.gs[idx_max_zone4_160m_snr]
    label_160m = '160m\n' 'nopts=' + str(len(sorted_zone4_160m.gs)) + '\ndate maxSNR=' + str(date_max_zone4_160m_snr) + '\ntime maxSNR=' + str(time_max_zone4_160m_snr) + '\ncall maxSNR=' + str(call_max_zone4_160m_snr) + '\ngrid maxSNR=' + str(grid_max_zone4_160m_snr)    
    plt.figure(1)
    plt.hist(sorted_zone4_160m.snr, stacked=True, bins=30, density=False, label=label_160m)
    plt.legend()
    plt.xlabel('SNR')
    plt.ylabel('Frequency')
    plt.title(figtitle)
    print('Number of US zone4 160m datapoints = %d' % (len(sorted_zone4_160m.gs)))
else:
    print('Number of US zone4 160m datapoints = 0')

    
if len(zone4_80m) > 0:
    zone4_80m_df.columns = ['dates','time','snr','freq','call','gs','pwr']
    sorted_zone4_80m = zone4_80m_df.sort_values(by=['dates','time'])
    no_zone4_80m_pts = len(sorted_zone4_80m)
    max_zone4_80m_snr = max(sorted_zone4_80m.snr)
    idx_max_zone4_80m_snr = sorted_zone4_80m[sorted_zone4_80m.snr == max(sorted_zone4_80m.snr)].index[0]
    date_max_zone4_80m_snr = sorted_zone4_80m.dates[idx_max_zone4_80m_snr]
    time_max_zone4_80m_snr = sorted_zone4_80m.time[idx_max_zone4_80m_snr]
    call_max_zone4_80m_snr = sorted_zone4_80m.call[idx_max_zone4_80m_snr]
    grid_max_zone4_80m_snr = sorted_zone4_80m.gs[idx_max_zone4_80m_snr]
    label_80m = '80m\n' 'nopts=' + str(len(sorted_zone4_80m.gs)) + '\ndate maxSNR=' + str(date_max_zone4_80m_snr) + '\ntime maxSNR=' + str(time_max_zone4_80m_snr) + '\ncall maxSNR=' + str(call_max_zone4_80m_snr) + '\ngrid maxSNR=' + str(grid_max_zone4_80m_snr)
    plt.figure(2)
    plt.hist(sorted_zone4_80m.snr, stacked=True, bins=30, density=False, label=label_80m)
    plt.legend()
    plt.xlabel('SNR')
    plt.ylabel('Frequency')
    plt.title(figtitle)
    print('Number of US zone4 80m datapoints = %d' % (len(sorted_zone4_80m.gs)))
else:
    print('Number of US zone4 80m datapoints = 0')    

    
if len(zone4_40m) > 0:    
    zone4_40m_df.columns = ['dates','time','snr','freq','call','gs','pwr']
    sorted_zone4_40m = zone4_40m_df.sort_values(by=['dates','time'])
    no_zone4_40m_pts = len(sorted_zone4_40m)
    max_zone4_40m_snr = max(sorted_zone4_40m.snr)
    idx_max_zone4_40m_snr = sorted_zone4_40m[sorted_zone4_40m.snr == max(sorted_zone4_40m.snr)].index[0]
    date_max_zone4_40m_snr = sorted_zone4_40m.dates[idx_max_zone4_40m_snr]
    time_max_zone4_40m_snr = sorted_zone4_40m.time[idx_max_zone4_40m_snr]
    call_max_zone4_40m_snr = sorted_zone4_40m.call[idx_max_zone4_40m_snr]
    grid_max_zone4_40m_snr = sorted_zone4_40m.gs[idx_max_zone4_40m_snr]
    label_40m = '40m\n' 'nopts=' + str(len(sorted_zone4_40m.gs)) + '\ndate maxSNR=' + str(date_max_zone4_40m_snr) + '\ntime maxSNR=' + str(time_max_zone4_40m_snr) + '\ncall maxSNR=' + str(call_max_zone4_40m_snr) + '\ngrid maxSNR=' + str(grid_max_zone4_40m_snr)
    plt.figure(3)
    plt.hist(sorted_zone4_40m.snr, stacked=True, bins=30, density=False, label=label_40m)
    plt.legend()
    plt.xlabel('SNR')
    plt.ylabel('Frequency')
    plt.title(figtitle)
    print('Number of US zone4 40m datapoints = %d' % (len(sorted_zone4_40m.gs)))   
else:
    print('Number of US zone4 40m datapoints = 0') 

    
if len(zone4_30m) > 0:
    zone4_30m_df.columns = ['dates','time','snr','freq','call','gs','pwr']
    sorted_zone4_30m = zone4_30m_df.sort_values(by=['dates','time'])
    no_zone4_30m_pts = len(sorted_zone4_30m)
    max_zone4_30m_snr = max(sorted_zone4_30m.snr)
    idx_max_zone4_30m_snr = sorted_zone4_30m[sorted_zone4_30m.snr == max(sorted_zone4_30m.snr)].index[0]
    date_max_zone4_30m_snr = sorted_zone4_30m.dates[idx_max_zone4_30m_snr]
    time_max_zone4_30m_snr = sorted_zone4_30m.time[idx_max_zone4_30m_snr]
    call_max_zone4_30m_snr = sorted_zone4_30m.call[idx_max_zone4_30m_snr]
    grid_max_zone4_30m_snr = sorted_zone4_30m.gs[idx_max_zone4_30m_snr]
    label_30m = '30m\n' 'nopts=' + str(len(sorted_zone4_30m.gs)) + '\ndate maxSNR=' + str(date_max_zone4_30m_snr) + '\ntime maxSNR=' + str(time_max_zone4_30m_snr) + '\ncall maxSNR=' + str(call_max_zone4_30m_snr) + '\ngrid maxSNR=' + str(grid_max_zone4_30m_snr)
    plt.figure(4)
    plt.hist(sorted_zone4_30m.snr, stacked=True, bins=30, density=False, label=label_30m)
    plt.legend()
    plt.xlabel('SNR')
    plt.ylabel('Frequency')
    plt.title(figtitle)
    print('Number of US zone4 30m datapoints = %d' % (len(sorted_zone4_30m.gs)))
else:
    print('Number of US zone4 30m datapoints = 0')     

    
if len(zone4_20m) > 0:    
    zone4_20m_df.columns = ['dates','time','snr','freq','call','gs','pwr']
    sorted_zone4_20m = zone4_20m_df.sort_values(by=['dates','time'])
    no_zone4_20m_pts = len(sorted_zone4_20m)
    max_zone4_20m_snr = max(sorted_zone4_20m.snr)
    idx_max_zone4_20m_snr = sorted_zone4_20m[sorted_zone4_20m.snr == max(sorted_zone4_20m.snr)].index[0]
    date_max_zone4_20m_snr = sorted_zone4_20m.dates[idx_max_zone4_20m_snr]
    time_max_zone4_20m_snr = sorted_zone4_20m.time[idx_max_zone4_20m_snr]
    call_max_zone4_20m_snr = sorted_zone4_20m.call[idx_max_zone4_20m_snr]
    grid_max_zone4_20m_snr = sorted_zone4_20m.gs[idx_max_zone4_20m_snr]
    label_20m = '20m\n' 'nopts=' + str(len(sorted_zone4_20m.gs)) + '\ndate maxSNR=' + str(date_max_zone4_20m_snr) + '\ntime maxSNR=' + str(time_max_zone4_20m_snr) + '\ncall maxSNR=' + str(call_max_zone4_20m_snr) + '\ngrid maxSNR=' + str(grid_max_zone4_20m_snr)
    plt.figure(5)
    plt.hist(sorted_zone4_20m.snr, stacked=True, bins=30, density=False, label=label_20m)
    plt.legend()
    plt.xlabel('SNR')
    plt.ylabel('Frequency')
    plt.title(figtitle)
    print('Number of US zone4 20m datapoints = %d' % (len(sorted_zone4_20m.gs)))
else:
    print('Number of US zone4 20m datapoints = 0')    

    
if len(zone4_15m) > 0:    
    zone4_15m_df.columns = ['dates','time','snr','freq','call','gs','pwr']
    sorted_zone4_15m = zone4_15m_df.sort_values(by=['dates','time'])
    no_zone4_15m_pts = len(sorted_zone4_15m)
    max_zone4_15m_snr = max(sorted_zone4_15m.snr)
    idx_max_zone4_15m_snr = sorted_zone4_15m[sorted_zone4_15m.snr == max(sorted_zone4_15m.snr)].index[0]
    date_max_zone4_15m_snr = sorted_zone4_15m.dates[idx_max_zone4_15m_snr]
    time_max_zone4_15m_snr = sorted_zone4_15m.time[idx_max_zone4_15m_snr]
    call_max_zone4_15m_snr = sorted_zone4_15m.call[idx_max_zone4_15m_snr]
    grid_max_zone4_15m_snr = sorted_zone4_20m.gs[idx_max_zone4_15m_snr]
    label_15m = '15m\n' 'nopts=' + str(len(sorted_zone4_15m.gs)) + '\ndate maxSNR=' + str(date_max_zone4_15m_snr) + '\ntime maxSNR=' + str(time_max_zone4_15m_snr) + '\ncall maxSNR=' + str(call_max_zone4_15m_snr) + '\ngrid maxSNR=' + str(grid_max_zone4_15m_snr)
    plt.figure(6)
    plt.hist(sorted_zone4_15m.snr, stacked=True, bins=30, density=False, label=label_15m)
    plt.legend()
    plt.xlabel('SNR')
    plt.ylabel('Frequency')
    plt.title(figtitle)
    print('Number of US zone4 15m datapoints = %d' % (len(sorted_zone4_15m.gs)))
else:
    print('Number of US zone4 15m datapoints = 0')    

    
if len(zone4_10m) > 0:    
    zone4_10m_df.columns = ['dates','time','snr','freq','call','gs','pwr']
    sorted_zone4_10m = zone4_10m_df.sort_values(by=['dates','time'])
    no_zone4_10m_pts = len(sorted_zone4_10m)
    max_zone4_10m_snr = max(sorted_zone4_10m.snr)
    idx_max_zone4_10m_snr = sorted_zone4_10m[sorted_zone4_10m.snr == max(sorted_zone4_10m.snr)].index[0]
    date_max_zone4_10m_snr = sorted_zone4_10m.dates[idx_max_zone4_10m_snr]
    time_max_zone4_10m_snr = sorted_zone4_10m.time[idx_max_zone4_10m_snr]
    call_max_zone4_10m_snr = sorted_zone4_10m.call[idx_max_zone4_10m_snr]
    grid_max_zone4_10m_snr = sorted_zone4_20m.gs[idx_max_zone4_10m_snr]
    label_10m = '10m\n' 'nopts=' + str(len(sorted_zone4_10m.gs)) + '\ndate maxSNR=' + str(date_max_zone4_10m_snr) + '\ntime maxSNR=' + str(time_max_zone4_10m_snr) + '\ncall maxSNR=' + str(call_max_zone4_10m_snr) + '\ngrid maxSNR=' + str(grid_max_zone4_10m_snr)
    plt.figure(7)
    plt.hist(sorted_zone4_10m.snr, stacked=True, bins=30, density=False, label=label_10m)
    plt.legend()
    plt.xlabel('SNR')
    plt.ylabel('Frequency')
    plt.title(figtitle)
    print('Number of US zone4 10m datapoints = %d' % (len(sorted_zone4_10m.gs)))
else:
    print('Number of US zone4 10m datapoints = 0')    

    
# plt.legend()
# plt.grid()
    
# df = pd.concat([pd.DataFrame(a, columns=[f'snr{i}']) for i, a in enumerate([x1, x2, x3], 1)], axis=1)

# df = pd.concat([pd.DataFrame(a, columns=[f'snr{i}']) for i, a in zone4_bands, axis=1)


# query_str='%f <= freq <= %f and %f <= dates <= %f and %f <= time <= %f' % (fmin,fmax,dmin,dmax,tmin,tmax)
# subsetwspr=wspr.query(query_str)
# subsetwspr1=wspr1.query(query_str)

# print('Number of %s datapoints = %d' % (band, len(subsetwspr)))










