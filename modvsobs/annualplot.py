# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 09:41:35 2013

@author: jmanning
"""

import matplotlib.pyplot as plt
from getdata import getemolt_latlon,getobs_tempsalt
from conversions import dm2dd,f2c
import pandas as pd
from numpy import float64
from datetime import datetime
from datetime import timedelta
import datetime as dt
import numpy as np
import netCDF4
def nearlonlat(lon,lat,lonp,latp):
    """
    i,min_dist=nearlonlat(lon,lat,lonp,latp)
    find the closest node in the array (lon,lat) to a point (lonp,latp)
    input:
        lon,lat - np.arrays of the grid nodes, spherical coordinates, degrees
        lonp,latp - point on a sphere
        output:
            i - index of the closest node
            min_dist - the distance to the closest node, degrees
            For coordinates on a plane use function nearxy
            
            Vitalii Sheremet, FATE Project
    """
    cp=np.cos(latp*np.pi/180.)
    # approximation for small distance
    dx=(lon-lonp)*cp
    dy=lat-latp
    dist2=dx*dx+dy*dy
    # dist1=np.abs(dx)+np.abs(dy)
    i=np.argmin(dist2)
    #min_dist=np.sqrt(dist2[i])
    return i#,min_dist 
site=['BN01']
depthinfor=[]
minnumperday=18
numperday=24
intend_to='temp'##############notice intend_to can be 'temp'or'salinity'
surf_or_bott='bott'
starttime=dt.datetime(2003,1,1)
endtime=dt.datetime(2010,12,31)
for k in range(len(site)):
#################read-in obs data##################################
        print site[k]
        [lati,loni,on,bd]=getemolt_latlon(site[k]) # extracts lat/lon based on site code
        print bd
        [lati,loni]=dm2dd(lati,loni)#converts decimal-minutes to decimal degrees
        if surf_or_bott=='bott':
            dept=[bd[0]-0.25*bd[0],bd[0]+.25*bd[0]]
        else:
            dept=[0,5]
        (obs_dt,obs_temp,obs_salt,distinct_dep)=getobs_tempsalt(site[k], input_time=[starttime,endtime], dep=dept)
        depthinfor.append(site[k]+','+str(bd[0])+','+str(distinct_dep[0])+'\n')
        obs_dtindex=[]
        if intend_to=='temp':            
            for kk in range(len(obs_temp)):
                obs_temp[kk]=f2c(obs_temp[kk]) # converts to Celcius
                obs_dtindex.append(datetime.strptime(str(obs_dt[kk])[:10],'%Y-%m-%d'))
            obstso=pd.DataFrame(obs_temp,index=obs_dtindex)
        else:
            for kk in range(len(obs_salt)):
                obs_dtindex.append(datetime.strptime(str(obs_dt[kk])[:10],'%Y-%m-%d'))
            obstso=pd.DataFrame(obs_salt,index=obs_dtindex)   
        print 'obs Dataframe is ready'
        resamdaobs=float64(obstso[0]).resample('A',how=['count','mean'])
        
        resamdaobs.ix[resamdaobs['count']<7500,['mean']] = 'NaN'
        resamdaobsdot=resamdaobs[(resamdaobs['count']>7500) & (resamdaobs['count']<8160)]
        #starttime=obs_dt[0].replace(tzinfo=None)
        #endtime=obs_dt[-1].replace(tzinfo=None)
        
        if surf_or_bott=='bott':
            layer=44
            vname=intend_to
            urlfvcom = 'http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3'
            nc = netCDF4.Dataset(urlfvcom)
            nc.variables
            lat = nc.variables['lat'][:]
            lon = nc.variables['lon'][:]
            times = nc.variables['time']
            jd = netCDF4.num2date(times[:],times.units)
            var = nc.variables[vname]
            print 'Now find the coincide timestample'
            inode = nearlonlat(lon,lat,loni,lati)
            print inode
            modindex=netCDF4.date2index([starttime,endtime],times,select='nearest')
            print "now gnerate Dateframe"
            modtso=pd.DataFrame(var[modindex[0]:modindex[1],layer,inode],index=jd[modindex[0]:modindex[1]])
            '''
            for mm in range(len(modtso)):
               if modtso.index[mm].month==1:
                   modtso[0][mm]=modtso[0][mm]-0.15
               if modtso.index[mm].month==2:
                   modtso[0][mm]=modtso[0][mm]-0.12
               if modtso.index[mm].month==3:
                   modtso[0][mm]=modtso[0][mm]-0.08
               if modtso.index[mm].month==4:
                   modtso[0][mm]=modtso[0][mm]-0.13
               if modtso.index[mm].month==5:
                   modtso[0][mm]=modtso[0][mm]-0.57
               if modtso.index[mm].month==6:
                   modtso[0][mm]=modtso[0][mm]-0.81
               if modtso.index[mm].month==7:
                   modtso[0][mm]=modtso[0][mm]-1.06
               if modtso.index[mm].month==8:
                   modtso[0][mm]=modtso[0][mm]-1.13 
               if modtso.index[mm].month==9:
                   modtso[0][mm]=modtso[0][mm]-1.03
               if modtso.index[mm].month==10:
                   modtso[0][mm]=modtso[0][mm]-0.56 
               if modtso.index[mm].month==11:
                   modtso[0][mm]=modtso[0][mm]-0.08
               if modtso.index[mm].month==12:
                   modtso[0][mm]=modtso[0][mm]-0.12     
                   
            '''
            resamdamod=float64(modtso[0]).resample('A',how=['count','mean'])
        
            resamdamod.ix[resamdamod['count']<8160,['mean']] = 'NaN'
            #resamdamod['mean'] += resamdaobs['mean']*0
            #resamdamoddot=resamdamod[(resamdamod['count']>7500) & (resamdamod['count']<8160)]
            fig=plt.figure()
            ax=fig.add_subplot(111)
            ax.plot_date(resamdaobs.index-1,resamdaobs['mean'],fmt='o-')
            ax.plot_date(resamdamod.index-1,resamdamod['mean'],fmt='o-',color='red')#bottom most value equals 44
            plt.grid()
            ax.plot_date(resamdaobsdot.index-(timedelta(days=365)),resamdaobsdot['mean'],marker='o',markersize=20)
            if intend_to=='temp':
                plt.ylabel('degree C',fontsize=20)
            else:
                plt.ylabel('salinity')
            plt.title('eMOLT site '+site[k]+'annual mean vs FVCOM ',fontsize=20)
            plt.legend(['observed','modeled'],loc='best')
            ax.tick_params(axis='both', which='major', labelsize=15)
            plt.show()
            plt.savefig(site[k]+surf_or_bott+intend_to+' annual_mod_obs2.png')
            '''
            fig=plt.figure()
            ax=fig.add_subplot(111)
            ax.plot_date(obstso.index,obstso[0],fmt='-')
            ax.plot_date(modtso.index,modtso[0],fmt='-',color='red')#bottom most value equals 44
            plt.grid()
            plt.show()
            '''