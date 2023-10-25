# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 09:25:34 2021

@author: mcquiggan
"""

import pandas as pd
from datetime import date
import numpy as np
import os
import sys
sys.path.append('G:/Shared drives/CZN_HydroGroup/Data/process_scripts/')
import LTC

#Specify path and file name
path='G:/Shared drives/CZN_HydroGroup/Data/preprocess_files/'
file='FILE NAME HERE'

#Read csv in as dataframe
df=pd.read_csv(path+file,index_col='Site ID',na_values=np.nan)
df=df.iloc[2: , :]

#***SPECIFY SITE ID HERE***
siteid='MNMF2-SP-D'

wc=df[siteid+'_WC'].astype(float).interpolate(axis=0,inplace=False).round(decimals=3)
st=df[siteid+'_ST'].astype(float).interpolate(axis=0,inplace=False).round(decimals=1)
se=df[siteid+'_SE'].astype(float).interpolate(axis=0,inplace=False).round(decimals=3)

#Plot the data - change label variable to whatever column name you want to plot
label='COLUMN HEADER'
LTC.plot_smrx(df,label)

#----------------------------------------------------
#ENTER INFO INTO BLOCK AND DATA TABLES
#----------------------------------------------------
#Enter the variables below
sensor_sn='SENSOR NUMBER'
initials='INITIALS'
matrix='S'
sensor='TEROS'
datum='GS'
interval=15
n=len(df.index)-1

#*****HIGHLIGHT BELOW TO THE BOTTOM AND RUN*****
#Open existing block table as dataframe
df_block=pd.read_csv('G:/Shared drives/CZN_HydroGroup/Data/data_tables/block.csv')

block_start_time=df.index[0]
block_end_time=df.index[len(df.index)-1]
process_date=date.today().strftime('%m/%d/%Y')
quality='P'

#Water content
dat_type='WC'
unit='M3'
blockno=int(df_block['blockno'].max()+1)
ind1=int(df_block['index2'].max()+1)
ind2=int(ind1+n)
df_block=df_block.append({'blockno':blockno,
                          'site_id':siteid,
                          'start_time':block_start_time,
                          'index1':ind1,
                          'end_time':block_end_time,
                          'index2':ind2,
                          'matrix':matrix,
                          'data_type':dat_type,
                          'sensor':sensor,
                          'sensor_sn':sensor_sn,
                          'unit':unit,
                          'interval':interval,
                          'mp_datum':datum,
                          'accuracy':np.nan,
                          'drift':np.nan,
                          'process_initials':initials,
                          'process_date':process_date,
                          'quality':quality},ignore_index=True)

df_data=pd.DataFrame()
df_data['index']=list(range(ind1,ind2+1,1))
df_data['blockno']=blockno
df_data['amount']=wc.to_list()

#Soil temp
dat_type='ST'
unit='DC'
blockno=int(df_block['blockno'].max()+1)
ind1=int(df_block['index2'].max()+1)
ind2=int(ind1+n)
df_block=df_block.append({'blockno':blockno,
                          'site_id':siteid,
                          'start_time':block_start_time,
                          'index1':ind1,
                          'end_time':block_end_time,
                          'index2':ind2,
                          'matrix':matrix,
                          'data_type':dat_type,
                          'sensor':sensor,
                          'sensor_sn':sensor_sn,
                          'unit':unit,
                          'interval':interval,
                          'mp_datum':datum,
                          'accuracy':np.nan,
                          'drift':np.nan,
                          'process_initials':initials,
                          'process_date':process_date,
                          'quality':quality},ignore_index=True)

df_app=pd.DataFrame()
df_app['index']=list(range(ind1,ind2+1,1))
df_app['blockno']=blockno
df_app['amount']=st.to_list()
frames=[df_data,df_app]
df_data=pd.concat(frames)

#Saturation ext
dat_type='SE'
unit='MS'
blockno=int(df_block['blockno'].max()+1)
ind1=int(df_block['index2'].max()+1)
ind2=int(ind1+n)
df_block=df_block.append({'blockno':blockno,
                          'site_id':siteid,
                          'start_time':block_start_time,
                          'index1':ind1,
                          'end_time':block_end_time,
                          'index2':ind2,
                          'matrix':matrix,
                          'data_type':dat_type,
                          'sensor':sensor,
                          'sensor_sn':sensor_sn,
                          'unit':unit,
                          'interval':interval,
                          'mp_datum':datum,
                          'accuracy':np.nan,
                          'drift':np.nan,
                          'process_initials':initials,
                          'process_date':process_date,
                          'quality':quality},ignore_index=True)

df_app=pd.DataFrame()
df_app['index']=list(range(ind1,ind2+1,1))
df_app['blockno']=blockno
df_app['amount']=se.to_list()
frames=[df_data,df_app]
df_data=pd.concat(frames)

#Write new block and data info to .csv files for import
df_block.to_csv('G:/Shared drives/CZN_HydroGroup/Data/data_tables/block.csv',index=False)
df_data.to_csv('G:/Shared drives/CZN_HydroGroup/Data/data_tables/data_sm.csv',mode='a',header=False,index=False)


#DON'T RUN THIS UNTIL DONE WITH THE ENTIRE .CSV DOCUMENT (I.E. IF YOU HAVE S AND D SENSORS)
#Move processed file to postprocess_files folder
postpath='G:/Shared drives/CZN_HydroGroup/Data/postprocess_files/'
os.replace(path+file,postpath+file)


