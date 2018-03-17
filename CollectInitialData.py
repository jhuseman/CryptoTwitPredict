#! /usr/bin/env python

"""CollectInitialData: Collect Data from Twitter and CryptoCompare APIs"""

import time
import json

from CollectComparisonData import CollectComparisonData
from DataOutput import DataOutput

def get_timestamp():
	"""ts"""
	return time.asctime(time.gmtime())

class CollectInitialData(object):
	"""CollectInitialData: Collect Data from Twitter and CryptoCompare APIs"""
	def __init__(self, conn=CollectComparisonData(), dout=DataOutput(out_filename='InitialData_'+get_timestamp().replace(':','_').replace(' ','_')+'.txt')):
		self.conn = conn
		self.dout = dout

	def __del__(self):
		self.dout.__del__()

	def print_dat(self, dat):
		"""Print a message nicely"""
		self.dout.out(json.dumps(dat))

	def add_timestamp(self, dat):
		"""adds a timestamp"""
		return {
			'time':get_timestamp(),
			'data':dat,
		}

	def run(self):
		"""Main execution function"""
		def callback(dat):
			"""f"""
			self.print_dat(self.add_timestamp(dat))

		self.conn.get_abbrev_data(callback)


if __name__ == "__main__":
	CollectInitialData().run()
