#Image Converter
#Converts *.cr2 Image Files to *.jpg

import numpy as np
import os
import re

from PIL import Image
from rawkit.raw import Raw




def getfiles(dir):
    files = []
    directories = []
    for root,dirs,file_names in os.walk(dir):
        if file_names:
            for file_name in file_names:
                pattern = r".*\.[cC][rR]2"
                if re.search(pattern,file_name):
                    files.append(root+'/'+file_name)
    return files


def convert_file(path,destination):
    '''Converts path.cr2 File and returns JPEG'''
    raw_image = Raw(path)
    buffered_image = np.array(raw_image.to_buffer())
    image = Image.frombytes('RGB', (raw_image.metadata.width, raw_image.metadata.height), buffered_image)
    image.save(destination, format='jpeg')


if __name__ == '__main__':
    root = os.getcwd()
    files = getfiles(root)
    counter = 1000
    for file in files:
        print("Converting "+file)
        destination = root+'/ConvertedImages/IMG'+str(counter)+'.jpg'
        convert_file(file,destination)
        print("Creating "+destination)
        counter += 1