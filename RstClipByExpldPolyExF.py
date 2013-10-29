#=====================================================


import osgeo, os, sys, gdal
from osgeo import ogr

def run(path, shp, img):
	setup(path)
	explosion(shp, img)

def setup(datapath):
	#datapath = input('Type the path to the folder with inputs: ')
	#inputshp = input('Define the mask image to explode features. Must be a shapefile. Type the name of the vector file with extension: ')
	#rasterimg = input('Define the raster image to be clipped. Type the name of the raster file with extension: ')
	#set up GDAL to work
	sys.path.append("/Library/Frameworks/GDAL.framework/Programs")
	os.system("gdalinfo --version")
	#change to appropriate directory 
	os.chdir(datapath)

def explosion(inputshp, rasterimg):
	#print inputshp
	shpshort=os.path.splitext(inputshp)[-2]
	#open blank file
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

		outraster = str(cnt)
		clippedrst = shpshort+'_'+str(cnt)+'_clip.tif'
		print type(extent)
		print type (extent[1])
		print extent[1]
		#clip the raster with the shapefile
		print (os.system('echo $PYTHONPATH'))
		#clips the raster using the extent of the subset shapefile
		os.system('gdal_translate -of Ehdr -projwin %s %s %s %s %s %s' % (bbox[0], bbox[3], bbox[1], bbox[2], rasterimg, outraster))
		#uses the newly created shapefile to mask the bounded raster
		os.system('gdalwarp -of GTIFF -co "TFW=YES" -cutline %s %s %s' % (outfile, outraster, clippedrst))
		#delete the extraneous files
		cntstr = str(cnt)
		try:
			os.remove(outfile)
			os.remove(cntstr+'.clr')
			os.remove(cntstr+'.dbf')
			os.remove(cntstr+'.hdr')
			os.remove(cntstr+'.prj')
			os.remove(cntstr+'.shx')
			os.remove(cntstr+'.aux.xml')			
			os.remove(outraster)
		except OSError: 
			pass
		cnt=cnt+1

if __name__ == '__main__':
	#1 is datapath, 2 is inputshp, 3 is raster image
    run(sys.argv[1], sys.argv[2], sys.argv[3])
