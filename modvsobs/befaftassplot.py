# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 09:33:49 2013

@author: jmanning
"""
from pydap.client import open_url
from matplotlib.dates import num2date
import matplotlib.pyplot as plt
from getdata import getemolt_latlon,getobs_tempsalt
from conversions import dm2dd,f2c
from utilities import my_x_axis_format
import pandas as pd
from numpy import float64
from datetime import datetime, timedelta
from models import getFVCOM_bottom_tempsalt_netcdf
import datetime as dt
import numpy as np
import sys
import netCDF4
from pylab import unique
import matplotlib.dates as dates
def get_dataset(url):
    try:
        dataset = open_url(url)
    except:
        print 'Sorry, ' + url + 'is not available' 
        sys.exit(0)
    return dataset
def nearlonlat(lon,lat,lonp,latp):
    cp=np.cos(latp*np.pi/180.)
    # approximation for small distance
    dx=(lon-lonp)*cp
    dy=lat-latp
    dist2=dx*dx+dy*dy
    # dist1=np.abs(dx)+np.abs(dy)
    i=np.argmin(dist2)
    #min_dist=np.sqrt(dist2[i])
    return i#,min_dist 
site=['NL01']
layer=44
intend_to='temp'##############notice intend_to can be 'temp'or'salinity'
vname=intend_to
surf_or_bott='bott'
month=range(1,13)
for k in range(len(site)):
    fig=plt.figure(figsize=(15,10))
    ax=fig.add_subplot(111)
    for m in range(len(month)):
        month_time=month[m]   
#################read-in obs data##################################
        print site[k]
        [lati,loni,on,bd]=getemolt_latlon(site[k]) # extracts lat/lon based on site code
        print bd
        [lati,loni]=dm2dd(lati,loni)#converts decimal-minutes to decimal degrees
        print lati,loni
        if surf_or_bott=='bott':
            dept=[bd[0]-0.25*bd[0],bd[0]+.25*bd[0]]
            
        else:
            dept=[0,5]
#        (obs_dt,obs_temp,obs_salt,distinct_dep)=getobs_tempsalt(site[k], 
######################################################################################
        if month_time<12:
          input_time=[dt.datetime(2008,int(month_time),1),dt.datetime(2008,int(month_time)+1,1)]
        else:
          input_time=[dt.datetime(2008,int(month_time),1),dt.datetime(2008,int(month_time),31)]  
        dep=dept
        obs_dt,obs_temp,obs_salt,distinct_dep=getobs_tempsalt(site[k],input_time,dep)
        obs_dtindex=[]
        if intend_to=='temp':            
            for kk in range(len(obs_temp)):
                obs_temp[kk]=f2c(obs_temp[kk]) # converts to Celcius
                obs_dtindex.append(datetime.strptime(str(obs_dt[kk])[:19],'%Y-%m-%d %H:%M:%S'))
            obstso=pd.DataFrame(obs_temp,index=obs_dtindex)
        else:
            for kk in range(len(obs_salt)):
                obs_dtindex.append(datetime.strptime(str(obs_dt[kk])[:19],'%Y-%m-%d %H:%M:%S'))
            obstso=pd.DataFrame(obs_salt,index=obs_dtindex)   
        print 'obs Dataframe is ready'
        try:        
            starttime=obs_dt[0].replace(tzinfo=None)        
        #endtime=obs_dt[-1].replace(tzinfo=None)
            if month_time<10:
               month_time=str(0)+str(month_time)            
            urlbeforeassi='http://www.smast.umassd.edu:8080/thredds/dodsC/models/fvcom/NECOFS/Archive/eMOLT/gom'+str(month_time)+'_0001.nc'            
            nb = netCDF4.Dataset(urlbeforeassi)
            nb.variables
            latb = nb.variables['lat'][:]
            lonb = nb.variables['lon'][:]
            timesb = nb.variables['time']
            jdb = netCDF4.num2date(timesb[:],timesb.units)
            varb = nb.variables[vname]
            print 'Now find the coincide before assinulate timestample'
            inode = nearlonlat(lonb,latb,loni,lati)
            print inode
            beftso=pd.DataFrame(varb[:,layer,inode],index=jdb)
                 ###http://www.smast.umassd.edu:8080/thredds/dodsC/models/fvcom/NECOFS/Archive/eMOLT_temp/gom3_200801.nc
            urlfvcom = 'http://www.smast.umassd.edu:8080/thredds/dodsC/models/fvcom/NECOFS/Archive/eMOLT_temp/gom3_2008'+str(month_time)+'.nc'
            nc = netCDF4.Dataset(urlfvcom)
            nc.variables
            var = nc.variables['temp']
            print 'Now find the coincide timestample'
            print inode
            modtso=pd.DataFrame(var[:,layer,inode],index=jdb)
            ####before assimulate#######
        
            badindex=[]
            for ii in range(len(modtso)):
                tdelta=[]
                for j in range(len(obstso)):
                    tdelta.append(abs(modtso.index[ii] - obstso.index[j]))
                if min(tdelta)>timedelta(hours=0.5):
                       print min(tdelta),ii
                       badindex.append(ii)
                       print ii
            modtso=modtso.drop(modtso.index[badindex])
            beftso=beftso.drop(beftso.index[badindex])

            rmsa=np.sqrt((sum((obstso.values-modtso.values)**2))/len(obstso))
            rmsb=np.sqrt(sum((obstso.values-beftso.values)**2)/len(obstso))
            print "rmsa"+str(rmsa),"rmsb"+str(rmsb)
            
            ax.plot(obstso.index,obstso[0].values,color='red')
            ax.plot(modtso.index,modtso[0].values,color='blue')
            ax.plot(beftso.index,beftso[0].values,color='green') 
            ax.xaxis.set_minor_locator(dates.MonthLocator(bymonth=(1),
                                                interval=1))
            ax.xaxis.set_minor_formatter(dates.DateFormatter(''))
            ax.xaxis.set_major_locator(dates.MonthLocator())
            ax.xaxis.set_major_formatter(dates.DateFormatter('\n%b'))
            print str(month_time)+"is done"
        except:
            m=m+1
            
  
    
    
    
    ax.set_ylabel('Temperature(degC)',fontsize=20)
    ax.set_title('Bottom temperature at '+str(site[k]),fontsize=20)
    ax.grid(True)
    plt.legend(['observed','after assimulation','before assimulation'],loc='upper right',# bbox_to_anchor=(1.01, 1.20),
                  ncol=10, fancybox=True, shadow=True,prop={'size':20})
    ax.tick_params(axis='both', which='major', labelsize=20)
    plt.show()
    plt.savefig(str(site[k])+'_bottTEMPERATUREassimulation.png')
       