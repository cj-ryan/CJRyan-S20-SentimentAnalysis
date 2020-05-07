# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 11:48:41 2020

@author: CJ
"""

# credit to Ekapope Viriyakovithya for FreeCodeCamp

import os
import glob
import pandas as pd
os.chdir("C:\\Users\\CJ\\Documents\\CSC499\\499PROJECT\\Data\\Raw_CSV")

extension = 'csv'
all_filenames = [i for i in glob.glob('coronavirus_*.{}'.format(extension))]

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')