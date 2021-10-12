# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 12:23:29 2021

@author: mcquiggan
"""

import csv
def find_sn(path,file):
    with open(path+file) as f:
        csv.reader(f)
        for row in f:
            return next(f)[0:7]

