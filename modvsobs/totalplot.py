# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 15:12:47 2013

@author: jmanning
"""

import pandas as pd
from pandas.core.common import save
import matplotlib.pyplot as plt
site=['AB01','BA01','BA02','BA03','BF01','BI01','BM01','BN01','CP01','DC01','DJ01']
df1=pd.read_csv(site[0]+'_wtmp_mc_mod_mc_obs.csv',index_col=0)
dfmean1=df1['mean']
pdmean1=pd.DataFrame(dfmean1,index=df1.index)
pdmean1.columns=[site[0]]
for k in range(len(site)):
    if k!=0:
        df=pd.read_csv(site[k]+'_wtmp_mc_mod_mc_obs.csv',index_col=0)
        dfmean=df['mean']
        pdmean=pd.DataFrame(dfmean,index=df.index)
        pdmean.columns=[site[k]]
        pdmean1=pdmean1.join(pdmean)
print pdmean1
pdmean1.to_csv('totalplot.csv',index=True)
htmlmean=pdmean1.to_html(header=True,index=True)
save(htmlmean,'totalplot.html')
fig=plt.figure()
ax=fig.add_subplot(111)
ax.plot(pdmean1.index,pdmean1.values)
ax.set_ylabel('Temperature difference (degC)')
ax.set_xlabel('Month')
for i in range(len(ax.lines)):#plot in different ways
    if i<int(len(ax.lines)/2):
        ax.lines[i].set_linestyle('--')
        ax.lines[i].set_linewidth(4)
    elif i>=int(len(ax.lines)/2):
        ax.lines[i].set_linestyle('-')
        ax.lines[i].set_linewidth(4)

patches,labels=ax.get_legend_handles_labels()
#ax.legend(set(tso['Year'].values),loc='center left', bbox_to_anchor=(.05, 0.5))
ax.legend(site,loc='best')
plt.grid()
plt.title('Model vs Observed Mthly Means at 11 eMOLT sites')
#pdmean1.plot(figsize=(16,4),x_compat=True,grid=True,linewidth=3,title='Meandiff')
plt.show()
plt.savefig('emoltvsnecofs_diff.png')