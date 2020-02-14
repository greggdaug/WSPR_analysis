# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 06:39:55 2018

@author: gregg
"""

#from pyhamtools.locator import locator_to_latlong
#import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import maidenhead as mh
from haversine import haversine, Unit
import numpy as np
#import matplotlib.colors as colors
#from mpl_toolkits.mplot3d import Axes3D
#from shapely.geometry import Point #,LineString,Polygon

#%%
mygs = 'FN20xb'
band = '40m'
callsign = 'WB6YAZ'
antenna = 'Longwire'
dmin = 200210   
dmax = 200210 
tmin = 0
tmax = 2300

import paramiko
host = "ip addr" # IP address of RedPitaya
port = 22
transport = paramiko.Transport((host, port)) 
password = "password"
username = "root"
transport.connect(username = username, password = password)
sftp = paramiko.SFTPClient.from_transport(transport)
filepath = '/dev/shm/ALL_WSPR.TXT'
localpath = r'C:\Users\gregg\Documents\Python\test\ALL_WSPR_cpy.TXT'
#sftp.put(localpath, filepath)
sftp.get(filepath, localpath)
sftp.close()
transport.close()
#
f=open('test\All_WSPR_cpy.TXT')
#f=open(r'C:\Users\gregg\Documents\Python\test\ALL_WSPR_cpy.TXT')
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
gsx=0

allLN=txt.splitlines(); # split by row
for ln in allLN: # for every line
     tmp=ln.split()
     str_list = list(filter(None, tmp))#remove spaces
     if(len(str_list) == 14):
         dates.append(float(str_list[0]))
         time.append(float(str_list[1]))
         n0.append(str_list[2])
         snr.append(float(str_list[3]))
         drift.append(str_list[4])
         freq.append(float(str_list[5]))
         call.append(str_list[6])
         gs.append(str_list[7])
         pwr.append(str_list[8])
         n1.append(str_list[9])
         n2.append(str_list[10])
         n3.append(str_list[11])
         n4.append(str_list[12])
         n5.append(str_list[13])
     elif(len(str_list)) < 14:
#         prtstr=('skipped line# = %d, prev line callsign = %s' % (i-1,call[i-1]))
        #print('skipped line# =',i-1,'prev line callsign =', call[i-1])
#         print(prtstr)
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

subsetwspr1_630m=wspr1.query(query_str_630m)
subsetwspr1_160m=wspr1.query(query_str_160m)
subsetwspr1_80m=wspr1.query(query_str_80m)
subsetwspr1_40m=wspr1.query(query_str_40m)
subsetwspr1_20m=wspr1.query(query_str_20m)
subsetwspr1_15m=wspr1.query(query_str_15m)
subsetwspr1_10m=wspr1.query(query_str_10m)

subsort_630m=subsetwspr1_630m.sort_values('call')
subsort_160m=subsetwspr1_160m.sort_values('call')
subsort_80m=subsetwspr1_80m.sort_values('call')
subsort_40m=subsetwspr1_40m.sort_values('call')
subsort_20m=subsetwspr1_20m.sort_values('call')
subsort_15m=subsetwspr1_15m.sort_values('call')
subsort_10m=subsetwspr1_10m.sort_values('call')

if band == '630m':
    df=subsort_630m
elif band == '160m':
    df=subsort_160m
elif band == '80m':
    df=subsort_80m
elif band == '40m':
    df=subsort_40m
elif band == '20m':
    df=subsort_20m
elif band == '15m':
    df=subsort_15m
elif band == '10m':
    df=subsort_10m

print('number of 630m datapoints =', len(subsort_630m.call))
print('number of 160m datapoints =', len(subsort_160m.call))
print('number of 80m datapoints =', len(subsort_80m.call))
print('number of 40m datapoints =', len(subsort_40m.call))
print('number of 20m datapoints =', len(subsort_20m.call))
print('number of 15m datapoints =', len(subsort_15m.call))
print('number of 10m datapoints =', len(subsort_20m.call))

#%%
print()
#dfgs = df.gs
#print(df)
#print(dfgs)

dist_km = []
dist_mi = []

#mygs_ary=mygs*np.ones((len(df),1))

for i in range(0,len(df)):
   dist_km.append(haversine(mh.toLoc(mygs),mh.toLoc(str(df.iat[i,4]))))
   dist_mi.append(haversine(mh.toLoc(mygs),mh.toLoc(str(df.iat[i,4])),unit='mi'))
   
df['dist_mi'] = dist_mi
df['dist_km'] = dist_km
   
print(df)
    

#dist_km = haversine(mygs,df.iat[0,4])
#dist_mi = haversine(mygs_ary,df.iat[0:4],unit='mi')

#print(dist_km)
#print(dist_mi)
#
#vmin=subsort_630m.min()['snr']
#vmax=subsort_630m.max()['snr']

#normalize = colors.Normalize(vmin=vmin, vmax=vmax)
#colormap = 'jet'

vmin=df.min()['snr']
vmax=df.max()['snr']

fig,ax=plt.subplots()
plt.subplots_adjust(bottom=0.2, right=0.8, top=0.9)

ax.scatter(x='call', y='time', data=df, c='snr', cmap='jet', picker=2)

#for i, txt in enumerate(df.snr):
#    ax.annotate(txt, (df.call.iat[i],df.time.iat[i]), xytext=(5,0), textcoords='offset points',family='sans-serif', size=8, color='darkslategrey')
    
for tick in ax.get_xticklabels():
    tick.set_rotation(90)
    
fig = ax.get_figure()

cax = plt.axes([0.85, 0.2, 0.03, 0.7])
sm = plt.cm.ScalarMappable(cmap='jet', norm=plt.Normalize(vmin=vmin, vmax=vmax))

sm._A = []
cbar = fig.colorbar(sm, cax=cax)
cbar.ax.set_title('SNR')

ax.set_title('WSPR RX from %s (%s): Dmin=%d, Dmax=%d, Time(Z)=%d-%d, Freq=%s, Ant=%s' % (callsign,mygs,dmin,dmax,tmin,tmax,band,antenna))
ax.set_xlabel('Location')
ax.set_ylabel('Time(Z)')

def onpick(event):
    print('--------------')
    print(df.iloc[event.ind])
    print('--------------')        

fig.canvas.mpl_connect('pick_event', onpick)

