# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 09:07:49 2018

@author: eArsenault
"""
import numpy as np
import os
import re
import scipy.io as sio
import scipy.stats.mstats as statm

folder_name = "J:\\Projects\\GIS\\climate2018\\rcp85_tasmin_daily\\"
quantile_array = np.load(folder_name + "quantile.npy", mmap_mode="r+")

for entry in os.scandir(folder_name):
    filename = entry.path
    data = sio.loadmat(filename)
    if data["outputData"].shape in {(8964,365,119)}:
       np.save(filename[:-4],data["outputData"]) 
    print("file: {}, shape: {}".format(filename,data["outputData"].shape))
    del data

#data = [] # initialize some handy variables
#index = 0
#for entry in os.scandir(folder_name):
#    match = re.search("\.npy$",entry.name) 
#    if match and not entry.name == "quantile.npy": # we don't want to include our output .npy file in this
#        data.append(np.load(entry.path, mmap_mode="r")) 
#        if not data[index].shape in {(8964,365,119)}: #data should all share the same shape, we ensure that weird indices are removed
#            data.pop() 
#        else:
#            index += 1 
#        
#length = len(data)
#dimI,dimJ,dimK = data[0].shape #data now share the same shape so this is valid
#
###NEEDS OPTIMIZATION
#for k in range(dimK):
#    for j in range(dimJ):
#        sub_data = np.empty((length,dimI), dtype="int16")
#        
#        for arr in range(length):
#            sub_data[arr,:] = data[arr][:,j,k]
#    
#        quantile = statm.mquantiles(sub_data, prob=[0.5], alphap=1/3, betap=1/3, axis=0) # for these values of alpha,beta, 50th percentile is median  
#        quantile = np.array(quantile, dtype="int16") # we want an int array, not a float masked array
#        quantile_array[:,j,k] = quantile
#        