# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 14:31:00 2021

@author: mcquiggan
"""
import sys
sys.path.append('G:/Shared drives/CZN_HydroGroup/Data/process_scripts/')
import LTC

#Specify location and name of working file (.csv)
file='MBMF_20210624_20210915_LTC_Compensated.csv'
path='G:/Shared drives/CZN_HydroGroup/Data/preprocess_files/'
#Input manual measurement from when LTC was stopped/downloaded
end_lev=0.832
start_std=1413
start_cal=1413
end_std=5000
end_cal=5100
#Block table input
initials='DP'
matrix='W'
sensor='M3001'
datum='TOC'
interval=15


#Open file and format
df=LTC.reformat(path,file)
#Create interactive plot
LTC.plot(df)

df.plot()

#Data cleaning

df=LTC.r_first_rows(df,start_del=1)

df=LTC.r_last_rows(df,end_del=1)

LTC.interpolate_one(df,dt='08/26/2021 00:45:00',param='CONDUCTIVITY')

LTC.interpolate_btw(df,dt_1='04/26/2021 14:30:00',dt_2='04/26/2021 16:00:00',param='CONDUCTIVITY')



#Run the following 3 lines all at once
global n,acc,drift
LTC.drift_cor(df,end_lev)
LTC.sc_cor(df,start_std,start_cal,end_std,end_cal)

#Write to block and data tables
LTC.update_tabs(df,path,file,matrix,sensor,datum,interval,initials)


























