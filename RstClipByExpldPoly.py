import osgeo, os, sys, gdal
from osgeo import ogr

path = '/Users/johnpconnors/testing/'
inputshp = 'NRCS_HUC8_2011.shp'
rasterimg='AZ_CDL_2010.tif'

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
	lyr=ds2.GetLayerByName("0")
	num=lyr.GetFeatureCount()
	print num
	extent=lyr.GetExtent()
	print extent
	bbox = [extent[0], extent[1], extent [2], extent[3]]
	print bbox[0]
	print bbox[1]
	print bbox[2]
	print bbox[3]
	feature.Destroy()
	feature=inLayer.GetNextFeature()


	#get bounding box for shapefile
	#print outfile
	#ds = driver.Open(outfile)
	#print cnt
	#l=str(cnt)
	#print l
	#lyr = ds.GetLayerByName(l)
	#print lyr
	#numfeat=lyr.GetFeatureCount()
	#print numfeat
	#extent=lyr.GetExtent()
	#print extent
	#for feat in lyr:
	#	env = feat.GetGeometryRef().GetEnvelope()
	#	print ('here it is', env)
	#	bbox = [env[0], env[2], env[1], env[3]]
	#print env

	outraster = str(cnt)+'.rst'
	
	#clip the raster with the shapefile
	os.system('gdal_translate -projwin %s %s %s %s -co "TFW=YES"') % (extent[0], extent[1], extent[2], extent[3])

	cnt=cnt+1
