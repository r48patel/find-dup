from find_dup import *
from os.path import isfile, join, isdir, getsize

def test_find_locations():
	assert find_locations("test_resources/test_images", 1) == ['test_resources/test_images']
	assert find_locations(".", 2) == ['.', './test_resources']
	assert find_locations(".", 4) == ['.', './test_resources', './test_resources/test_images']


def test_find_dups():
	expected_dict = {
		'test_resources/test_images/Scan 104-1.jpeg': [
			'test_resources/test_images/Scan 104-0.jpeg', 
			'test_resources/test_images/Scan 104-4.jpeg', 
			'test_resources/test_images/Scan 104-3.jpeg', 
			'test_resources/test_images/Scan 103.jpeg', 
			'test_resources/test_images/Scan 104-2.jpeg'
		]
	}

	filters = [isfile,is_ds_store]
	dup_dict = find_dups("test_resources/test_images", "test_resources/test_images/duplicates", filters, FILE_OPTIONS.dry_run, False)
	
	assert dup_dict == expected_dict
