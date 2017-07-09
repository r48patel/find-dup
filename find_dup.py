#!/usr/bin/env python2.7

import sys
import os
from os.path import isfile, join, isdir, getsize
import md5
import hashlib
import time
import datetime
import argparse
import shutil
import logging
from enum import Enum

#*********************************************
# Ideas:
#	Logger or file option for output
#       gmail.py type of feature where you can read file and apply action.
#*********************************************

hash_dict = {}
only_ext = ''
DUP_FILE_SIZE_BYTES = 0
excluded_exts = []
locations = []
FORMAT = '%(module)s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=20)
logger = logging.getLogger('find_dup')
FILE_OPTIONS = Enum('File Options', 'delete, dry_run, move')
TYPES = {
    'pictures': ['png', 'jpeg', 'dng', 'nef', 'jpg'],
    'movies': ['mov, mp4, wmv', 'avi', 'mpg']
}


def get_file_ext(file):
    return file.split('.')[-1].lower()

def is_picture(file):
    return get_file_ext(file) in TYPES['pictures']

def is_movie(file):
    return get_file_ext(file) in TYPES['movies']

def is_custom_ext(file):
    return get_file_ext(file) == only_ext    

def is_excluded(file):
    return get_file_ext(file) not in excluded_exts

def find_dups(location, filters, file_option, delete_empty_folders):
    global DUP_FILE_SIZE_BYTES
    onlyfiles = [ join(location,f) for f in os.listdir(location) if all(fil(join(location,f)) for fil in filters) ]
    counter = 0    
    for file in onlyfiles:
        file_name = file.split(os.sep)[-1]

        file_hash = hashlib.md5(open(file, 'rb').read()).hexdigest()
        if file_hash not in hash_dict:
            hash_dict.update({file_hash:file})
        else:
            dup_dir = join(location, 'duplicates')
            
            if not os.path.exists(dup_dir):
                os.mkdir(dup_dir)
            time_stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S.%f') 
            file_size = getsize(file)
            DUP_FILE_SIZE_BYTES = DUP_FILE_SIZE_BYTES + file_size
            logger_msg = "Duplicate item found! \n\tOriginal: \t%s \n\tDuplicate: \t%s \n\tSize: \t%s \n" % (hash_dict[file_hash],
                join(location, file_name), get_human_readable_size(file_size))

            if file_option == FILE_OPTIONS.delete:
                os.remove(file)
                logger_msg += "Deleted File!"
            elif file_option == FILE_OPTIONS.move:
                logger_msg += "\t\tMoving: %s\n" % file
                os.rename(file, join(dup_dir, file_name))
                if os.path.exists(hash_dict[file_hash]):
                    logger_msg += "\t\tMoving: %s\n" % hash_dict[file_hash]
                    os.rename(hash_dict[file_hash], join(dup_dir, hash_dict[file_hash]))
            elif file_option == FILE_OPTIONS.dry_run:
                logger_msg += "No Action Taken!"
            else:
                sys.exit("Invalid option: %s", file_option)
            
            logger.info(logger_msg)

    if delete_empty_folders:
        if len(os.listdir(location)) == 0:
            shutil.rmtree(location)
            logger.info("Folder deleted: %s", location)


def find_locations(start_location, levels):
    if levels == 1:
        locations.append(start_location)
    else:
        locations.append(start_location)
        all_folders = [ join(start_location, d) for d in os.listdir(start_location) if isdir(join(start_location, d)) ]
        for folder in all_folders:
            find_locations(folder, levels-1)

def get_human_readable_size(size,precision=2):
    suffixes=['B','KB','MB','GB','TB']
    suffixIndex = 0
    while size > 1024:
        suffixIndex += 1 #increment the index of the suffix
        size = size/1024.0 #apply the division
    return "%.*f %s"%(precision,size,suffixes[suffixIndex])

if __name__== '__main__':

    parser = argparse.ArgumentParser('Find Duplicates')
    parser.add_argument('--location',
                        help=('Where do you want to start the search '
                              '(default: "%(default)s")'),
                        default=os.getcwd())
    parser.add_argument('--type',
                        help=('What type of file to find dupicate for '
                              '(default: %(default)s)'),
                        choices=['movies', 'pictures', 'all'],
                        default='all')
    parser.add_argument('--only-extension',
                        help=('compare files with given extension'))
    parser.add_argument('--exclude-extensions',
                        help=('Which extensions should be ignored '
                              'Separate multiple extensions with space'),
                        nargs='+')
    parser.add_argument('--action',
                        help=('Action to take when duplicate is found'),
                        default="dry_run",
                        choices=['move', 'delete', 'dry_run'])
    parser.add_argument('--delete-empty-folders',
                        help=('Delete any empty folders '
                              '(default: "%(default)s")'),
                        default=False,
                        action='store_true',
                        dest='delete_empty_folders')
    parser.add_argument('--levels',
                        help=('How many nested levels to itterate from root folder. '
                              '(default: "%(default)s")'),
                        default=1,
                        type=int)
    parser.add_argument('--custom-locations',
                        help=('Run scripts on custom location '
                              'Separate multiple locations with space'),
                        nargs='+')

    args = parser.parse_args()

    filters = [isfile]

    if args.type == 'pictures':
        filters.append(is_picture)

    if args.type == 'movies':
        filters.append(is_movie)

    if args.exclude_extensions:
        excluded_exts=args.exclude_extensions
        filters.append(is_excluded)

    if args.only_extension:
        only_ext=args.only_extension
        filters.append(is_custom_ext)

    if args.custom_locations:
        locations = args.custom_locations
    else:
        find_locations(args.location, args.levels)

    if args.action == 'dry_run':
        file_option = FILE_OPTIONS.dry_run
    elif args.action == 'delete':
        file_option = FILE_OPTIONS.delete
    elif args.action == 'move':
        file_option = FILE_OPTIONS.move

    logger.info("Start!")
    
    for location in locations:
        logger.info("Checking location: %s", location)
        find_dups(location, filters, file_option, args.delete_empty_folders)

    logger.info("Total space (potentiallly) saved: %s", get_human_readable_size(DUP_FILE_SIZE_BYTES))
    logger.info("Done!")