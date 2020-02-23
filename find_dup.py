#!/usr/bin/env python2.7

import sys
import os
from os.path import isfile, join, isdir, getsize
import hashlib
import time
import datetime
import argparse
import shutil
import logging
from enum import Enum
from prettytable import PrettyTable
import re

#*********************************************
# Ideas:
#	Logger or file option for output
#       gmail.py type of feature where you can read file and apply action.
#*********************************************

hash_dict = {}
only_ext = ''
DUP_FILE_SIZE_BYTES = 0
excluded_exts = []
FORMAT = '%(module)s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=20, stream=sys.stdout)
logger = logging.getLogger('find_dup')
FILE_OPTIONS = Enum('File Options', 'delete, dry_run, move')
TYPES = {
    'pictures': ['png', 'jpeg', 'dng', 'nef', 'jpg'],
    'movies': ['mov, mp4, wmv', 'avi', 'mpg']
}


def get_file_ext(file):
    return file.split('.')[-1].lower()


def is_ds_store(file):
    return not get_file_ext(file) == 'ds_store'


def is_picture(file):
    return get_file_ext(file) in TYPES['pictures']


def is_movie(file):
    return get_file_ext(file) in TYPES['movies']


def is_custom_ext(file):
    return get_file_ext(file) == only_ext    


def is_excluded(file):
    return get_file_ext(file) not in excluded_exts

def is_not_hidden(file):
    return not re.match("^\.[a-zA-Z]", file)


def take_action(file_option, file, dup_dir):
    if file_option == FILE_OPTIONS.delete:
        os.remove(file)
        return 'Deleted File!'

    elif file_option == FILE_OPTIONS.move:
        if not os.path.exists(dup_dir):
            logger.info("Creating dir: %s" % dup_dir)
            os.mkdir(dup_dir)
        file_name = file.split(os.sep)[-1]
        os.rename(file, join(dup_dir, file_name))
        return 'Moved File!'

    elif file_option == FILE_OPTIONS.dry_run:
        return 'Dry Run!'

    else:
        sys.exit("Invalid option: %s", file_option)


def find_dups(location, dup_dir, filters, file_option, delete_empty_folders):
    duplicates_dict = {}
    global DUP_FILE_SIZE_BYTES
    onlyfiles = [ join(location,f) for f in os.listdir(location) if all(fil(join(location,f)) for fil in filters) ]
    counter = 0
    onlyfiles.reverse()
    
    for file in onlyfiles:
        file_hash = hashlib.md5(open(file, 'rb').read()).hexdigest()
        if file_hash not in hash_dict:
            hash_dict.update({file_hash:file})
        else:
            original_file = hash_dict[file_hash]
            if original_file not in duplicates_dict:
                duplicates_dict[original_file] = []
            duplicates_dict[original_file].append(file)
            file_size = getsize(file)
            

            DUP_FILE_SIZE_BYTES = DUP_FILE_SIZE_BYTES + file_size
            duplicate_file = file
            

    if delete_empty_folders:
        if len(os.listdir(location)) == 0:
            shutil.rmtree(location)
            logger.info("Folder deleted: %s", location)

    return duplicates_dict


def find_locations(start_location, levels):
    found_locations = []
    if levels == 1:
        found_locations.append(start_location)
    else:
        found_locations.append(start_location)
        all_folders = [ join(start_location, d) for d in os.listdir(start_location) if is_not_hidden(d) and d != '__pycache__' and isdir(join(start_location, d)) ]
        for folder in all_folders:
            found_locations += find_locations(folder, levels-1)

    return found_locations


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
    
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--dry-run', nargs='?', dest='file_option', const=FILE_OPTIONS.dry_run, help='Dry run. Display duplicates but no actions taken')
    action.add_argument('--move', nargs='?', dest='file_option', const=FILE_OPTIONS.move, help='Move duplicates file under a folder named duplicate')
    action.add_argument('--delete', nargs='?', dest='file_option', const=FILE_OPTIONS.delete, help='Delete duplicate files')


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
    filters = [is_not_hidden,isfile,is_ds_store]

    if args.type == 'pictures':
        filters.append(is_picture)

    if args.type == 'movies':
        filters.append(is_movie)

    if args.exclude_extensions:
        excluded_exts =  args.exclude_extensions

    if args.only_extension:
        only_ext = args.only_extension
        filters.append(is_custom_ext)

    if args.custom_locations:
        locations = args.custom_locations
    else:
        locations = find_locations(args.location, args.levels)


    logger.info("Start!")

    all_duplicates = {}
    
    for location in locations:
        logger.info("Checking location: %s", location)
        dup_dir = join(location, 'duplicates')
        logger.info("Duplication location: %s" % dup_dir )
        all_duplicates.update(find_dups(location, dup_dir, filters, args.file_option, args.delete_empty_folders))

    info_table = PrettyTable(['Original File', 'Duplicate File', 'Size', 'Action'])
    info_table.align = 'l'
    

    for file in all_duplicates:
        isFirst = True
        for dup_file in all_duplicates[file]:
            file_size = get_human_readable_size(getsize(dup_file))
            info = [dup_file, file_size]

            if isFirst:
                info.insert(0, file)
                isFirst = False
            else:
                info.insert(0, '')
            
            info.append(take_action(args.file_option, dup_file, dup_dir))
            info_table.add_row(info)

    print info_table.get_string()
    logger.info("Total space (potentiallly) saved: %s", get_human_readable_size(DUP_FILE_SIZE_BYTES))
    logger.info("Done!")