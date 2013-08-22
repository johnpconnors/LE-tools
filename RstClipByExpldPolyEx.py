#=====================================================


import osgeo, os, sys, gdal
from osgeo import ogr

path = '/Users/johnpconnors/testing/'
inputshp = 'NRCS_HUC8_2011.shp'
rasterimg='AZ_CDL_2010.tif'
sys.path.append("/Library/Frameworks/GDAL.framework/Programs")
os.system("gdalinfo --version")
#change to appropriate directory
os.chdir(path)

#Gets Spatial Ref
shape = ogr.Open(inputshp)
spatial_ref = shape.GetLayer().GetSpatialRef().Clone()

#Get the Drivers to open Shapefile
driver=ogr.GetDriverByName('ESRI Shapefile')

#Read the specified shapefile
datasource=driver.Open(inputshp, 0)
inLayer=datasource.GetLayer()

#Open the first feature in the shapefile
feature=inLayer.GetNextFeature()

#loop through to create new shapefile for each 
cnt = 0
while feature:
	print(cnt)
	outfile=str(cnt)+'.shp'

	#Create a new data source and layer
	if os.path.exists (outfile):
		driver.DeleteDataSource(outfile)
	outDS=driver.CreateDataSource(outfile)
	if outDS is None:
		print 'Could Not Create File'		
		sys.exit(1)
	outLayer  = outDS.CreateLayer('Poly', spatial_ref, ogr.wkbPolygon)

	#Use the input FieldDefn to add a field to the output
	fieldDefn = inLayer.GetFeature(0).GetFieldDefnRef('fid')
	outLayer.CreateField(fieldDefn)

	#get the FeatureDefn for the output layer
	featureDefn=outLayer.GetLayerDefn()


	#create new feature
	outFeature = ogr.Feature(featureDefn)
	outFeature.SetGeometry(feature.GetGeometryRef())
	outFeature.SetField('fid', feature.GetField('fid'))

	#add the feature to the output layer
	outLayer.CreateFeature(outFeature)
	
	outFeature.Destroy()
	outDS.Destroy()

	driver2 = ogr.GetDriverByName('ESRI Shapefile')
	ds2 = driver2.Open(outfile)
	if ds2 is None:
		print 'could not open'
	lyr=ds2.GetLayerByName(str(cnt))
	if lyr is None:
		print 'nonetype'
	num=lyr.GetFeatureCount()
	extent=lyr.GetExtent()
	bbox = [str(extent[0]), str(extent[1]), str(extent [2]), str(extent[3])]
	print(bbox)
	feature.Destroy()
	feature=inLayer.GetNextFeature()

	outraster = str(cnt)+'.tif'
	clippedrst = str(cnt)+'_clip.tif'
	print type(extent)
	print type (extent[1])
	print extent[1]
	#clip the raster with the shapefile
	print (os.system('echo $PYTHONPATH'))
	os.system('gdal_translate -of GTiff -projwin %s %s %s %s -co "TFW=YES" %s %s' % (bbox[0], bbox[3], bbox[1], bbox[2], rasterimg, outraster))
	os.system('gdalwarp -of GTIFF -cutline %s %s %s' % (outfile, outraster, clippedrst))
	cnt=cnt+1
