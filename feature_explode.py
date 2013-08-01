import ogr, os, sys

path = '/Users/johnpconnors/testing/'
inputshp = 'NRCS_HUC8_2011.shp'

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
while cnt < 10:
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

	feature.Destroy()
	feature=inLayer.GetNextFeature()

	cnt=cnt+1
