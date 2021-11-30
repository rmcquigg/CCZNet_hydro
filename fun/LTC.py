# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 13:09:21 2021

@author: mcquiggan
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
import os
import sys
sys.path.append('G:/Shared drives/CZN_HydroGroup/Data/process_scripts/')
import find_first_row
from find_sn import find_sn

def reformat(path,file):
    #Bring LTC file data in as df
    ffr=find_first_row.first_row(path+file)
    df=pd.read_csv(path+file,skiprows=ffr)
    
    #Combine date and time columns and round to nearest 15-min interval
    df['DateTime']=pd.to_datetime(df['Date']+" "+df['Time'])
    df['DateTime']=pd.to_datetime(df['DateTime']).dt.round('15min').dt.strftime('%m/%d/%Y %H:%M:%S')
    df=df.set_index('DateTime')
    return df
        
def plot(df):
    #Interactive plot window to check for any data outliers/noisy points
    df.plot(y='LEVEL',style='.',rot=45)
    plt.grid()
    plt.tight_layout()
    plt.show()

#----------------------------------------------------
#DATA CLEANING
#----------------------------------------------------
def r_first_rows(df,start_del):
    ##To remove a specified number of records at the start of the file
    #Enter the number of rows below as start_del
    df=df.iloc[start_del:]
    df.head()
    return df

def r_last_rows(df,end_del):
    #To remove a specified number of records at the end of the file
    #Enter the number of rows below as end_del
    df=df.iloc[:-end_del]
    df.tail()
    return df

def interpolate_one(df,dt,param):
    #To interpolate values between two records (i.e. smooth over a point)
    #Change the date and time to that of whatever point you want to smooth over
    #Can do this multiple times for multiple points and the interpolate function will do all at once
    point=(df.index.get_loc(dt))
    df[param][point]=np.nan
    df[param]=df[param].interpolate(axis=0)
    print(df[param][point])

def interpolate_btw(df,dt_1,dt_2,param):
    #To interpolate values over multiple records (i.e. interpolate over multiple consecutive records)
    #Change the date and time for the first (first_pt) and last (last_pt) of the interval you want to change
    first_pt=df.index.get_loc(dt_1)
    last_pt=df.index.get_loc(dt_2)+1
    df[param][first_pt:last_pt]=np.nan
    df[param]=df[param].interpolate(axis=0)
    #df.head()
    return df

#----------------------------------------------------
#CORRECT FOR WATER LEVEL SENSOR DRIFT
#----------------------------------------------------
def drift_cor(df,end_lev):
    global n
    global acc
    n=len(df['LEVEL'])-1
    R2=df['LEVEL'][n]
    acc=round((end_lev-R2),3)
    K=acc/(n-1)
    #return n

    #Correct LEVEL column to match field-measured water levels
    new_lc=[]
    for index,val in enumerate(df['LEVEL'],start=1):
        corr=K*(index-1)
        new=round(val+corr,3)
        new_lc.append(new)
    
    df['LEVEL_cor']=new_lc

#----------------------------------------------------
#CORRECT FOR SC SENSOR DRIFT
#----------------------------------------------------
def sc_cor(df,start_std,start_cal,end_std,end_cal):
    n=len(df['CONDUCTIVITY'])-1
    K1=start_std/start_cal
    K2=end_std/end_cal
    global drift
    drift=round(K1-K2,4)
    dK=(K2-K1)/(n-1)
    
    #Correct CONDUCTIVITY column to LTC sensor drift (from calibration check values)
    new_sc=[]
    for index,val in enumerate(df['CONDUCTIVITY'],start=1):
        corr=1+(dK/K1)*(index-1)
        new=round(val*corr,1)
        new_sc.append(new)
        
    df['SC_cor']=new_sc

#----------------------------------------------------
#ENTER INFO INTO BLOCK AND DATA TABLES
#----------------------------------------------------
#Enter the variables below


#*****HIGHLIGHT BELOW TO THE BOTTOM AND RUN*****
#Open existing block table as dataframe
def update_tabs(df,path,file,matrix,sensor,datum,interval,initials):
    df_block=pd.read_csv('G:/Shared drives/CZN_HydroGroup/Data/data_tables/block.csv')
    
    block_start_time=df.index[0]
    block_end_time=df.index[len(df.index)-1]
    site_id=file.split('_')[0]
    n=len(df['LEVEL'])-1
    process_date=date.today().strftime('%m/%d/%Y')
    quality='P'
    sensor_sn=find_sn(path,file)
    
    blockno=df_block['blockno'].max()+1
    ind1=int(df_block['index2'].max()+1)
    ind2=int(ind1+n)
    dat_type='L'
    unit='M'
    df_block=df_block.append({'blockno':blockno,
                              'site_id':site_id,
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
                              'accuracy':acc,
                              'drift':np.nan,
                              'process_initials':initials,
                              'process_date':process_date,
                              'quality':quality},ignore_index=True)
    
    df_data=pd.DataFrame()
    df_data['index']=list(range(ind1,ind2+1,1))
    df_data['blockno']=blockno
    df_data['amount']=df['LEVEL_cor'].to_list()
    
    #SC
    dat_type='C'
    unit='US'
    blockno=df_block['blockno'].max()+1
    ind1=int(df_block['index2'].max()+1)
    ind2=int(ind1+n)
    df_block=df_block.append({'blockno':blockno,
                              'site_id':site_id,
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
                              'drift':drift,
                              'process_initials':initials,
                              'process_date':process_date,
                              'quality':quality},ignore_index=True)
    #df_data=pd.DataFrame()
    df_app=pd.DataFrame()
    df_app['index']=list(range(ind1,ind2+1,1))
    df_app['blockno']=blockno
    df_app['amount']=df['SC_cor'].to_list()
    frames=[df_data,df_app]
    df_data=pd.concat(frames)
    
    
    #Temp    
    dat_type='T'
    unit='DC' 
    blockno=df_block['blockno'].max()+1
    ind1=int(df_block['index2'].max()+1)
    ind2=int(ind1+n)
    df_block=df_block.append({'blockno':blockno,
                              'site_id':site_id,
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
    #df_data=pd.DataFrame()
    df_app=pd.DataFrame()
    df_app['index']=list(range(ind1,ind2+1,1))
    df_app['blockno']=blockno
    df_app['amount']=df['TEMPERATURE'].to_list()
    frames=[df_data,df_app]
    df_data=pd.concat(frames)
    
    df_block.to_csv('G:/Shared drives/CZN_HydroGroup/Data/data_tables/block.csv',index=False)
    df_data=df_data.to_csv('G:/Shared drives/CZN_HydroGroup/Data/data_tables/data.csv',mode='a',header=False,index=False)
    #Move processed file to postprocess_files folder    
    df.to_csv(path+file)
    postpath='G:/Shared drives/CZN_HydroGroup/Data/postprocess_files/'
    os.replace(path+file,postpath+file)
       


