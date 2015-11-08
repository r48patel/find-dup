import sys
import os
from os.path import isfile, join
import md5
import hashlib
import argparse

#*********************************************
# Current Issues:
#   Print messages are ugly
#   
# Ideas:
#   Add more types
#*********************************************

hash_dict = {}

def is_picture(file):
    picture_ext = ["png", "jpeg", "dng", "NEF", "jpg", "JPG"]
    file_ext = file.split('.')[-1]

    return file_ext in picture_ext

if __name__== '__main__':
    parser = argparse.ArgumentParser('Find Duplicates')
    parser.add_argument('--location',
                        help=('Where do you want to start the search '
                              '(default: "%(default)s")'),
                         default=os.getcwd())
    parser.add_argument('--type',
                         help=('What type of file to find dupicate for '
                               '(default: %(default)s)'),
                         choices=['pictures', 'all'],
                         default='all')
    args = parser.parse_args()

    filters = [isfile]

    if args.type == 'pictures':
        filters.append(is_picture)

    onlyfiles = [ join(args.location,f) for f in os.listdir(args.location) if all(fil(join(args.location,f)) for fil in filters) ]
    
    for file in onlyfiles:
        file_hash = hashlib.md5(open(file, 'rb').read()).hexdigest()
        # print f
        # print file_hash
        if file_hash not in hash_dict:
            hash_dict.update({file_hash:file})
            print file + ": NEW!"
        else:
            print file + ": FOUND IT!"
            print hash_dict[file_hash]
            rename_file = hash_dict[file_hash] + "_" + file.split(os.sep)[-1]
            print "rename it: " + rename_file
            os.rename(file, rename_file)