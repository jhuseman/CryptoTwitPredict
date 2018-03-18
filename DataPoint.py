#! /usr/bin/env python

"""A data point for the collected data"""

import csv
import json
import time

class DataPoint(object):
	"""A data point for the collected data"""
	def __init__(self, from_type='json', data=None):
		self.basis_currency = "USD"
		self.timestamp = None
		self.prices = {}
		self.tweet_data = {}
		self.valid = False
		decoders = {
			'dict':self.from_dict,
			'json':self.from_json,
			'csv':self.from_csv,
		}
		if from_type in decoders:
			decoder = decoders[from_type]
			decoder(data)

	def from_csv(self, data):
		"""conversion function for importing from csv format"""
		if not data:
			return
		self.valid = True
		fields = list(csv.reader([data]))[0]
		self.timestamp = time.strptime(fields[0], '%c')
		self.tweet_data = {
			"screen_name":fields[1],
			"text":fields[2],
		}
		is_key = True
		key = ''
		for item in fields[3:]:
			if is_key:
				is_key = False
				key = item
			else:
				is_key = True
				self.prices[key] = {self.basis_currency: item}

	def from_dict(self, data):
		"""conversion function for importing from dict format"""
		if not data:
			return
		self.valid = True
		self.timestamp = time.strptime(data['time'], '%c')
		self.prices = data['data']['prices']
		self.tweet_data = data['data']['tweet']

	def from_json(self, data):
		"""conversion function for importing from json format"""
		if not data:
			return
		self.from_dict(json.loads(data))

	def get_price_csv(self):
		"""returns price data in csv format"""
		ret = ''
		for key in self.prices:
			if ret:
				ret = ret + ','
			ret = ret + '{type},{price}'.format(
				type=key,
				price=self.prices[key][self.basis_currency],
			)
		return ret

	def get_tweet_csv(self):
		"""returns tweet info in csv format"""
		return u'"{screen_name}","{text}"'.format(
			screen_name=self.tweet_data['screen_name'].replace('"', '""'),
			text=self.tweet_data['text'].replace('"', '""').replace('\n', '\\n'),
		)

	def to_csv(self):
		"""conversion function for exporting to csv format"""
		return u'{timestamp},{tweet_csv},{price_csv}'.format(
			timestamp=time.asctime(self.timestamp),
			tweet_csv=self.get_tweet_csv(),
			price_csv=self.get_price_csv(),
		)

	def to_dict(self):
		"""conversion function for exporting to dict format"""
		return {
			"time": time.asctime(self.timestamp),
			"data": {
				"prices": self.prices,
				"tweet": self.tweet_data,
			},
		}

	def to_json(self):
		"""conversion function for exporting to json format"""
		return json.dumps(self.to_dict(), indent=4)

	def to_json_single_line(self):
		"""conversion function for exporting to json format in a single line"""
		return json.dumps(self.to_dict())
