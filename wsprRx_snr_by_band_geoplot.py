# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 21:40:47 2018

@author: Jon Chin & Gregg Daugherty (WB6YAZ)
"""
from pyhamtools.locator import locator_to_latlong
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point #,LineString,Polygon
import paramiko
# from pyproj import CRS

#%%

mygs = 'FN20wb'
band = '40m'
callsign = 'WB6YAZ'
antenna = 'Longwire'
dmin = 210201
dmax = 210202
tmin = 0
tmax = 2359

host = "yourIP"
port = 22
transport = paramiko.Transport((host, port)) 
password = "yourpassword"
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

#%%

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
    print('No band found')
    

mygpsloc= [locator_to_latlong(mygs)]
mypts=[Point(gpspoint[1],gpspoint[0]) for gpspoint in mygpsloc]

d = {'myloc':[ 1 ]}
df = pd.DataFrame(data=d)

crs = {'init': 'epsg:4326'}
# crs='EPSG:4326'
# crs_4326 = CRS('EPSG:4326')

df=gpd.GeoDataFrame(df, crs=crs, geometry=mypts)
# df = gpd.GeoDataFrame(df, crs=crs, geometry=mypts)


#%%

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
     elif(len(str_list)) < 17:
         print('skipped line# =',i+1)
     i=i+1
print('number of datapoints =',i)
f.close()
print('Number of skipped datapoints =',i-len(n3))
                                              

gpsloc= [locator_to_latlong(n) for n in gs]
pts=[Point(gpspoint[1],gpspoint[0]) for gpspoint in gpsloc]
d={'dates': dates,'time':time,'snr':snr,'drift':drift,'freq':freq,'call':call,'gs':gs,'pwr':pwr,'gpsLoc':gpsloc,'pts':pts}
d1={'dates': dates,'time':time,'snr':snr,'drift':drift,'freq':freq,'call':call,'gs':gs,'pwr':pwr}
wspr=pd.DataFrame(data=d)
wspr1=pd.DataFrame(data=d1)

query_str='%f <= freq <= %f and %f <= dates <= %f and %f <= time <= %f' % (fmin,fmax,dmin,dmax,tmin,tmax)
subsetwspr=wspr.query(query_str)
subsetwspr1=wspr1.query(query_str)

#%%
# world=gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

#crs = {'init': 'epsg:4326'}
# fig,ax = plt.subplots()
fig,ax = plt.subplots(figsize=(24,12))

ax.set_aspect('equal')

fp = 'C:\\users\\gregg\\Documents\\Python\\wspr_analysis\\grid_square\\Maidenhead_Locator_World_Grid.shp'

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

data = gpd.read_file(fp)

data.apply(lambda x: ax.annotate(text=x.Name, xy=x.geometry.centroid.coords[0], ha='center', fontfamily='sans-serif', fontsize=6, fontweight='ultralight'),axis=1)

plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
gf=gpd.GeoDataFrame(subsetwspr, crs=crs, geometry='pts')
ax=world.plot(alpha = .5,ax=ax)
#world.boundary.plot(ax=ax, edgecolor='dodgerblue', lw=0.75)
data.boundary.plot(ax=ax, color='black', lw=0.1)

vmin=subsetwspr.min()['snr'];
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

# tbox = '1'

def onpick(event):

    textstr = subsetwspr1.iloc[event.ind]
    print('--------------')
    print(textstr)
    print('--------------')
    
    # global tbox = ''
    # tbox_date = []
    # tbox_time = []
    # tbox_snr = []
    # tbox_drift = []
    # tbox_freq = []
    # tbox_call = []
    # tbox_gs = []
    # tbox_pwr = []
    # for i in range(0,len(textstr)):
    #     tbox_date.append(textstr.iloc[i,0])
    #     tbox_time.append(textstr.iloc[i,1])
    #     tbox_snr.append(textstr.iloc[i,2])
    #     tbox_drift.append(textstr.iloc[i,3])
    #     tbox_freq.append(textstr.iloc[i,4])
    #     tbox_call.append(textstr.iloc[i,5])
    #     tbox_gs.append(textstr.iloc[i,6])
    #     tbox_pwr.append(textstr.iloc[i,7])
    # tbox = '\n'.join(('Date: '+ str(tbox_date[0]),
    #                   'Time: ' + str(tbox_time[0]),
    #                   'SNR: ' + str(tbox_snr[0]),
    #                   'Drift: ' + str(tbox_drift[0]),
    #                   'Freq: ' + str(tbox_freq[0]),
    #                   'Call: ' + str(tbox_call[0]),
    #                   'Grid: ' + str(tbox_gs[0]),
    #                   'Pwr: ' + str(tbox_pwr[0])))
    # print(tbox)
    
    # fig,ax = plt.subplots(figsize=(24,12))

    # ax.set_aspect('equal')

    # fp = 'C:\\users\\gregg\\Documents\\Python\\wspr_analysis\\grid_square\\Maidenhead_Locator_World_Grid.shp'

    # world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    # data = gpd.read_file(fp)

    # data.apply(lambda x: ax.annotate(text=x.Name, xy=x.geometry.centroid.coords[0], ha='center', fontfamily='sans-serif', fontsize=6, fontweight='ultralight'),axis=1)

    # plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    # gf=gpd.GeoDataFrame(subsetwspr, crs=crs, geometry='pts')
    # ax=world.plot(alpha = .5,ax=ax)
    # #world.boundary.plot(ax=ax, edgecolor='dodgerblue', lw=0.75)
    # data.boundary.plot(ax=ax, color='black', lw=0.1)

    # vmin=subsetwspr.min()['snr'];
    # vmax=subsetwspr.max()['snr']

    # gf.plot(column='snr',ax=ax,cmap='jet',markersize=10,vmin=vmin, vmax=vmax,picker=2)
    # df.plot(ax=ax,marker='x',color='r',markersize=25)
    # fig = ax.get_figure()
    # cax = plt.axes([0.85, 0.1, 0.03, 0.8])
    # sm = plt.cm.ScalarMappable(cmap='jet', norm=plt.Normalize(vmin=vmin, vmax=vmax))

    # sm._A = []
    # cbar = fig.colorbar(sm, cax=cax)
    # cbar.ax.set_title('SNR')
    # props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    # # ax.text(50, -25, tbox, transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=props)
    # ax.text(-150, -75, tbox, fontsize=10, bbox=props)
    # ax.set_title('WSPR RX from %s (%s): Dmin=%d, Dmax=%d, Time(Z)=%d-%d, Freq=%s, Ant=%s' % (callsign,mygs,dmin,dmax,tmin,tmax,band,antenna))
    # ax.set_xlabel('Longitude')
    # ax.set_ylabel('Latitude')

fig.canvas.mpl_connect('pick_event', onpick)

