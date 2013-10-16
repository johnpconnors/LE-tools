#=====================================================
#This script creates a transect of evenly spaced points and their buffers.
#The user specifies a start and an end point, a buffer size, and a distance between samples. 
#The points should be in decimal degrees, but the distance should be in the units of the projection of the output map. 
#The use also specifies a raster image that will be used in later analysis, from which the projection information is derived. All outputs are in the same projection.
#The outputs are two shapefiles. One contains point data with evenly spaced points on a transect. The other is the buffer polygons around these points.
#
#=====================================================

import osgeo, os, sys, gdal, math
from osgeo import ogr, osr

def run(datapath, startx, starty, endx, endy, dist, buff, inputrst):
	os.chdir(datapath)
	#Create the output shapefiles
	outpts='transectpoints_d'+str(dist)+'b'+str(buff)+'.shp'
	outbuffs='buffers_d'+str(dist)+'b'+str(buff)+'.shp'

	#Convert the string inputs to float type
	startx = float(startx)
	starty = float(starty)
	endx = float(endx)
	endy = float(endy)
	dist = float(dist)
	buff=float(buff)

	#Get the projection information from the raster file. 
	spatialReference = newmap(inputrst)

	#convert the start and end points to the appropriate projection. 
	projpts = convertpts(startx, starty, endx, endy, spatialReference)
	
	#specify new start and end points based on the projected information
	startx = float(projpts[0])
	starty = float(projpts[1])
	endx = float(projpts[2])
	endy = float(projpts[3])
	move = transectpoints(startx, starty, endx, endy, dist)

	pts = [startx, starty]

	#spatialReference.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
	driver = osgeo.ogr.GetDriverByName('ESRI Shapefile')
	shapeData = driver.CreateDataSource(outpts)
	outfile = driver.CreateDataSource(outbuffs)
	#Create Layer
	layer = shapeData.CreateLayer('layer1', spatialReference, osgeo.ogr.wkbPoint)
	layerDef = layer.GetLayerDefn()
	outlayer = outfile.CreateLayer('layer1', spatialReference, osgeo.ogr.wkbPolygon)
	outLayerDef = layer.GetLayerDefn()
	#loop through to calculate new points and save to shapefile
	totaldist = math.sqrt(((endx-startx)**2)+((endy-starty)**2))
	print(totaldist)
	numpts=int(round(totaldist/dist))
	print('making points')
	for i in range(numpts):
		pts = createpts(pts, move, layer, layerDef)
	shapeData.Destroy()
	buffers(outlayer, buff)

def transectpoints(startx, starty, endx, endy, dist):
	#Define the start and end points of the transect
	#Specify the Buffer
	#Specify the distance
	slope = (endy-starty)/(endx-startx)
	angle = math.atan(slope)
	xmove = dist * math.cos(angle)
	print xmove
	ymove = dist * math.sin(angle)
	print ymove
	move = [xmove, ymove]
	return move

def createpts(pts, move, layer, layerDef):
	print 'go'
	xpt = pts[0]
	ypt = pts[1]
	xpt = xpt + move[0]
	ypt = ypt + move[1]
	pts = [xpt, ypt]
	print pts
	#Create Feature
	feat = ogr.Feature(layerDef)
	#Create a New Feature for the Shapefile
	point = ogr.Geometry(ogr.wkbPoint)
	point.SetPoint(0, xpt, ypt)
	feat.SetGeometry(point)
	layer.CreateFeature(feat)
	print pts
	return pts

def buffers(outlayer, buff):
#Loop through Features to buffer them
	ds=ogr.Open('/Users/johnpconnors/testing/transectpoints.shp', 1)
	print ds
	lc=ds.GetLayerCount()
	print lc
	lyr=ds.GetLayer()
	fc=lyr.GetFeatureCount()
	print fc

	for i in range(fc):
		print i
		feat=lyr.GetFeature(i)
		geom=feat.GetGeometryRef()
		feat.SetGeometry(geom.Buffer(buff))
		outlayer.CreateFeature(feat)

def newmap(inputrst):
#Creates a blank map with the same dimensions and projeciton as the input raster to be clipped
	rs=gdal.Open(inputrst)
	#gets projection information
	rsProj=rs.GetProjectionRef()
	spatialReference = osgeo.osr.SpatialReference(rsProj)
	#spatialReference.ImportFromProj4(rsProj)
	
	#gets information on coordinates of corners
	info=rs.GetGeoTransform()
	#top left coordinates
	ulx=info[0]
	uly=info[3]
	#lower right coordinates. the RasterX/YSize class gets number of rows/columns. Info[1] and info[5] get the cell resolution with appropriate +/- sign to calculate other corners. 
	lrx=ulx+info[1]*rs.RasterXSize
	lry=ulx+info[5]*rs.RasterYSize

	return spatialReference

def convertpts(startx, starty, endx, endy, spatialref):
	#define the output image as , and define the inpu
	srs_in = osr.SpatialReference()
	print spatialref
	srs_out = spatialref
	srs_in.ImportFromEPSG(4326)
	ct=osr.CoordinateTransformation(srs_in, srs_out)
	#convert the lat/long points to the image reference
	(x1, y1, height)=ct.TransformPoint(startx, starty)
	(x2, y2, height)=ct.TransformPoint(endx, endy)
	return x1, y1, x2, y2


if __name__ == '__main__':
	#1 is datapath, 2 is shapefile, 3 is transect start, 4 is transect end, 5 is buffer size, 6 is distance between points
	run(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])