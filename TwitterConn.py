#! /usr/bin/env python

"""Basic file for a twitter connection"""

import json
import os.path
import tweepy
from TwitterStreaming import TwitterStreaming

class TwitterConn(object):
	"""Basic class for a twitter connection"""
	def __init__(self, auth_file="TwitterAuth.json", auth_file_override="TwitterAuth_override.json"):
		self.auth_file = auth_file
		if os.path.isfile(auth_file_override):
			self.auth_file = auth_file_override
		self.auth = None
		self.api = None

	def get_auth(self):
		"""
		Get authentication data
		loads the data from the file if first time accessed
		otherwise caches it
		"""
		if self.auth is None:
			with open(self.auth_file) as auth_file_read:
				auth_data = json.load(auth_file_read)
				self.auth = tweepy.OAuthHandler(auth_data["consumer_key"], auth_data["consumer_secret"])
				self.auth.set_access_token(auth_data["access_token"], auth_data["access_token_secret"])
		return self.auth

	def get_api(self):
		"""
		Get tweepy instance
		creates new instance if first time accessed
		otherwise caches it
		"""
		if self.api is None:
			self.api = tweepy.API(self.get_auth())
		return self.api

	def create_stream(self, callback):
		"""Create new tweepy streaming instance"""
		stream_listener = TwitterStreaming(callback)
		return tweepy.Stream(auth=self.get_api().auth, listener=stream_listener)



if __name__ == "__main__":
	CONN = TwitterConn()

	print CONN.get_api().get_user('13334762')
