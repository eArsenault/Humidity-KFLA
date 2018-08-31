import arcpy
import logging
import numpy as np
import os
import pandas as pd
import requests
import time
import warnings
import zipfile

class fileObject:
    def __init__(self):
        self.zipdir = "J:/Projects/GIS/climate2018/CCDP_text/" # folder where all files will be stored
        self.zipnameshort = "intermediate.zip" # name for zip file, can be anything
        self.zipnamefull = os.path.join(zipdir,zipnameshort)
        self.datanameshort = "datafile.txt" # name for datafile inside .zip, must match actual name
        self.zipnamefull = os.path.join(zipdir,datanameshort)
        
def downloadData(timePeriod,variable,model,row):
    data = {
    "hmUserID": "6hdNkuH+1ow=", # uses my (EA) username + password
    "hmTimeperiod": timePeriod, # "RF" "2030s" "2050s" "2080s"
    "hmVariable": variable, # "Shum" "Sprs"
    "hmMeasurement": "Series",
    "hmAverage": "Daily",
    "hmModel": model, # "CanESM" "HadGEM" "GFDL" "IPSL" "MPI"
    "hmLatitude": row[0],
    "hmLongitude": row[1],
    "hmPointID": row[2],
    "rnd": 49, # it takes a random integer? value changes when I call get request on same square + params so I doubt it matters
    }
     for i in range(5):
        try:
            handler = requests.post(URL + "downloadHandler_rcp85.ashx",data=data) # gets extension from download handler
            download = requests.get(URL + handler.text) # uses handler extension to download file into the content
            return download
        except requests.ConnectionError:
            logging.warning("Connection error at {}_{}_{}".format(row[2],timePeriod,model))
            time.sleep(0.5)   
    logging.warning("Returning empty series at {}_{}_{}".format(row[2],timePeriod,model))

def unzipText(zipDir,zipName,datafile,download):
    with open(zipName, "wb") as zip_download:
                zip_download.write(download.content) # names and places as a .zip
     with zipfile.ZipFile(zipName,"r") as zip_file: # unzips datafile.txt
        names = zip_file.namelist()
        zip_file.extract(datafile,path=zipDir)
        
def processdata(files,download):
    if download:
        try:
            unzipText(files.zipdir,files.zipnamefull,files.datanameshort,download)
            valIntermediate = np.loadtxt(files.datanamefull, skiprows=1)
        except UserWarning:
            valIntermediate = np.empty(36500)
            valIntermediate.fill(np.nan)
    else:
        valIntermediate = np.empty(36500)
        valIntermediate.fill(np.nan)
    return valIntermediate

def stretch(array,N=365): # takes a 1D array and stretches it to 365 entries
    length = len(array)
    positionIndex = np.linspace(0,length - 1,N) # generate a stretched index array
    afloor = np.floor(positionIndex).astype("uint16") # arrays of indices
    aCeil = np.ceil(positionIndex).astype("uint16") # only need up to N=36500 so this is sufficient
    weight = positionIndex - afloor
    return (1 - weight)*array[afloor] + (weight)*array[aCeil]

# initialize the logger, make sure warnings are handled as errors - handy later on
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
requestsLogger = logging.getLogger("requests")
requestsLogger.setLevel(logging.WARNING)
warnings.filterwarnings("error")

# initial variables - we use a cursor to read the data from a .gdb feature class
file = "J:/Projects/GIS/climate2018/intermediates.gdb/humidex_grid"
fields = ["Lat","Lon","PointID"]
dataList = set([row for row in arcpy.da.SearchCursor(file, fields)]) # use set to get unique occurences only

timeOptions = ["RF","2030s","2050s","2080s"]
modelOptions = ["CanESM","HadGEM","GFDL","IPSL","MPI"]
variable = "Shum" # Options are "Shum", "Sprs" for humidity, pressure respectively

URL = "http://www.ontarioccdp.ca/"
files = fileObject()

CCDP1 = pd.date_range("19851201","20051130") # base period
CCDP2 = pd.date_range("20191201","20991130") # projections
CCDPdates = CCDP1.append(CCDP2)
CCDPdates = CCDPdates[~((CCDPdates.month==2)&(CCDPdates.day==29))] # trim leap days

indexField = [element[2] for element in dataList]
emptyData = np.empty((len(indexField),len(CCDPdates)),dtype = "int16")
testTable = pd.DataFrame(data=emptyData, index=indexField, columns=CCDPdates)
del indexField, emptyData

countMain = 0
countSub = 0
# iterate through coordinates via dataList, then through different parameters
for row in dataList:
logging.info("Lat: {}, Lon: {}, PointID: {}".format(*row))
ensembleTable = pd.DataFrame(index=modelOptions, columns=CCDPdates)    
for model in modelOptions:
    for timePeriod in timeOptions:
        logging.debug("Iteration #{}: {}_{}".format(countSub,timePeriod,model))       
        download = downloadData(timePeriod,variable,model,row)
        logging.debug("Type of download: {}".format(type(download)))
        valIntermediate = processdata(files,download)
        
        if timePeriod == "RF": # at start of time period we create new list, add onto it with later time periods
            valArray = valIntermediate
        else:
            valArray = np.append(valArray,valIntermediate)
            
        countSub += 1
        
    if len(valArray)== 36500: # we are using base-365 year, no leap-days. There are 100 years of data from CCDP.
        ensembleTable.loc[model] = valArray
    else:
        ensembleTable.loc[model] = np.round(stretch(valArray,36500),2)
        
meanSeries = ensembleTable.mean(axis=0,skipna=True)
meanSeries = (1000*meanSeries).astype("int16") # recast as int16 to preserve memory, must divide by 1000 when using it again
testTable.loc[row[2]] = meanSeries

if countMain == 10:
    break
else:
    countMain += 1
