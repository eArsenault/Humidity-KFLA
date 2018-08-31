import arcpy 
import pandas as pd

# initial variables - we use a cursor to read the data from a .gdb feature class
file = "J:/Projects/GIS/climate2018/intermediates.gdb/humidex_grid"
newfile = "J:/Projects/GIS/climate2018/intermediates.gdb/humidex_grid_project"
fields = ["PointID","id"]

WKID = 102001 #EPSG code for new projection - Canada Albers Equal Area Conic
spatialReference = arcpy.SpatialReference(WKID)
transformation = "WGS_1984_(ITRF00)_To_NAD_1983"
arcpy.Project_management(file, newfile, spatialReference,transformation)# equal area projection to avoid skewed values of area

CCDPIndex = set([row[0] for row in arcpy.da.SearchCursor(newfile, fields)])# we only want unique values for these, hence set (will become indices)
OCCPIndex = set([row[1] for row in arcpy.da.SearchCursor(newfile, fields)])
joinIndex = [row for row in arcpy.da.SearchCursor(newfile, fields)]
shapeArea = [row[0] for row in arcpy.da.SearchCursor(newfile, "SHAPE@AREA")]
OCCPIndexFull = [i + 1 for i in range(8964)]

##OCCP_dates = pd.date_range("19810101",periods=119*365 + 100) #100 accounts for leap days
##OCCP_dates = OCCP_dates[(OCCP_dates.year <= 2099) & ~((OCCP_dates.month == 2) & (OCCP_dates.day == 29))]
##
##CCDP1 = pd.date_range("19851201","20051130")
##CCDP2 = pd.date_range("20191201","20991130")
##CCDP_dates = CCDP1.append(CCDP2)
##
##dates = CCDP_dates.intersection(OCCP_dates)

arcpy.Delete_management(newfile)

