import arcpy
import numpy as np

def oneDDistanceMatrix(distanceArr):
    N = len(distanceArr)
    distanceArr = np.array(distanceArr) # recasts array-like as numpy array
    distanceArr = distanceArr.flatten()
    matrix1 = np.tile(distanceArr,(N,1)) #each row in matrix is original row
    matrix2 = np.transpose(matrix1) #each column in matrix is original row

    return matrix1 - matrix2 # matrix where distance from point i to point j is matrix[i,j] 

def angleMatrix(xMat,yMat):
    divideMat = np.zeros(xMat.shape) # assume each matrix has the same shape
    with np.errstate(divide="ignore", invalid="ignore"): #throws a warning otherwise, but operation proceeds regardless so can't be important
        divideMat = np.where(xMat != 0, yMat/xMat, 0) # avoid a zero denominator, is set to zero if xMat == 0 
    
    angMat = np.arctan(divideMat)
    angMat[xMat < 0] = angMat[xMat < 0] + np.pi
    angMat[(xMat > 0) & (yMat < 0)] = angMat[(xMat > 0) & (yMat < 0)] + 2*np.pi
    return angMat # matrix where angle from point i to point j is matrix[i,j]

def roundToArray(value,array):
    dimensions = array.shape
    error = abs(value*np.ones(dimensions) - array)
    return array[np.unravel_index(error.argmin(),dimensions)]

grid = "J:/Projects/GIS/climate2018/CCDP_grid.gdb/rcp85_grid"
fields = ["OID@", "SHAPE@XY"]

threshold = 46000 # maximum distance between adjacent squares while also less than all non-adjacent distances
startingNewIndex = 1703
startingOldIndex = 1091

dataList = [row for row in arcpy.da.SearchCursor(grid, fields)]
OIDList = [data[0] for data in dataList]
XArray = np.array([data[1][0] for data in dataList])
YArray = np.array([data[1][1] for data in dataList])

distanceMatX = oneDDistanceMatrix(XArray)
distanceMatY = oneDDistanceMatrix(YArray)
distanceMatZ = np.sqrt(distanceMatX**2 + distanceMatY**2)
angleMat = angleMatrix(distanceMatX,distanceMatY)

completed = set()
objective = {startingOldIndex}

while (len(completed) < len(dataList)):
    for elementIndex in objective:
        rowIndex = OIDList.index(elementIndex)
        
        
