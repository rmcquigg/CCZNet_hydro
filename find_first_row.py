# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 09:12:34 2021

@author: mcquiggan
"""
import csv
def first_row(filename):
    with open(filename,encoding='gbk') as f:
        csv.reader(f)
        substring='Date'
        for i, row in enumerate(f):
            if substring in row:
                return i
                #print(i)

