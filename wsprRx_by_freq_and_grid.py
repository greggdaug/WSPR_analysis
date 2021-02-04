# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 06:39:55 2018

@author: wb6yaz - gregg
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import paramiko
# from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
#import matplotlib.dates as dates

#%%
mygs = 'FN20'
band = 'All'
callsign = 'WB6YAZ'
antenna = 'Longwire'
dmin = 210103   
dmax = 210125 
tmin = 0
tmax = 2359
searchgrid = 'CN'


# fname = 'C:\\users\\gregg\\Documents\\Python\\wspr_analysis\\ALL_WSPR.TXT'

host = "192.168.11.142"
port = 22
transport = paramiko.Transport((host, port)) 
password = "radiopi599"
username = "pi"
transport.connect(username = username, password = password)
sftp = paramiko.SFTPClient.from_transport(transport)
filepath = '/home/pi/.local/share/WSJT-X/ALL_WSPR.TXT'
localpath = r'C:\Users\gregg\Documents\Python\wspr_analysis\data\ALL_WSPR_cpy.TXT'
#sftp.put(localpath, filepath)
sftp.get(filepath, localpath)
sftp.close()
transport.close()

# fname = 'C:\\users\\gregg\\Documents\\Python\\wspr_analysis\\ALL_WSPR.TXT'
fname = r'C:\users\gregg\Documents\Python\wspr_analysis\data\ALL_WSPR_cpy.TXT'
f=open(fname)

txt=f.read()

#%%

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

allLN=txt.splitlines(); # split by row
for ln in allLN: # for every line
     tmp=ln.split()
     str_list = list(filter(None, tmp))#remove spaces
     if(len(str_list) >= 17):
         dates.append(float(str_list[0]))
#         dates.append(str_list[0])
         time.append(float(str_list[1]))
#         time.append(str_list[1])
         snr.append(float(str_list[2]))
         drift.append(str_list[3])
         freq.append(float(str_list[4]))
         call.append(str_list[5])
         gs.append(str_list[6])
         pwr.append(str_list[7])
         n1.append(str_list[8])
         n2.append(str_list[9])
         n3.append(str_list[10])
     elif(len(str_list)) < 17:
        print('bad line =',str_list)
     i=i+1
print('number of datapoints =',i)
f.close()
print('Number of skipped datapoints =',i-len(n3))

#datetimestr = []

#for i in range(0,len(dates)):
#    dates1.append(str(dates[i])[0:6])
#    time1.append(str(time[i])[0:4])
#    datetimestr.append(str(dates[i])[0:6] + '%04.0f'% time[i])
                                              
#%%
#gpsloc= [locator_to_latlong(n) for n in gs]
#pts=[Point(gpspoint[1],gpspoint[0]) for gpspoint in gpsloc]
#d={'dates': dates,'time':time,'snr':snr,'drift':drift,'freq':freq,'call':call,'gs':gs,'pwr':pwr,'gpsLoc':gpsloc,'pts':pts}
d1={'dates': dates,'time':time,'snr':snr,'drift':drift,'freq':freq,'call':call,'gs':gs,'pwr':pwr}
#wspr=pd.DataFrame(data=d)
wspr1=pd.DataFrame(data=d1)

xdt = []
xdt1 = []

for i in range(len(wspr1)):
    xdt = str(wspr1.dates.iat[i])[0:6] + '%04.0f' % wspr1.time.iat[i]
    xdt1.append(datetime.strptime(xdt, "%y%m%d%H%M"))
  
wspr2 = wspr1.assign(date_time=xdt1)
wspr2gs = wspr2.gs.str.slice(0,2).astype('string')

# wspr2 = wspr1.assign(date_time_str=str(xdt))

df630m = wspr2.loc[(wspr2.freq < 0.48) & (wspr2.freq > 0.47) & (wspr2gs == searchgrid)]
df160m = wspr2.loc[(wspr2.freq < 1.9) & (wspr2.freq > 1.8) & (wspr2gs == searchgrid)]
df80m = wspr2.loc[(wspr2.freq < 3.6) & (wspr2.freq > 3.5) & (wspr2gs == searchgrid)]
df40m = wspr2.loc[(wspr2.freq < 7.1) & (wspr2.freq > 6.9) & (wspr2gs == searchgrid)]
df20m = wspr2.loc[(wspr2.freq < 14.1) & (wspr2.freq > 13.9) & (wspr2gs == searchgrid)]
df15m = wspr2.loc[(wspr2.freq < 21.1) & (wspr2.freq > 21.0) & (wspr2gs == searchgrid)]   
df10m = wspr2.loc[(wspr2.freq < 28.1) & (wspr2.freq > 28.0) & (wspr2gs == searchgrid)]


