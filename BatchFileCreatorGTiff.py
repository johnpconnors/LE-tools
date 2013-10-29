#========================================================
# This script assists with the creation of batch files for Fragstats. 
#Specify a directory with a list of Esri header-specified files and a text document to write to. 
#========================================================

import re, os, glob, osgeo, gdal

def run():
    #Input variables
    #directory is the folder containing 32-bit floating point files
    directory="/Users/johnpconnors/UrbanExpansion/T1/Clips/"
    writefile="/Users/johnpconnors/UrbanExpansion/T1/batch.txt"

    cellsize=1
    bg=9999

    #Set up folder to loop through
    listing=os.listdir(directory)
    index=0
    f=open(writefile, "r+")
    print writefile


    #loops through files in the folder 
    for infile in glob.glob(os.path.join(directory,'*.tif')):
        print infile
        #header = open(infile, "r")
        #header2 = header

        rs=gdal.Open(infile)
        numcol=rs.RasterYSize
        numrow=rs.RasterXSize
            
        output=(infile, cellsize, bg, numcol, numrow, "IDF_GeoTIFF")
        output=str(output)
        print output
        f.write('\n'+ output)

    f.close()

if __name__ == '__main__':
    run()