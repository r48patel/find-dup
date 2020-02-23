from find_dup import *
from os.path import isfile, join, isdir, getsize

def inc(x):
    return x + 1

def test_find_locations():
	assert find_locations("test_resources/test_images", 1) == ['test_resources/test_images']
	assert find_locations(".", 2) == ['.', './test_resources']
	assert find_locations(".", 4) == ['.', './test_resources', './test_resources/test_images']


def test_find_dups():
	expected_info_table = PrettyTable(['Original File', 'Duplicate File', 'Size', 'Action'])
	expected_info_table.align = 'l'
	expected_info_table.add_row(["test_resources/test_images/Scan 104-1.jpeg", "test_resources/test_images/Scan 104-0.jpeg", "1.38 MB", "Dry Run!"])
	expected_info_table.add_row(["test_resources/test_images/Scan 104-1.jpeg", "test_resources/test_images/Scan 104-4.jpeg", "1.38 MB", "Dry Run!"])
	expected_info_table.add_row(["test_resources/test_images/Scan 104-1.jpeg", "test_resources/test_images/Scan 104-3.jpeg", "1.38 MB", "Dry Run!"])
	expected_info_table.add_row(["test_resources/test_images/Scan 104-1.jpeg", "test_resources/test_images/Scan 103.jpeg", "1.38 MB", "Dry Run!"])
	expected_info_table.add_row(["test_resources/test_images/Scan 104-1.jpeg", "test_resources/test_images/Scan 104-2.jpeg", "1.38 MB", "Dry Run!"])

	filters = [isfile,is_ds_store]
	x = find_dups("test_resources/test_images", "test_resources/test_images/duplicates", filters, FILE_OPTIONS.dry_run, False)
	
	assert x.get_string() == expected_info_table.get_string()
