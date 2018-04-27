#! /usr/bin/env python

"""Plot the data given a specific format"""

import os
import sys
import json
import matplotlib.pyplot as plt
from ConvertData import ConvertData

def get_by_keys(desired_keys, all_keys, vals):
	"""gets by keys"""
	def get_by_indexes(indices, vals):
		"""asdfasdfasdf"""
		ret = []
		for i in indices:
			ret.append(vals[i])
		return ret

	offsets = []
	for key in desired_keys:
		offsets.append(all_keys.index(key))
	return [get_by_indexes(offsets, r) for r in vals]

def plot_data(array_list):
	"""plots the data set using matplotlib"""
	key = array_list[0]
	vals = array_list[1]
	print key
	x_axis_keys = ['unixtime']
	y_axis_keys = ['BTC']
	y_axis_b_keys = ['polarity']
	timestamps = get_by_keys(x_axis_keys, key, vals)
	x_axis = [t[0]-timestamps[0][0] for t in timestamps]
	y_axis = get_by_keys(y_axis_keys, key, vals)
	y_axis_b = get_by_keys(y_axis_b_keys, key, vals)
	plt.figure(1)
	plt.subplot(211)
	plt.plot(x_axis, y_axis)
	plt.subplot(212)
	plt.plot(x_axis, y_axis_b)
	plt.show()

def get_kwargs():
	"""returns the arguments that should be given to the initializer for ConvertData"""
	infiletype = "jsonl"
	infile = None
	outfiletype = "array_sent_json"

	if len(sys.argv) > 1:
		infiletype = sys.argv[1]
	if len(sys.argv) > 2:
		infile = sys.argv[2]

	inf = os.path.splitext(infile)
	outfile = inf[0]+'.sent.arr.json'
	if ".sent.arr.json" in infile:
		outfiletype = None
		outfile = None

	return {
		"in_filename":infile,
		"in_type":infiletype,
		"out_filename":outfile,
		"out_type":outfiletype,
	}

if __name__ == "__main__":
	FILEINFO = get_kwargs()
	ARR_SENT = None
	if FILEINFO['in_type'] == "array_sent_json":
		with open(FILEINFO['in_filename']) as fp:
			ARR_SENT = json.load(fp)
	else:
		DATA = ConvertData(
			out_filename=FILEINFO['out_filename'],
			out_type=FILEINFO['out_type'],
			in_filename=FILEINFO['in_filename'],
			in_type=FILEINFO['in_type'],
		)
		ARR_SENT = DATA.to_array_sent()
	plot_data(ARR_SENT)
