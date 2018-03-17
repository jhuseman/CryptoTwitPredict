#! /usr/bin/env python

"""Collection of different output functions"""

import sys

class DataOutput(object):
	"""Output class to handle output of data"""
	def __init__(self, out_filename=None, print_to_console=True):
		self.out_file = None
		self.out_filename = None
		self.change_file(out_filename)
		self.print_to_console = print_to_console

	def __del__(self):
		self.close_file()

	def out_raw(self, data, screen_only=False):
		"""prints the data given"""
		if self.print_to_console:
			sys.stdout.write(data.encode('utf-8', 'ignore'))
			sys.stdout.flush()
		if self.out_file != None and not screen_only:
			self.out_file.write(data.encode('utf-8', 'ignore'))
			self.out_file.flush()

	def out(self, data, screen_only=False):
		"""prints the data given, followed by a newline"""
		self.out_raw(data, screen_only=screen_only)
		self.out_raw("\n", screen_only=screen_only)

	def change_file(self, out_filename):
		"""switches to using a different file"""
		self.close_file()
		self.out_filename = out_filename
		if self.out_filename is None:
			self.out_file = None
		else:
			self.out_file = open(self.out_filename, mode="w")

	def close_file(self):
		"""closes the writing file"""
		if self.out_file != None:
			self.out_file.close()
			self.out_file = None
		self.out_filename = None
