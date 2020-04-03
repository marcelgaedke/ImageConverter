#Image Converter
#Converts *.cr2 Image Files to *.jpg

import argparse
import numpy as np
import os
import re

from PIL import Image
from rawkit.raw import Raw




def getfiles_with_subdirectories(dir):
    '''Returns list of CR2 files in dir including subdirectories'''
    files = []
    directories = []
    for root,dirs,file_names in os.walk(dir):
        if file_names:
            for file_name in file_names:
                pattern = r".*\.[cC][rR]2"
                if re.search(pattern,file_name):
                    files.append(root+'/'+file_name)
    return files


def get_files_no_subdirectories(dir):
    '''Returns list of CR2 files in dir NOT including subdirectories'''
    files = []
    for listing in os.listdir(dir):
        pattern = r".*\.[cC][rR]2"
        if re.search(pattern,listing):
            files.append(dir+'/'+listing)
    return files


def convert_file(path,destination):
    '''Converts path.cr2 File and returns JPEG'''
    raw_image = Raw(path)
    buffered_image = np.array(raw_image.to_buffer())
    image = Image.frombytes('RGB', (raw_image.metadata.width, raw_image.metadata.height), buffered_image)
    image.save(destination, format='jpeg')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--destination',help='destination folder for converted images. Default currentDirectory/ConvertedImages')
    parser.add_argument('-s','--source',help='source folder of CR2 Files. Default = current directory')
    parser.add_argument('-i','--includesubdirs',help='Flag: include subdirectories', action="store_true")
    args = parser.parse_args()

    destination = args.destination if args.destination else (os.getcwd()+'/ConvertedImages/')
    source = args.source if args.source else os.getcwd()

    print("{0: <15s}: {1}".format("source",source))
    print("{0: <15s}: {1}".format("includesubdirs", args.includesubdirs))
    print("{0: <15s}: {1}".format("destination",destination))

    files = getfiles_with_subdirectories(source) if args.includesubdirs else get_files_no_subdirectories(source)
    counter = 1000
    for file in files:
        #print("Converting "+file)
        file_name = 'IMG'+str(counter)+'.jpg'
        try:
            convert_file(file,destination+file_name)
        except Exception as e:
            print("Error while converting -",e)

        print("Creating "+ file_name)
        counter += 1
