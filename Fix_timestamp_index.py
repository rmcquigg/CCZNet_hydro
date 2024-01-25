# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 12:50:13 2023

@author: mcquiggan
"""
import pandas as pd
import numpy as np

#***Must have a timestamp column named DATE***
#Data in comme-separated value file .csv

#Read in file and get first and last timestamps
path='C:/Users/mcquiggan/Downloads/' #File path
file='MB01_Velocity_17Nov22' #File name
dat=pd.read_csv(path+file+'.csv',skiprows=(6),na_values=np.nan) #This will skip 6 rows of metadata, but you can change that to whatever your dataset looks like
dat['DATE']=pd.to_datetime(dat['DATE'])
ts1=dat['DATE'][0]
ts2=dat['DATE'][(len(dat))-1]
dat=dat.set_index('DATE')

#Check for duplicate timestamps and drop, keeping only the first
print(dups=dat[dat.duplicated()])
dat.drop_duplicates(keep='first') #This will drop duplicate timestamp records and keep the FIRST REC ONLY

#Create an empty dataframe with continuous timestamp intervals (every 15 min, 60 min, etc)
df=pd.DataFrame()
df['DATE']=pd.date_range(ts1,ts2,freq='15T') #Change the frequency, in minutes, for your data
df=df.set_index('DATE')

#Merge dataset with the empty timestamp dataframe
datmerge=df.merge(dat,how='left',left_on=df.index,right_on=dat.index)

#***Pick one of the two options below: either flag missing data OR interpolate***

#1. If you want to fill missing data with a flag 
datmerge=datmerge.fillna(999)

#2. If you want to interpolate over missing data
datmerge=datmerge.interpolate(axis=0)

#Send as csv to the file path
datmerge.to_csv(path+file+'_REV.csv')
