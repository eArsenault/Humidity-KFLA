import numpy as np
import matplotlib.pyplot as pl

def stretch(array,N=365): # takes a 1D array and stretches it to 365 entries
    length = len(array)
    positionIndex = np.linspace(0,length - 1,N)
    afloor = np.floor(positionIndex).astype("uint16")
    aCeil = np.ceil(positionIndex).astype("uint16")
    weight = positionIndex - afloor
    
    return (1 - weight)*array[afloor] + (weight)*array[aCeil]
    


