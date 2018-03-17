#! /usr/bin/env python

"""CryptoCompare: Collect Data from CryptoCompare API"""

import json
import requests

class CryptoCompare(object):
	"""CryptoCompare: Collect Data from CryptoCompare API"""
	def __init__(self, basis=["USD"], crypto=["BTC", "ETH"]): # pylint: disable=W0102
		self.basis = basis
		self.crypto = crypto

	def get_tsyms(self):
		"""Get list of basis currencies in format for URL"""
		ret = self.basis[0]
		for base in self.basis[1:]:
			ret = ret + ',' + base
		return ret

	def get_fsyms(self):
		"""Get list of cryptocurrencies in format for URL"""
		ret = self.crypto[0]
		for crypt in self.crypto[1:]:
			ret = ret + ',' + crypt
		return ret

	def get_api_url(self):
		"""Get URL for the current value of the specified currencies"""
		return "https://min-api.cryptocompare.com/data/pricemulti?fsyms={fsyms}&tsyms={tsyms}".format(
			fsyms=self.get_fsyms(),
			tsyms=self.get_tsyms(),
		)

	def get_current_data(self):
		"""Get the current value of the specified currencies"""
		req = requests.get(self.get_api_url())
		return json.loads(req.content)
