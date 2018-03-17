#! /usr/bin/env python

"""CollectInitialData: Collect Data from Twitter and CryptoCompare APIs"""

import time
import json

from CollectComparisonData import CollectComparisonData
from DataOutput import DataOutput

def get_timestamp():
	"""ts"""
	return time.asctime(time.gmtime())

def get_fname_timestamp():
	"""ts"""
	return get_timestamp().replace(':', '_').replace(' ', '_')

def add_timestamp(dat):
	"""adds a timestamp"""
	return {
		'time':get_timestamp(),
		'data':dat,
	}

class CollectInitialData(object):
	"""CollectInitialData: Collect Data from Twitter and CryptoCompare APIs"""
	def __init__(self, conn=CollectComparisonData(),
	      dout=DataOutput(out_filename='InitialData_'+get_fname_timestamp()+'.txt')):
		self.conn = conn
		self.dout = dout

	def __del__(self):
		self.dout.__del__()

	def print_dat(self, dat):
		"""Print a message nicely"""
		self.dout.out(json.dumps(dat))

	def run(self):
		"""Main execution function"""
		def callback(dat):
			"""f"""
			self.print_dat(add_timestamp(dat))

		self.conn.get_abbrev_data(callback)


if __name__ == "__main__":
	CollectInitialData().run()
