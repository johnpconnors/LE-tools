#========================================================
# This script assists with the creation of batch files for Fragstats. 
#Specify a directory with a list of Esri header-specified files and a text document to write to. 
#========================================================

import re, os, glob

#Input variables
#directory is the folder containing 32-bit floating point files
directory="/Users/johnpconnors/testing/"
writefile="/Users/johnpconnors/testing/batch.txt"

cellsize=2.4
bg=9999

#Set up folder to loop through
listing=os.listdir(directory)
index=0
f=open(writefile, "r+")


#loops through files in the folder 
for infile in glob.glob(os.path.join(directory,'*.hdr')):
    #header = open(infile, "r")
    #header2 = header
    #loops through lines in header file to get column number
    with open (infile, 'r') as header:
        for line in header:
            print(line)
            regex1 = re.match(r'(NCOLS)\s*(\w+).*$', line)
            if regex1 is not None: 
                print regex1.group(2)
                break
        
    #loops through header file to get number of rows
    print('here')
    with open (infile, 'r') as header2:
        for lines in header2:
            print('here2')
            print(lines)
            regex2 = re.match(r'(NROWS)\s*(\w+).*$', lines)
            if regex2 is not None: 
                print regex2.group(2)
                break
        
    output=(infile, cellsize, bg, regex2.group(2), regex1.group(2), "IDF_32BIT")
    output=str(output)
    print output
    f.write('\n'+ output)

f.close()
