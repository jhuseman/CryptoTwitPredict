#! /usr/bin/env python

"""Conversion functions for data collected earlier"""

import json
import sys
from DataPoint import DataPoint

class ConvertData(object):
	"""Conversion functions for data collected earlier"""
	def __init__(self, in_filename=None, in_type="jsonl", out_filename=None, out_type=None,
	      in_data_raw=None):
		self.in_filename = in_filename
		self.out_filename = out_filename
		self.in_type = in_type
		self.out_type = out_type
		self.data_points = []
		decoders = {
			'json':self.from_json,
			'jsonl':self.from_jsonl,
			'csv':self.from_csv,
		}
		if not in_filename is None:
			with open(in_filename, 'r') as in_file:
				in_data = in_file.read().decode('utf8')
		else:
			in_data = in_data_raw
		if in_type in decoders:
			decoder = decoders[in_type]
			decoder(in_data)
		if not out_type is None:
			encoders = {
				'json':self.to_json,
				'jsonl':self.to_jsonl,
				'csv':self.to_csv,
				'csv_sent':self.to_csv_sent,
				'json_sent':self.to_json_sent,
				'jsonl_sent':self.to_jsonl_sent,
			}
			if out_type in encoders:
				encoder = encoders[out_type]
				out_data = encoder()
				if out_filename is None:
					sys.stdout.write(out_data.encode('UTF-8'))
				else:
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

	def from_jsonl(self, data):
		"""conversion function for importing from jsonl format"""
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
		to_ret = []
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
			if len(ret) > 100000:
				to_ret.append(ret)
				ret = ''
		print ""
		if to_ret:
			to_ret.append(ret)
			ret = ''
			for val in to_ret:
				ret = ret + val
		return ret

	def to_csv_sent(self):
		"""conversion function for exporting to csv format with sentiment analysis"""
		to_ret = []
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
				ret = ret + item.to_csv_sent() + '\n'
			if len(ret) > 100000:
				to_ret.append(ret)
				ret = ''
		print ""
		if to_ret:
			to_ret.append(ret)
			ret = ''
			for val in to_ret:
				ret = ret + val
		return ret

	def to_dict(self):
		"""conversion function for exporting to dict format"""
		ret = []
		for item in self.data_points:
			if item.valid:
				ret.append(item.to_dict())
		return ret

	def to_dict_sent(self):
		"""conversion function for exporting to dict format with sentiment analysis"""
		ret = []
		for item in self.data_points:
			if item.valid:
				ret.append(item.to_dict_sent())
		return ret

	def to_json(self):
		"""conversion function for exporting to json format"""
		return json.dumps(self.to_dict(), indent=4)

	def to_jsonl(self):
		"""conversion function for exporting to jsonl format"""
		ret = ''
		for item in self.data_points:
			if item.valid:
				ret = ret + item.to_json_single_line() + '\n'
		return ret

	def to_json_sent(self):
		"""conversion function for exporting to json format with sentiment analysis"""
		return json.dumps(self.to_dict(), indent=4)

	def to_jsonl_sent(self):
		"""conversion function for exporting to jsonl format with sentiment analysis"""
		ret = ''
		for item in self.data_points:
			if item.valid:
				ret = ret + item.to_json_sent_single_line() + '\n'
		return ret

def get_kwargs():
	"""returns the arguments that should be given to the initializer for ConvertData"""
	infiletype = "jsonl"
	infile = None
	outfiletype = "csv"
	outfile = None

	if len(sys.argv) > 1:
		infiletype = sys.argv[1]
	if len(sys.argv) > 2:
		infile = sys.argv[2]
	if len(sys.argv) > 3:
		outfiletype = sys.argv[3]
	if len(sys.argv) > 4:
		outfile = sys.argv[4]

	return {
		"in_filename":infile,
		"in_type":infiletype,
		"out_filename":outfile,
		"out_type":outfiletype,
	}

if __name__ == "__main__":
	FILEINFO = get_kwargs()
	ConvertData(
		out_filename=FILEINFO['out_filename'],
		out_type=FILEINFO['out_type'],
		in_filename=FILEINFO['in_filename'],
		in_type=FILEINFO['in_type'],
	)
