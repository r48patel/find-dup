from find_dup import *
from os.path import isfile, join, isdir, getsize

def test_find_locations():
	assert find_locations("test_resources/test_images", 1) == ['test_resources/test_images']
	assert find_locations(".", 2) == ['.', './test_resources']
	assert find_locations(".", 4) == ['.', './test_resources', './test_resources/test_images', './test_resources/test_images/dir_1', './test_resources/test_images/dir_2']


def test_find_dups():
	expected_dict = collections.OrderedDict()
	expected_dict['./test_resources/test_images/1.jpg'] = [
		'./test_resources/test_images/dir_1/1.jpg',
		'./test_resources/test_images/dir_1/1a.jpg',
		'./test_resources/test_images/dir_1/1b.jpg',
		'./test_resources/test_images/dir_1/1c.jpg',
		'./test_resources/test_images/dir_1/1d.jpg',
		'./test_resources/test_images/dir_2/1b.jpg',
		'./test_resources/test_images/dir_2/1c.jpg',
		'./test_resources/test_images/dir_2/1d.jpg'
	]
	expected_dict['./test_resources/test_images/dir_1/2.jpg'] = [
			'./test_resources/test_images/dir_1/2a.jpg',
			'./test_resources/test_images/dir_1/2b.jpg',
			'./test_resources/test_images/dir_2/2.jpg',
	]
	expected_dict['./test_resources/test_images/4.jpg'] = [
		'./test_resources/test_images/dir_1/4.jpg',
	]
	expected_dict['./test_resources/test_images/5.jpg'] = [
		'./test_resources/test_images/dir_1/5.jpg',
		'./test_resources/test_images/dir_2/5.jpg',
	]
	

	filters = [isfile,is_ds_store]
	dup_dict = find_dups(find_locations(".", 4), filters, False)
	assert dup_dict == expected_dict
