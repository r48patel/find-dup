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
#   Dir level to go to
#*********************************************

hash_dict = {}
ext = ''
excluded_ext = []

def is_picture(file):
    picture_ext = ["png", "jpeg", "dng", "NEF", "jpg", "JPG"]
    file_ext = file.split('.')[-1]

    return file_ext in picture_ext

def is_custom_ext(file):
    file_ext = file.split('.')[-1]

    return file_ext == ext    

def is_excluded(file):
    file_ext = file.split('.')[-1]

    return file_ext not in excluded_ext

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
    parser.add_argument('--extension',
                         help=('compare files with given extension'))
    parser.add_argument('--exclude-extensions',
                         help=('Which extensions should be ignored '
                               'Separate multiple extensions with space'),
                         nargs='+')
    args = parser.parse_args()

    filters = [isfile]

    if args.type == 'pictures':
        filters.append(is_picture)

    if args.exclude_extensions:
        excluded_ext=args.exclude_extensions
        filters.append(is_excluded)

    if args.extension:
        ext=args.extension
        filters.append(is_custom_ext)

    onlyfiles = [ join(args.location,f) for f in os.listdir(args.location) if all(fil(join(args.location,f)) for fil in filters) ]
    
    for file in onlyfiles:
        file_hash = hashlib.md5(open(file, 'rb').read()).hexdigest()
        if file_hash not in hash_dict:
            hash_dict.update({file_hash:file})
            print file + ": NEW!"
        else:
            print file + ": FOUND IT!"
            print hash_dict[file_hash]
            file_renamed = hash_dict[file_hash] + "_" + file.split(os.sep)[-1]
            print "rename it: " + file_renamed
            os.rename(file, file_renamed)