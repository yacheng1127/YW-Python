# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 09:15:34 2013

@author: jmanning
"""
import matplotlib.pyplot as plt
from getdata import getemolt_latlon,getemolt_temp
from conversions import dm2dd,f2c
from utilities import my_x_axis_format
import pandas as pd
from numpy import float64
from datetime import datetime, timedelta
from models import getFVCOM_bottom_temp_netcdf


def resamda(oritso):
        '''
        resample daily average data
        add some new columns like 'count mean,median,max,min,std,yy,mm,dd'
        '''     
        resamda=float64(oritso[0]).resample('D',how=['count','mean','median','min','max','std'])
        resamda.ix[resamda['count']<minnumperday,['mean','median','min','max','std']] = 'NaN'
        resamda['yy']=resamda.index.year
        resamda['mm']=resamda.index.month
        resamda['dd']=resamda.index.day
        output_fmt=['yy','mm','dd','count','mean','median','min','max','std']
        resamdaf=resamda.reindex(columns=output_fmt)  
        return resamdaf

def resamma(oritso):
        '''
        resample month average data
        '''
        resamma=float64(oritso[0]).resample('m',how=['count','mean','median','min','max','std'],kind='period')
        resamma.ix[resamma['count']<25*numperday,['mean','median','min','max','std']] = 'NaN'
        resamma['yy']=resamma.index.year
        resamma['mm']=resamma.index.month
        resamma['dd']=15
        output_fmt=['yy','mm','dd','count','mean','median','min','max','std']
        resammaf=resamma.reindex(columns=output_fmt)# found I needed to generate a new dataframe to print in this order
        return resammaf

def resamdc(resamda):
        '''
        resample daily climatology
        '''
        newindex=[]
        for j in range(len(resamda)):    
                newindex.append(resamda['mean'].index[j].replace(year=2000)) # puts all observations in the same year
        repd=pd.DataFrame(resamda['mean'].values,index=newindex)
        resamdc=repd[0].resample('D',how=['count','mean','median','min','max','std'])    #add columns for custom date format
        resamdc['yy']=0
        resamdc['mm']=resamdc.index.month
        resamdc['dd']=resamdc.index.day
        output_fmt=['yy','mm','dd','count','mean','median','min','max','std']
        resamdcf=resamdc.reindex(columns=output_fmt)# found I needed to generate a new dataframe to print in this order
        return resamdcf

def resammc(resamdc):
        '''
        resample month climatology
        '''
        resammc=resamdc['mean'].resample('m',how=['mean','median'],loffset=timedelta(days=-15))
        resammc['count']=0
        resammc['min']=0.
        resammc['max']=0.
        resammc['std']=0.   
        recount=resamdc['count'].resample('m',how=['mean'],loffset=timedelta(days=-15)).values
        remi=resamdc['min'].resample('m',how=['mean'],loffset=timedelta(days=-15)).values
        rema=resamdc['max'].resample('m',how=['mean'],loffset=timedelta(days=-15)).values
        restd=resamdc['std'].resample('m',how=['mean'],loffset=timedelta(days=-15)).values
        for kk in range(len(resammc)):
           resammc['count'].values[kk]=recount[kk]
           resammc['min'].values[kk]=remi[kk]
           resammc['max'].values[kk]=rema[kk]
           resammc['std'].values[kk]=restd[kk]
        resammc['yy']=0
        resammc['mm']=resammc.index.month
        resammc['dd']=0
        output_fmt=['yy','mm','dd','count','mean','median','min','max','std']
        resammcf=resammc.reindex(columns=output_fmt)# found I needed to generate a new dataframe to print in this order
        return resammcf

def diffdadc(diff,output_fmt):
        day=[]
        for i in range(len(diff)):
            day.append(str(diff.index[i].year)+'-'+str(diffda.index[i].month)+'-'+str(diffda.index[i].day))
        daydadctime=pd.DataFrame(day,index=diff.index)
        diff=diff.join(daydadctime)
        difff=diff.reindex(columns=output_fmt)
        difff.columns=['date','mean','median','min','max','std']
        return difff


site=['AG01','BA01']
minnumperday=18
numperday=24
for k in range(len(site)):
#################read-in obs data##################################
        [lati,loni,on]=getemolt_latlon(site[k]) # extracts lat/lon based on site code
        [lati,loni]=dm2dd(lati,loni) #converts decimal-minutes to decimal degrees
        [obs_dt,obs_temp]=getemolt_temp(site[k]) # extracts time series
        obs_dtindex=[]
        for kk in range(len(obs_temp)):
            obs_temp[kk]=f2c(obs_temp[kk]) # converts to Celcius
            obs_dtindex.append(datetime.strptime(str(obs_dt[kk])[:10],'%Y-%m-%d'))
        obstso=pd.DataFrame(obs_temp,index=obs_dtindex)

##################generate resample DataFrame and putput file################################################
        reobsdaf=resamda(obstso) 
        reobsdaf.to_csv(site[k]+'_wtmp_da_obs.csv',index=False,header=False,na_rep='NaN',float_format='%10.2f')   
        reobsmaf=resamma(obstso)
        reobsmaf.to_csv(site[k]+'_wtmp_ma_obs.csv',index=False,header=False,na_rep='NaN',float_format='%10.2f')  
        reobsdcf=resamdc(reobsdaf)        
        reobsdcf.to_csv(site[k]+'_wtmp_dc_obs.csv',index=False,header=False,na_rep='NaN',float_format='%10.2f')
        reobsmcf=resammc(reobsdcf)
        reobsmcf.to_csv(site[k]+'_wtmp_mc_obs.csv',index=False,header=False,na_rep='NaN',float_format='%10.2f')
###################read-in mod data#################################

        starttime=obs_dt[0]
        endtime=obs_dt[-1]
        modtso=getFVCOM_bottom_temp_netcdf(lati,loni,starttime,endtime,layer=44)
##############generate resample DataFrame and putput file#############
        remoddaf=resamda(modtso) 
        remoddaf.to_csv(site[k]+'_wtmp_da_mod.csv',index=False,header=False,na_rep='NaN',float_format='%10.2f')   
        remodmaf=resamma(modtso)
        remodmaf.to_csv(site[k]+'_wtmp_ma_mod.csv',index=False,header=False,na_rep='NaN',float_format='%10.2f')  
        remoddcf=resamdc(remoddaf)        
        remoddcf.to_csv(site[k]+'_wtmp_dc_mod.csv',index=False,header=False,na_rep='NaN',float_format='%10.2f')
        remodmcf=resammc(remoddcf)
        remodmcf.to_csv(site[k]+'_wtmp_mc_mod.csv',index=False,header=False,na_rep='NaN',float_format='%10.2f')
##############plot da compare figure##################
        fig=plt.figure(figsize=(16,10))
        ax=fig.add_subplot(211)
        ax.plot_date(obs_dt,obs_temp,fmt='-')
        plt.grid()
        ax.plot_date(modtso.index,modtso.values,fmt='-',color='red')#bottom most value equals 44
        plt.ylabel('degree c')
        plt.title('eMOLT site '+site[k]+' temp vs FVCOM ')
        plt.legend(['observed','modeled'],loc='best')
#        plt.show()
###############plot mc compare figure##################
        TimeDelta=reobsmcf.index[-1]-reobsmcf.index[0]          
        ax1 = fig.add_subplot(212)
        my_x_axis_format(ax1, TimeDelta)
        ax1.plot_date(reobsmcf.index,reobsmcf['mean'],fmt='-')
        plt.grid()
        ax1.plot_date(remodmcf.index,remodmcf['mean'],fmt='-',color='red')#bottom most value equals 44
        plt.ylabel('degree c')
        plt.title('eMOLT site '+site[k]+' temp vs FVCOM ')
#        plt.title('eMOLT site '+site[k]+' temp vs FVCOM '+'%s at node=%d (Lon=%.4f, Lat=%.4f)' % ('temp', inode+1, lon[inode], lat[inode]))
        plt.legend(['observed','modeled'],loc='best')
        plt.show()
        plt.savefig(site[k]+'da_mc_mod_obs.png')
############calculate the different#######################
        output_fmt=[0,'mean','median','min','max','std']
        diffmc=reobsmcf-remodmcf
        month=pd.DataFrame(range(1,13),index=diffmc.index)
        diffmc=diffmc.join(month)
        diffmcf=diffmc.reindex(columns=output_fmt)
        diffmcf.columns=['month','mean','median','min','max','std']
        diffmcf.to_csv(site[k]+'_wtmp_mc_mod_mc_obs.csv',index=False,header=True,na_rep='NaN',float_format='%10.2f')

        diffma=reobsmaf-remodmaf
        date=[]
        for i in range(len(diffma)):
            date.append(str(diffma.index[i].year)+'-'+str(diffma.index[i].month))
        datetimepd=pd.DataFrame(date,index=diffma.index)
        diffma=diffma.join(datetimepd)
        diffmaf=diffma.reindex(columns=output_fmt)
        diffmaf.columns=['Year-Month','mean','median','min','max','std']
        diffmaf.to_csv(site[k]+'_wtmp_ma_mod_ma_obs.csv',index=False,header=True,na_rep='NaN',float_format='%10.2f')

        diffda=reobsdaf-remoddaf
        diffdc=reobsdcf-remoddcf

        diffdaf=diffdadc(diffda,output_fmt)
        diffdaf.to_csv(site[k]+'_wtmp_da_mod_da_obs.csv',index=False,header=True,na_rep='NaN',float_format='%10.2f')
        diffdcf=diffdadc(diffdc,output_fmt)
        diffdcf.to_csv(site[k]+'_wtmp_dc_mod_dc_obs.csv',index=False,header=True,na_rep='NaN',float_format='%10.2f')
