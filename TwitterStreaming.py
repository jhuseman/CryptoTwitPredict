#! /usr/bin/env python

"""File handling streaming of Twitter API"""

import tweepy

class TwitterStreaming(tweepy.StreamListener):
	"""Class to contain functions for streaming of data from Twitter"""
	def __init__(self, callback):
		self.callback = callback
		super(TwitterStreaming, self).__init__()

	def on_status(self, status):
		"""Callback for streamed data from Twitter"""
		self.callback(status)
