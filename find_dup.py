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

#*********************************************
# Ideas:
#   Add more types
#   Collect how much space was(could be) saved at the end
#*********************************************

hash_dict = {}
only_ext = ''
excluded_exts = []
locations = []
FORMAT = '%(module)s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=20)
logger = logging.getLogger('find_dup')

def is_picture(file):
    picture_ext = ["png", "jpeg", "dng", "NEF", "jpg", "JPG"]
    file_ext = file.split('.')[-1]

    return file_ext in picture_ext

def is_custom_ext(file):
    file_ext = file.split('.')[-1]

    return file_ext == only_ext    

def is_excluded(file):
    file_ext = file.split('.')[-1]

    return file_ext not in excluded_exts

def find_dups(location, filters, delete_duplicates, delete_empty_folders):
    onlyfiles = [ join(location,f) for f in os.listdir(location) if all(fil(join(location,f)) for fil in filters) ]
    
    for file in onlyfiles:
        file_name = file.split(os.sep)[-1]

        file_hash = hashlib.md5(open(file, 'rb').read()).hexdigest()
        if file_hash not in hash_dict:
            hash_dict.update({file_hash:file})
        else:
            time_stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S.%f')
            file_renamed = hash_dict[file_hash] + "_" + time_stamp + "_" + file_name
            logger_msg = "Duplicate item found! \n\tOriginal: \t%s \n\tDuplicate: \t%s \n\t"
            if delete_duplicates:
                logger_msg += "Deleted File!"
                os.remove(file)
            else:
                os.rename(file, file_renamed)
                logger_msg += "Renamed: \t" + file_renamed
            
            logger.info(logger_msg, 
                hash_dict[file_hash],
                join(location, file_name))

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

def GetHumanReadable(size,precision=2):
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
                         choices=['pictures', 'all'],
                         default='all')
    parser.add_argument('--only-extension',
                         help=('compare files with given extension'))
    parser.add_argument('--exclude-extensions',
                         help=('Which extensions should be ignored '
                               'Separate multiple extensions with space'),
                         nargs='+')
    parser.add_argument('--delete-duplicates',
                         help=('Delete any duplicate files found. '
                               'By default the duplicate file will be renamed. '
                               'FORMAT: originalFileName_timestamp_duplicateFileName '
                               '(default: "%(default)s")'),
                         default=False,
                         action='store_true',
                         dest='delete_duplicates')
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

    if args.exclude_extensions:
        excluded_exts=args.exclude_extensions
        filters.append(is_excluded)

    if args.only_extension:
        only_ext=args.only_extension
        filters.append(is_custom_ext)

    logger.info("Start!")
    
    if args.custom_locations:
        locations = args.custom_locations
    else:
        find_locations(args.location, args.levels)
    
    for location in locations:
        logger.info("Checking location: %s", location)
        find_dups(location, filters, args.delete_duplicates, args.delete_empty_folders)

    logger.info("Done!")