#! /usr/bin/env python

"""CollectComparisonData: Collect Data from Twitter and CryptoCompare APIs"""

from TwitterConn import TwitterConn
from CryptoCompare import CryptoCompare

class CollectComparisonData(object):
	"""CollectComparisonData: Collect Data from Twitter and CryptoCompare APIs"""
	def __init__(self, conn=TwitterConn(), basis=["USD"], cryptos={ # pylint: disable=W0102
			"BTC":{"keywords":["bitcoin", "BTC"]}, "ETH":{"keywords":["etherium", "ETH"]}}): # pylint: disable=W0102
		self.conn = conn
		self.twitter_keywords = []
		self.crypto_abbr = []
		self.cryptos = cryptos
		for key in cryptos:
			self.twitter_keywords = self.twitter_keywords + cryptos[key]["keywords"]
			self.crypto_abbr.append(key)
		self.crypto_basis = basis
		self.ccmp = CryptoCompare(basis=self.crypto_basis, crypto=self.crypto_abbr)

	def get_stream_combined_data(self, callback):
		"""Get streamed data from Twitter and combine with CryptoCompare data"""
		def int_callback(tweet):
			"""callback for get_stream_combined_data"""
			prices = self.ccmp.get_current_data()
			callback({"tweet":tweet, "prices":prices})
		return self.conn.create_stream(int_callback)

	def get_data(self, callback):
		"""Get streamed data"""
		self.get_stream_combined_data(callback).filter(track=self.twitter_keywords)

	def get_abbrev_data(self, callback):
		"""Get streamed data and simplify some of it"""
		def int_callback(dat):
			"""callback for get_abbrev_data"""
			long_tweet = dat['tweet']
			tweet = {
				'screen_name':long_tweet.user.screen_name,
				'text':long_tweet.text,
			}
			prices = dat['prices']
			callback({"tweet":tweet, "prices":prices})
		return self.get_data(int_callback)
