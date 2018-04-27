#! /usr/bin/env python

"""Concatenates data from different encodings"""

import sys
import json

from PlotData import get_by_keys

def load_arr_from_file(fname):
	"""returns the arr data from the file"""
	with open(fname) as filep:
		return json.load(filep)

def write_arr_to_file(fname, data):
	"""encodes the arr data in json format"""
	with open(fname, 'w') as filep:
		json.dump(data, filep)

def concat_two_arrs(arr1, arr2):
	"""concatenates the two arrays and makes sure headers match"""
	if arr1[0] == arr2[0]:
		return [arr1[0], (arr1[1]+arr2[1])]
	headers = []
	for head in arr1[0]: # get the headers that are in both
		if head in arr2[0]:
			headers.append(head)
	if headers == arr1[0]:
		trim_a1 = arr1[1]
	else:
		trim_a1 = get_by_keys(headers, arr1[0], arr1[1])
	if headers == arr2[0]:
		trim_a2 = arr2[1]
	else:
		trim_a2 = get_by_keys(headers, arr2[0], arr2[1])
	return [headers, (trim_a1+trim_a2)]

def concat_arr_data_files(out_file, in_files):
	"""
	concatenates all of the pieces of data from the list in_files
	and outputs it to a single file described by out_file

	only works with arr.json format files (or sent.arr.json)
	"""
	print "Loading from file {f}".format(f=in_files[0])
	data = load_arr_from_file(in_files[0])
	for infi in in_files[1:]:
		print "Concatenating data from file {f}".format(f=infi)
		data = concat_two_arrs(data, load_arr_from_file(infi))
	print "Writing to file {f}".format(f=out_file)
	write_arr_to_file(out_file, data)

def get_kwargs():
	"""returns the arguments that should be given to the initializer for ConvertData"""
	ret = {
		"out":None,
		"in":[],
	}

	i = 0
	while i < (len(sys.argv)-2):
		ret['in'].append(sys.argv[i+1])
		i = i + 1
	ret['out'] = sys.argv[i+1]

	return ret

if __name__ == "__main__":
	FILEINFO = get_kwargs()
	concat_arr_data_files(FILEINFO["out"], FILEINFO["in"])
