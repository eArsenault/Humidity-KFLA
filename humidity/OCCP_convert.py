# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 13:52:52 2018

@author: eArsenault
"""
import numpy as np
import os
import scipy.io as sio

folder_name = "J:\\Projects\\GIS\\climate2018\\rcp85_tasmin_daily\\"

for entry in os.scandir(folder_name):
    filename = entry.path
    data = sio.loadmat(filename)
    if data["outputData"].shape in {(8964,365,119)}: # 8964 grid squares * 365 days * 119 years, is norm for OCCP
       np.save(filename[:-4],data["outputData"]) 
    print("file: {}, shape: {}".format(filename,data["outputData"].shape))
    os.remove(filename) # delete file on completion