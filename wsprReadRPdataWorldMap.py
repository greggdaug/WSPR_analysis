# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 21:40:47 2018

@author: Jon Chin & Gregg Daugherty (WB6YAZ)
"""
from pyhamtools.locator import locator_to_latlong
import os
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point #,LineString,Polygon
from haversine import haversine, Unit
import maidenhead as mh

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

#%%
mygs = 'FN20xb'
band = '630m'
callsign = 'WB6YAZ'
antenna = 'Longwire'
dmin = 200211
dmax = 200211
tmin = 0
tmax = 2300

#f=open('All_WSPR2.TXT')
#f=open('C:\\Users\\gregg\\AppData\\Local\\WSJT-X\\All_WSPR.TXT')
#rp_dir = r'\\10.0.0.188\dev\shm'
#os.listdir(rp_dir)
f=open('test\All_WSPR_cpy.TXT')
txt=f.read()

if band == '2190m':
    fmin = 0.13
    fmax = 0.14
elif band == '630m':
    fmin = 0.47
    fmax = 0.48
elif band == '160m':
    fmin = 1.8
    fmax = 1.9
elif band == '80m':
    fmin = 3.5
    fmax = 3.6
elif band == '40m':
    fmin = 6.9
    fmax = 7.1
elif band == '30m':
    fmin = 10.1
    fmax = 10.2
elif band == '20m':
    fmin = 13.9
    fmax = 14.1
elif band == '17m':
    fmin = 18.1
    fmax = 18.2
elif band == '15m':
    fmin = 21.0
    fmax = 21.1
elif band == '12m':
    fmin = 24.0
    fmax = 24.1
elif band == '10m':
    fmin = 28.0
    fmax = 28.1
elif band == '6m':
    fmin = 50.2
    fmax = 50.3
elif band == '2m':
    fmin = 144.4
    fmax = 144.5
elif band == '70cm':
    fmin = 432.0
    fmax = 433.0
elif band == '23cm':
    fmin = 1296.0
    fmax = 1297.0
else:
    print('band =',band)
    

mygpsloc= [locator_to_latlong(mygs)]
mypts=[Point(gpspoint[1],gpspoint[0]) for gpspoint in mygpsloc]

d = {'myloc':[ 1 ]}
df = pd.DataFrame(data=d)
crs = {'init': 'epsg:4326'}

df=gpd.GeoDataFrame(df, crs=crs, geometry=mypts)

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

for i in range(0,len(gs)-1):
    if(gs[i] == gs[i+1]):
        gsx=gsx+1
        
print('number of different locations =',gsx)
                                              

gpsloc= [locator_to_latlong(n) for n in gs]
pts=[Point(gpspoint[1],gpspoint[0]) for gpspoint in gpsloc]
d={'dates': dates,'time':time,'snr':snr,'drift':drift,'freq':freq,'call':call,'gs':gs,'pwr':pwr,'gpsLoc':gpsloc,'pts':pts}
d1={'dates': dates,'time':time,'snr':snr,'drift':drift,'freq':freq,'call':call,'gs':gs,'pwr':pwr}
wspr=pd.DataFrame(data=d)
wspr1=pd.DataFrame(data=d1)

dist_km = []
dist_mi = []

for i in range(0,len(wspr)):
   dist_km.append(haversine(mh.toLoc(mygs),mh.toLoc(str(wspr.iat[i,5]))))
   dist_mi.append(haversine(mh.toLoc(mygs),mh.toLoc(str(wspr.iat[i,5])),unit='mi'))
   
#wspr['dist_km'] = dist_km
wspr['dist_mi'] = dist_mi
#wspr1['dist_km'] = dist_km
wspr1['dist_mi'] = dist_mi

print(wspr)

if(band == 'all'):
    query_str='%f <= dates <= %f and %f <= time <= %f' % (dmin,dmax,tmin,tmax)
else:
    query_str='%f <= freq <= %f and %f <= dates <= %f and %f <= time <= %f' % (fmin,fmax,dmin,dmax,tmin,tmax)
#query_str='%f <= dates <= %f and %f <= time <= %f' % (dmin,dmax,tmin,tmax)
subsetwspr=wspr.query(query_str)
subsetwspr1=wspr1.query(query_str)

#%%
world=gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

crs = {'init': 'epsg:4326'}
fig,ax = plt.subplots()
plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
gf=gpd.GeoDataFrame(subsetwspr, crs=crs, geometry='pts')
ax=world.plot(alpha = .5,ax=ax)

vmin=subsetwspr.min()['snr']
vmax=subsetwspr.max()['snr']

gf.plot(column='snr',ax=ax,cmap='jet',markersize=10,vmin=vmin, vmax=vmax,picker=2)
df.plot(ax=ax,marker='x',color='r',markersize=25)
fig = ax.get_figure()
cax = plt.axes([0.85, 0.1, 0.03, 0.8])
sm = plt.cm.ScalarMappable(cmap='jet', norm=plt.Normalize(vmin=vmin, vmax=vmax))

sm._A = []
cbar = fig.colorbar(sm, cax=cax)
cbar.ax.set_title('SNR')

ax.set_title('WSPR RX from %s (%s): Dmin=%d, Dmax=%d, Time(Z)=%d-%d, Freq=%s, Ant=%s' % (callsign,mygs,dmin,dmax,tmin,tmax,band,antenna))
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

def onpick(event):
    print('--------------')
    print(subsetwspr1.iloc[event.ind])
    print('--------------')        

fig.canvas.mpl_connect('pick_event', onpick)