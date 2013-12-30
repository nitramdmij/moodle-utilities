#!/usr/local/bin/python

# simple script for extracting course files from a Moodle backup file (.mbz)
# Usage:     python mbz_extract.py -i <path to .mbz file>
# Input:     a Moodle 2.x .mbz file
# Returns:   a sub-directory named according to the Moodle course name with
#            the unhashed/extracted course files

import os, sys
import zipfile
import shutil
import optparse
import xml.etree.ElementTree as etree

# search an xml file with a predictable structure
# for the <fullname> node and determine the course name
def getcoursename(xmlfile):
    xml = etree.parse(xmlfile)
    root = xml.getroot()
    return root.find('fullname').text

# search an xml file with a predictable structure
# for the <contenthash> and <filename> nodes and use that
# data to locate the course files and save them in a
# usable format
def getfiles(xmlfile,coursefilesdir):
    xml = etree.parse(xmlfile)
    root = xml.getroot()
    
    makedir(coursefilesdir)
    
    # search through all the <file> nodes
    for file in root.findall('file'):
        hashedfile = file.find('contenthash').text
        filename = file.find('filename').text
        
        # if there is an actual file name, copy the hashed file
        # and rename it using the actual name to a new folder
        if filename != '.':
            shutil.copyfile('temp/archive/files/' + hashedfile[:2] + '/'\
                            + hashedfile,coursefilesdir + '/' + filename)

# If the provided dir path does not exist,
# create it                            
def makedir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Given a zip file with a predictable structure, unzip it to a subfolder
# Search through the xml files to get the necessary data and create
# a folder with the unhashed course files
def processzip(path):
    fileprefix = 'temp/archive/'
    
    # Unzip the archive file
    try:
        z = zipfile.ZipFile(path)
        z.extractall(fileprefix)
    except zipfile.BadZipfile as zipfileException:
        print zipfileException
    finally:
        z.close()
    
    # get the course name and make a new folder with just the course files
    coursename = getcoursename('temp/archive/course/course.xml')    
    
    return coursename

    

def main():
    tempzip = 'temp/archive.zip'
    
    # parse the options for input and output files
    parser = optparse.OptionParser("usage %prog "+\
      "-i <input>")
    parser.add_option('-i', dest='in_name', type='string',\
      help='specify mbz file')
    parser.add_option('-o', dest='out_name', type='string',\
      help='specify output zip file')
    (options, args) = parser.parse_args()
    if (options.in_name == None):
        print parser.usage
        exit(0)
    else:
        in_name = options.in_name
    
    makedir('temp')
    shutil.copyfile(in_name,tempzip)
    
    coursename = processzip(tempzip)
    
    # Search the archive for the course files and process them
    getfiles('temp/archive/files.xml',coursename)
    
    # delete all temporary/intermediate files
    shutil.rmtree('temp')
    

if __name__ == '__main__':
    main()