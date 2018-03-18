#! /usr/bin/env python

"""Conversion functions for data collected earlier"""

import json
import sys
from DataPoint import DataPoint

class ConvertData(object):
	"""Conversion functions for data collected earlier"""
	def __init__(self, in_filename="InitialData_Sat_Mar_17_06_17_54_2018.txt", in_type="json_linedel",
	      out_filename="InitialData_converted_Sat_Mar_17_06_17_54_2018.csv", out_type="csv"):
		self.in_filename = in_filename
		self.out_filename = out_filename
		self.in_type = in_type
		self.out_type = out_type
		self.data_points = []
		decoders = {
			'json':self.from_json,
			'json_linedel':self.from_json_linedel,
			'csv':self.from_csv,
		}
		with open(in_filename, 'r') as in_file:
			in_data = in_file.read().decode('utf8')
		if in_type in decoders:
			decoder = decoders[in_type]
			decoder(in_data)
		encoders = {
			'json':self.to_json,
			'json_linedel':self.to_json_linedel,
			'csv':self.to_csv,
		}
		if out_type in encoders:
			encoder = encoders[out_type]
			out_data = encoder()
		with open(out_filename, 'w') as out_file:
			out_file.write(out_data.encode('UTF-8'))

	def from_csv(self, data):
		"""conversion function for importing from csv format"""
		if data is None:
			return
		for line in data.split('\n'):
			self.data_points.append(DataPoint(from_type='csv', data=line))

	def from_dict(self, data):
		"""conversion function for importing from dict format"""
		if data is None:
			return
		for item in data:
			self.data_points.append(DataPoint(from_type='dict', data=item))

	def from_json(self, data):
		"""conversion function for importing from json format"""
		if data is None:
			return
		self.from_dict(json.loads(data))

	def from_json_linedel(self, data):
		"""conversion function for importing from json_linedel format"""
		if data is None:
			return
		print "decoding:"
		prnt_cnt = 0
		prnt_tot = len(data.split('\n'))
		for line in data.split('\n'):
			sys.stdout.write("\r")
			sys.stdout.write(str(prnt_cnt))
			sys.stdout.write("/")
			sys.stdout.write(str(prnt_tot))
			sys.stdout.flush()
			prnt_cnt = prnt_cnt + 1

			self.data_points.append(DataPoint(from_type='json', data=line))
		print ""

	def to_csv(self):
		"""conversion function for exporting to csv format"""
		ret = ''
		print "exporting:"
		prnt_cnt = 0
		prnt_tot = len(self.data_points)
		for item in self.data_points:
			sys.stdout.write("\r")
			sys.stdout.write(str(prnt_cnt))
			sys.stdout.write("/")
			sys.stdout.write(str(prnt_tot))
			sys.stdout.write("    ")
			sys.stdout.write(str(len(ret)))
			sys.stdout.write(" bytes")
			sys.stdout.flush()
			prnt_cnt = prnt_cnt + 1

			if item.valid:
				ret = ret + item.to_csv() + '\n'
		print ""
		return ret

	def to_dict(self):
		"""conversion function for exporting to dict format"""
		ret = []
		for item in self.data_points:
			if item.valid:
				ret.append(item.to_dict())
		return ret

	def to_json(self):
		"""conversion function for exporting to json format"""
		return json.dumps(self.to_dict(), indent=4)

	def to_json_linedel(self):
		"""conversion function for exporting to json_linedel format"""
		ret = ''
		for item in self.data_points:
			if item.valid:
				ret = ret + item.to_json_single_line() + '\n'
		return ret

if __name__ == "__main__":
	# # DATES = ['Sat_Mar_17_04_50_56_2018', 'Sat_Mar_17_04_52_27_2018', 'Sat_Mar_17_05_51_12_2018',
	# #   'Sat_Mar_17_05_53_05_2018', 'Sat_Mar_17_06_03_13_2018', 'Sat_Mar_17_06_03_34_2018',
	# #   'Sat_Mar_17_06_06_50_2018']
	# # for date in DATES:
	# # 	ConvertData(in_filename="InitialData_"+date+".txt",
	# # 	out_filename="InitialData_converted_"+date+".csv")
	ConvertData()
	# ConvertData(in_filename="InitialData_Sat_Mar_17_06_15_13_2018.txt",
	#      out_filename="InitialData_converted_Sat_Mar_17_06_15_13_2018.csv")
