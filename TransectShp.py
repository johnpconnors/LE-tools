#=====================================================

#=====================================================

import osgeo, os, sys, gdal, math
from osgeo import ogr

def run(datapath, startx, starty, endx, endy, dist):
	os.chdir(datapath)
	startx = float(startx)
	starty = float(starty)
	endx = float(endx)
	endy = float(endy)
	dist = float(dist)
	print starty
	move = transectpoints(startx, starty, endx, endy, dist)
	pts = [startx, starty]
	#Create a Shapefile
	spatialReference = osgeo.osr.SpatialReference()
	spatialReference.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
	driver = osgeo.ogr.GetDriverByName('ESRI Shapefile')
	shapeData = driver.CreateDataSource('transectpoints.shp')
	outfile = driver.CreateDataSource('buffers.shp')
	#Create Layer
	layer = shapeData.CreateLayer('layer1', spatialReference, osgeo.ogr.wkbPoint)
	layerDef = layer.GetLayerDefn()
	outlayer = outfile.CreateLayer('layer1', spatialReference, osgeo.ogr.wkbPolygon)
	outLayerDef = layer.GetLayerDefn()
	#loop through to calculate new points and save to shapefile
	totaldist = math.sqrt(((endx-startx)**2)+((endy-starty)**2))
	print(totaldist)
	numpts=int(round(totaldist/dist))
	for i in range(numpts):
		pts = createpts(pts, move, layer, layerDef)
	shapeData.Destroy()
	buffers(outlayer, dist)

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

def buffers(outlayer, dist):
#Loop through Features to buffer them
	ds=ogr.Open('/Users/johnpconnors/testing/transectpoints.shp', 1)
	print ds
	lc=ds.GetLayerCount()
	print lc
	lyr=ds.GetLayer()
	fc=lyr.GetFeatureCount()
	print fc
	print dist


	for i in range(fc):
		print i
		feat=lyr.GetFeature(i)
		geom=feat.GetGeometryRef()
		feat.SetGeometry(geom.Buffer(dist))
		outlayer.CreateFeature(feat)

if __name__ == '__main__':
	#1 is datapath, 2 is shapefile, 3 is transect start, 4 is transect end, 5 is buffer size, 6 is distance between points
	run(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])