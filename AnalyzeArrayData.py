#! /usr/bin/env python

"""
Do an analysis on the given data in arr_json file, and save it to a file.
"""

import sys
import json
import copy
from PlotData import get_by_keys

CURRENT_VER = '0.1'

class AnalysisMethods(object):
	"""Class incorporating different analysis versions"""
	def __init__(self, array_list):
		self.array_list = array_list

	def v_compress(self):
		"""
		Version "compress"
		removes less relevant data to reduce file size
		"""
		key = copy.copy(self.array_list[0])
		if 'text' in key:
			key.remove('text')
		if 'screen_name' in key:
			key.remove('screen_name')

		if key == self.array_list[0]:
			return self.array_list
		return [key, get_by_keys(key, self.array_list[0], self.array_list[1])]

	def v_0_0(self):
		"""
		Version 0.0
		simply returns the original data
		"""
		return self.array_list

	def v_0_1(self):
		"""
		Version 0.1
		averages bins of the data
		"""
		keys = self.array_list[0]
		values = self.array_list[1]
		ret_keys = ['time', 'unixtime', 'polarity', 'subjectivity', 'ETH', 'BTC']
		ret_values = []

		bin_size = 10000
		num_vals = len(values)
		i = 0
		while i < num_vals:
			vals = values[i:i+bin_size]
			polarity_avg = sum([r[0] for r in get_by_keys(['polarity'], keys, vals)])/len(vals)
			subjectivity_avg = sum([r[0] for r in get_by_keys(['subjectivity'], keys, vals)])/len(vals)
			ETH_avg = sum([r[0] for r in get_by_keys(['ETH'], keys, vals)])/len(vals)
			BTC_avg = sum([r[0] for r in get_by_keys(['BTC'], keys, vals)])/len(vals)
			time_first = get_by_keys(['time'], keys, vals)[0][0]
			unixtime_first = get_by_keys(['unixtime'], keys, vals)[0][0]
			ret_values.append([time_first, unixtime_first, polarity_avg, subjectivity_avg, ETH_avg, BTC_avg])
			i = i + bin_size
		return [ret_keys, ret_values]

def analyze(array_list, version):
	"""analyzes the data with the given version number of analysis"""
	analysis_version_func_name = 'v_' + version.replace('.', '_')
	analysis_class = AnalysisMethods(array_list)
	analysis_version_func = getattr(analysis_class, analysis_version_func_name)
	return analysis_version_func()

def analyze_file(infile, version):
	"""analyzes the data in the file with the given version number of analysis"""
	arr = None
	with open(infile) as filep:
		arr = json.load(filep)
	return analyze(arr, version)

def save_to_file(data, outfile):
	"""simply saves the data in json format to the file"""
	with open(outfile, 'w') as filep:
		json.dump(data, filep)

def analyze_file_save(infile, outfile, version):
	"""analyzes the data in the file with the given version number of analysis and saves to outfile"""
	arr = analyze_file(infile, version)
	save_to_file(arr, outfile)

def get_kwargs_raw(argv):
	"""returns the arguments that should be given to the plot_data function"""
	infile = None
	outfile = None
	version = CURRENT_VER

	if len(argv) > 1:
		infile = argv[1]
	if len(argv) > 2:
		outfile = argv[2]
	if len(argv) > 3:
		version = argv[3]

	return [infile, outfile, version]

def get_kwargs():
	"""returns the arguments that should be given to the plot_data function"""
	return get_kwargs_raw(sys.argv)

if __name__ == "__main__":
	PARAMS = get_kwargs()
	analyze_file_save(PARAMS[0], PARAMS[1], PARAMS[2])