print('No of 630m points = ', len(df630m))
print('No of 160m points = ', len(df160m))
print('No of 80m points = ', len(df80m))
print('No of 40m points = ', len(df40m))
print('No of 20m points = ', len(df20m))
print('No of 15m points = ', len(df15m))
print('No of 10m points = ', len(df10m))

# df40m.plot(kind='scatter', x='date_time', y='snr')

# fig = plt.figure(figsize=(24,12))

# ax = fig.add_subplot(111, projection='3d')

# if len(df630m) > 0:
#     ax.scatter(df630m.dates, df630.time, df630m.snr, marker='v', label='630m')
    
# if len(df160m) > 0:
#     ax.scatter(df160m.dates, df160.time, df160m.snr, marker='^', label='160m')
    
# if len(df80m) > 0:
#     ax.scatter(df80m.dates, df80m.time, df80m.snr, marker='p', label='160m')
    
# if len(df40m) > 0:
#     ax.scatter(df40m.dates, df40m.time, df40m.snr, marker='*', label='40m')
   
# if len(df20m) > 0:
#     ax.scatter(df20m.dates, df20m.time, df20m.snr, marker='x', label='20m')

# if len(df15m) > 0:
#     ax.scatter(df15m.dates, df15m.time, df15m.snr, marker='s', label='20m')

# if len(df10m) > 0:
#     ax.scatter(df10m.dates, df10m.time, df10m.snr, marker='P', label='20m')

# ax.set_title('WSPR Rx (%s) from grid: %sxx, Dmin=%d, Dmax=%d, Time(Z)=%d-%d, Freq=%s, Ant=%s' % (callsign,searchgrid,dmin,dmax,tmin,tmax,'All',antenna))
# ax.set_xlabel('Date')
# ax.set_ylabel('Time')
# ax.set_zlabel('SNR')

# plt.legend()

fig,ax=plt.subplots(2, figsize=(24,12))

if len(df630m) > 0:
    ax[0].scatter(df630m.date_time, df630m.snr, marker='v', label='630m')
    ax[1].scatter(df630m.time, df630m.snr, marker='v', label='630m')

if len(df160m) > 0:
    ax[0].scatter(df160m.date_time, df160m.snr, marker='^', label='160m')
    ax[1].scatter(df160m.time, df160m.snr, marker='^', label='160m')

if len(df80m) > 0:
    ax[0].scatter(df80m.date_time, df80m.snr, marker='p', label='80m')
    ax[1].scatter(df80m.time, df80m.snr, marker='p', label='80m')

if len(df40m) > 0:
    ax[0].scatter(df40m.date_time, df40m.snr, marker='*', label='40m')
    ax[1].scatter(df40m.time, df40m.snr, marker='*', label='40m')
    
if len(df20m) > 0:
    ax[0].scatter(df20m.date_time, df20m.snr, marker='x', label='20m')
    ax[1].scatter(df20m.time, df20m.snr, marker='x', label='20m')
    
if len(df15m) > 0:
    ax[0].scatter(df15m.date_time, df15m.snr, marker='s', label='15m')
    ax[1].scatter(df15m.time, df15m.snr, marker='s', label='15m')
    
if len(df10m) > 0:
    ax[0].scatter(df10m.date_time, df10m.snr, marker='P', label='10m')
    ax[1].scatter(df10m.time, df10m.snr, marker='P', label='10m')

ax[0].grid(linestyle='-', linewidth=0.5)
ax[1].grid(linestyle='-', linewidth=0.5)
ax[0].legend()
ax[1].legend()

ax[0].set_title('WSPR Rx (%s) from grid %sxx: Dmin=%d, Dmax=%d, Time(Z)=%d-%d, Freq=%s, Ant=%s' % (callsign,searchgrid,dmin,dmax,tmin,tmax,'All',antenna))
ax[0].set_xlabel('Date')
ax[1].set_xlabel('Time')
ax[0].set_ylabel('SNR')
ax[1].set_ylabel('SNR')

# plt.xticks(rotation=90)

# ax.df20m.plot(kind='scatter', x='date_time', y='snr')

# plt.autofmt_xdate()
         
# plt.tight_layout()

# plt.subplots_adjust(bottom=0.25)

# ax.fmt_xdata = DateFormatter('%y%m%d%H%M')






