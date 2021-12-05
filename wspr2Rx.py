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
antenna1 = 'Longwire'
antenna2 = 'EWFD'
dmin = 210917   
dmax = 210917 
tmin = 0
tmax = 2300
searchcall = 'KC2TER'

fname1 = r'C:\Users\gregg\Documents\Python\wspr_analysis\ALL_WSPR_longwire_091921.TXT'
f1=open(fname1)
txt1=f1.read()

fname2 = r'C:\Users\gregg\Documents\Python\wspr_analysis\ALL_WSPR_ewfd_091921.TXT'
f2=open(fname2)
txt2=f2.read()

#%%

dates1=[]
time1=[]
n0_1=[]
snr1=[]
drift1=[]
freq1=[]
call1=[]
gs1=[]
pwr1=[]
n1_1=[]
n2_1=[]
n3_1=[]
n4_1=[]
n5_1=[]

dates2=[]
time2=[]
n0_2=[]
snr2=[]
drift2=[]
freq2=[]
call2=[]
gs2=[]
pwr2=[]
n1_2=[]
n2_2=[]
n3_2=[]
n4_2=[]
n5_2=[]

i=0

allLN1=txt1.splitlines(); # split by row
for ln in allLN1: # for every line
     tmp=ln.split()
     str_list = list(filter(None, tmp))#remove spaces
     if(len(str_list) == 17):
         dates1.append(float(str_list[0]))
         time1.append(float(str_list[1]))
         snr1.append(float(str_list[2]))
         drift1.append(str_list[3])
         freq1.append(float(str_list[4]))
         call1.append(str_list[5])
         gs1.append(str_list[6])
         pwr1.append(str_list[7])
         n1_1.append(str_list[8])
         n2_1.append(str_list[9])
         n3_1.append(str_list[10])
     elif(len(str_list)) < 17:
        print('bad line =',str_list)
     i=i+1
print('number of datapoints =',i)
f1.close()
print('Number of skipped datapoints1 =',i-len(n3_1))

i=0

allLN2=txt2.splitlines(); # split by row
for ln in allLN2: # for every line
     tmp=ln.split()
     str_list = list(filter(None, tmp))#remove spaces
     if(len(str_list) == 17):
         dates2.append(float(str_list[0]))
         time2.append(float(str_list[1]))
         snr2.append(float(str_list[2]))
         drift2.append(str_list[3])
         freq2.append(float(str_list[4]))
         call2.append(str_list[5])
         gs2.append(str_list[6])
         pwr2.append(str_list[7])
         n1_2.append(str_list[8])
         n2_2.append(str_list[9])
         n3_2.append(str_list[10])
     elif(len(str_list)) < 17:
        print('bad line =',str_list)
     i=i+1
print('number of datapoints =',i)
f2.close()
print('Number of skipped datapoints2 =',i-len(n3_2))
                                              
#%%
#gpsloc= [locator_to_latlong(n) for n in gs]
#pts=[Point(gpspoint[1],gpspoint[0]) for gpspoint in gpsloc]
#d={'dates': dates,'time':time,'snr':snr,'drift':drift,'freq':freq,'call':call,'gs':gs,'pwr':pwr,'gpsLoc':gpsloc,'pts':pts}
d1={'dates': dates1,'time':time1,'snr':snr1,'drift':drift1,'freq':freq1,'call':call1,'gs':gs1,'pwr':pwr1}
#wspr=pd.DataFrame(data=d)
wspr1=pd.DataFrame(data=d1)

d2={'dates': dates2,'time':time2,'snr':snr2,'drift':drift2,'freq':freq2,'call':call2,'gs':gs2,'pwr':pwr2}
#wspr=pd.DataFrame(data=d)
wspr2=pd.DataFrame(data=d2)

query_str='%f <= dates <= %f and %f <= time <= %f' % (dmin,dmax,tmin,tmax)

wspr1q = wspr1.query(query_str)
wspr2q = wspr2.query(query_str)

wspr1_spots=wspr1q.loc[lambda df: df['call'] == searchcall, :]
wspr2_spots=wspr2q.loc[lambda df: df['call'] == searchcall, :]

df1 = pd.merge(wspr1_spots,wspr2_spots,on='time')

nopts = len(df1)

#%%
#print()
#print(df)
x = []
y1 = []
y2 = []

for i in range(len(df1)):
    x.append(str(df1.dates_x.iat[i]) + ':' + str(df1.time.iat[i]))
    y1.append(df1.snr_x.iat[i])
    y2.append(df1.snr_y.iat[i])
    

fig,ax=plt.subplots()
plt.plot(x,y1,linewidth=2,label='Ant1')
plt.plot(x,y2,linewidth=1,label='Ant2')
plt.legend(loc='best') 
plt.xticks(x[::5], rotation=45)
plt.tight_layout()

ax.set_title('WSPR Rx (%s) from %s: Dmin=%d, Dmax=%d, Time(Z)=%d-%d, Freq=%s, Ant1=%s, Ant2=%s' % (callsign,searchcall,dmin,dmax,tmin,tmax,band,antenna1,antenna2))
ax.set_xlabel('Time(Z)')
ax.set_ylabel('SNR')
ax.text(.01,.85,'TxInfo:' + '\nCall:' + searchcall + '\nGrid: ' + str(df1.gs_x.iloc[0]) + '\nPwr: ' + str(df1.pwr_x.iloc[0]) + '\nNoPts: ' + str(nopts),bbox=dict(facecolor='white', alpha=0.5),transform=ax.transAxes)






