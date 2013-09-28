#=====================================================

#=====================================================

import osgeo, os, sys, gdal, math
from osgeo import ogr

#Set the environment
def setup(datapath):
	os.chdir(datapath)

#Define the start and end points of the transect
#Specify the Buffer
#Specify the distance
def transectpoints(shpout, start, end, dist):
	slope = (endy-starty)/(endx-startx)
	
	angle = math.atan(slope)

	xmove = dist * math.cos(angle)
	ymove = dist * math.sin(angle)

	#Create a Shapefile
	driver = osgeo.ogr.GetDriverByName('ESRI Shapefile')
	shapeData = driver.CreateDataSource('transectpoints.shp')
	
	#Create Layer
	layer = shapeData.CreateLayer('layer1', spatialReference, osgeo.ogr.wkbPoint)
	layerDef = layer.GetLayerDefn()


def creatept():
	xpt = xpt + xmove
	ypt = ypt + ymove

	#Create Feature
	feat = ogr.Feature(layerDef)
	feat.SetField ("Name", Name)

	#Create a New Feature for the Shapefile
	point = ogr.Geometry(ogr.wkbPoint)
	point.SetPoint(0, xpt, ypt)

	feat.SetGeometry(pt)

def buffers(buffers):
#Loop through Features to buffer them


if __name__ == '__main__':
	#1 is datapath, 2 is shapefile, 3 is transect start, 4 is transect end, 5 is buffer size, 6 is distance between points
	run(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])