# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 06:39:55 2018

@author: wb6yaz - gregg
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#%%
mygs = 'FN20'
band = '40m'
callsign = 'WB6YAZ'
antenna = 'EWFD'
dmin = 211130  
dmax = 211204 
tmin = 0
tmax = 2300
searchcall = 'W6LVP'

fname = r'C:\Users\gregg\Documents\Python\wspr_analysis\ALL_WSPR_ewfd_120921.TXT'
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
     if(len(str_list) == 17):
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
     elif(len(str_list)) < 17:
        print('bad line =',str_list)
     i=i+1
print('number of datapoints =',i)
f.close()
print('Number of skipped datapoints =',i-len(n3))
                                              
#%%
#gpsloc= [locator_to_latlong(n) for n in gs]
#pts=[Point(gpspoint[1],gpspoint[0]) for gpspoint in gpsloc]
#d={'dates': dates,'time':time,'snr':snr,'drift':drift,'freq':freq,'call':call,'gs':gs,'pwr':pwr,'gpsLoc':gpsloc,'pts':pts}
d1={'dates': dates,'time':time,'snr':snr,'drift':drift,'freq':freq,'call':call,'gs':gs,'pwr':pwr}
#wspr=pd.DataFrame(data=d)
wspr1=pd.DataFrame(data=d1)

query_str_630m='%f <= freq <= %f and %f <= dates <= %f and %f <= time <= %f' % (0.47,0.48,dmin,dmax,tmin,tmax)
query_str_160m='%f <= freq <= %f and %f <= dates <= %f and %f <= time <= %f' % (1.8,1.9,dmin,dmax,tmin,tmax)
query_str_80m='%f <= freq <= %f and %f <= dates <= %f and %f <= time <= %f' % (3.5,3.6,dmin,dmax,tmin,tmax)
query_str_40m='%f <= freq <= %f and %f <= dates <= %f and %f <= time <= %f' % (6.9,7.1,dmin,dmax,tmin,tmax)
query_str_20m='%f <= freq <= %f and %f <= dates <= %f and %f <= time <= %f' % (13.9,14.1,dmin,dmax,tmin,tmax)
query_str_15m='%f <= freq <= %f and %f <= dates <= %f and %f <= time <= %f' % (21.0,21.1,dmin,dmax,tmin,tmax)
query_str_10m='%f <= freq <= %f and %f <= dates <= %f and %f <= time <= %f' % (28.0,28.1,dmin,dmax,tmin,tmax)

try:
    subsetwspr1_630m=wspr1.query(query_str_630m)
    unique_calls_630m = np.unique(subsetwspr1_630m.call)
    unique_gs_630m = np.unique(subsetwspr1_630m.gs)
    wspr1_630m=subsetwspr1_630m.loc[lambda df: df['call'] == searchcall, :]
except:
    print('630m no data')

try:   
    subsetwspr1_160m=wspr1.query(query_str_160m)
    unique_calls_160m = np.unique(subsetwspr1_160m.call)
    unique_gs_160m = np.unique(subsetwspr1_160m.gs)
    wspr1_160m=subsetwspr1_160m.loc[lambda df: df['call'] == searchcall, :]
except:
    print('160m no data')
    
try:
    subsetwspr1_80m=wspr1.query(query_str_80m)
    unique_calls_80m = np.unique(subsetwspr1_80m.call)
    unique_gs_80m = np.unique(subsetwspr1_80m.gs)
    wspr1_80m=subsetwspr1_80m.loc[lambda df: df['call'] == searchcall, :]
except:
    print('80m no data')
    
try:
    subsetwspr1_40m=wspr1.query(query_str_40m)
    unique_calls_40m = np.unique(subsetwspr1_40m.call)
    unique_gs_40m = np.unique(subsetwspr1_40m.gs)
    wspr1_40m=subsetwspr1_40m.loc[lambda df: df['call'] == searchcall, :]
except:
    print('40m no data')
    
try:
    subsetwspr1_20m=wspr1.query(query_str_20m)
    unique_calls_20m = np.unique(subsetwspr1_20m.call)
    unique_gs_20m = np.unique(subsetwspr1_20m.gs)
    wspr1_20m=subsetwspr1_20m.loc[lambda df: df['call'] == searchcall, :]
except:
    print('20m no data')
    
try:
    subsetwspr1_15m=wspr1.query(query_str_15m)
    unique_calls_15m = np.unique(subsetwspr1_15m.call)
    unique_gs_15m = np.unique(subsetwspr1_15m.gs)
    wspr1_15m=subsetwspr1_15m.loc[lambda df: df['call'] == searchcall, :]
except:
    print('15m no data')
    
try:
    subsetwspr1_10m=wspr1.query(query_str_10m)
    unique_calls_10m = np.unique(subsetwspr1_10m.call)
    unique_gs_10m = np.unique(subsetwspr1_10m.gs)
    wspr1_10m=subsetwspr1_10m.loc[lambda df: df['call'] == searchcall, :]
except:
    print('10m no data')


if band == '630m':
    df=wspr1_630m
elif band == '160m':
    df=wspr1_160m
elif band == '80m':
    df=wspr1_80m
elif band == '40m':
    df=wspr1_40m
elif band == '20m':
    df=wspr1_20m
elif band == '15m':
    df=wspr1_15m
elif band == '10m':
    df=wspr1_10m
    
print()

print('number of 630m datapoints =', len(wspr1_630m))
print('number of 160m datapoints =', len(wspr1_160m))
print('number of 80m datapoints =', len(wspr1_80m))
print('number of 40m datapoints =', len(wspr1_40m))
print('number of 20m datapoints =', len(wspr1_20m))
print('number of 15m datapoints =', len(wspr1_15m))
print('number of 10m datapoints =', len(wspr1_20m))

print()

print('selected ' + band + ' callsign = ' + searchcall)

print()

ucalls = vars()['unique_calls_' + band]
print('unique ' + band + ' calls:\n', ucalls)

print()

ugs = vars()['unique_gs_' + band]
print('unique ' + band + ' grids:\n', ugs)

#%%
#print()
#print(df)
x = []
y = []

for i in range(len(df)):
    a = str(df.dates.iat[i]) + ':' + str(df.time.iat[i])
    b = df.snr.iat[i]
    x.append(a)
    y.append(b)
    

fig,ax=plt.subplots()
plt.plot(x,y)
plt.xticks(x[::5], rotation=90)
plt.tight_layout()

ax.set_title('WSPR Rx (%s) from %s: Dmin=%d, Dmax=%d, Time(Z)=%d-%d, Freq=%s, Ant=%s' % (callsign,searchcall,dmin,dmax,tmin,tmax,band,antenna))
ax.set_xlabel('Time(Z)')
ax.set_ylabel('SNR')





