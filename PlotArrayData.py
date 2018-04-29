#! /usr/bin/env python

"""Plot the data given in array_json format, using the specified keys"""

import sys
import json
import matplotlib.pyplot as plt
from PlotData import get_by_keys

def plot_data(array_list, params):
	"""plots the data set using matplotlib"""
	key = array_list[0]
	vals = array_list[1]
	print key
	print len(vals)
	figure_id = 1
	for item in params:
		x_axis = get_by_keys(item['x_keys'], key, vals)
		y_axis = get_by_keys(item['y_keys'], key, vals)
		plt.figure(figure_id)
		plt.plot(x_axis, y_axis)
		figure_id = figure_id + 1
	plt.show()

def plot_file(filename, params):
	"""plots the data in the file with the specified parameters"""
	arr = None
	with open(filename) as filep:
		arr = json.load(filep)
	plot_data(arr, params)

def get_kwargs_raw(argv):
	"""returns the arguments that should be given to the plot_data function"""
	infile = None
	params = []

	if len(argv) > 1:
		infile = argv[1]

	i = 1
	while i < (len(argv)-2):
		params.append({
			'x_keys':argv[i+1].split(','),
			'y_keys':argv[i+2].split(','),
		})
		i = i + 2

	return [infile, params]

def get_kwargs():
	"""returns the arguments that should be given to the plot_data function"""
	return get_kwargs_raw(sys.argv)

if __name__ == "__main__":
	PARAMS = get_kwargs()
	plot_file(PARAMS[0], PARAMS[1])
