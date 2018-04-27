#! /usr/bin/env python

"""Concatenates data from different encodings"""

import sys
from ConvertData import ConvertData

def concat_data(out_fileinfo, in_fileinfo):
	"""
	concatenates all of the pieces of data from the list in_fileinfo
	and outputs it to a single file described by out_fileinfo

	expects a fileinfo to be {'filename':'test.jsonl', 'type':'jsonl'}
	"""
	data = ConvertData(
		out_filename=None,
		out_type=None,
		in_filename=None,
		in_type=None,
	)
	for infi in in_fileinfo:
		data.decode_as(
			in_filename=infi['filename'],
			in_type=infi['type'],
		)
	data.encode_as(
		out_filename=out_fileinfo['filename'],
		out_type=out_fileinfo['type'],
	)

def get_kwargs():
	"""returns the arguments that should be given to the initializer for ConvertData"""
	ret = {
		"out":{},
		"in":[],
	}

	i = 0
	while i < (len(sys.argv)-4):
		ret['in'].append({
			'type':sys.argv[i+1],
			'filename':sys.argv[i+2],
		})
		i = i + 2
	ret['out']['type'] = sys.argv[i+1]
	ret['out']['filename'] = sys.argv[i+2]

	return ret

if __name__ == "__main__":
	FILEINFO = get_kwargs()
	concat_data(FILEINFO["out"], FILEINFO["in"])
