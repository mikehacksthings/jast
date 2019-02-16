#!/usr/bin/env python
import requests
import hashlib
import urllib3

from alert import ALERT, SUCCESS

class Host:
	def __init__(self, url='', status_code=0, ss_file='', content_hash='', follow_redirects=False, store_headers=False):
		self._url = url
		self._status_code = status_code
		self._ss_file = ss_file
		self._content_hash = content_hash
		self._follow_redirects = follow_redirects
		self._store_headers = store_headers
		self._headers = {}
		self.error = False
		self.error_msg = ''

	def set_url(self, url):
		self._url = url

	def get_url(self):
		return self._url

	def set_status_code(self, status_code):
		self._status_code = status_code

	def get_status_code(self):
		return self._status_code

	def set_ss_filename(self, file):
		self._ss_file = file

	def get_ss_filename(self):
		return self._ss_file

	def set_hash(self, content):
		m = hashlib.sha256()
		m.update(content.text.encode('utf-8'))
		self._content_hash = m.hexdigest()

	def get_hash(self):
		return self._content_hash

	def add_header(self, headers):
		self._headers = headers

	def get_headers(self):
		return self._headers

	def store_headers(self):
		return self._store_headers

	def check_host(self):
		try:
			urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
			request = requests.get(self._url,
								   allow_redirects=False,
								   verify=False,
								   timeout=10)
			self.set_status_code(request.status_code)

			if (request.status_code == 302 or request.status_code == 301) and self._follow_redirects:
				self.set_url(request.headers['Location'])
				request = requests.get(self._url,
									   allow_redirects=True,
									   verify=False,
									   timeout=10)

			if request.raise_for_status() is None:
				try:
					if self._store_headers:
						self.add_header(request.headers)
				except KeyError:
					pass

				self.set_hash(request)

				return True
			else:
				print(ALERT + "Bad HTTP response code from host: {0}. Skipping.".format(str(request.status_code)))
				return False

		except (requests.ConnectionError, requests.HTTPError) as error:
			print(ALERT + "Error taking screenshot for host. See report for details. Skipping.")
			self.error_msg = error
			return False

		except (urllib3.exceptions.ReadTimeoutError, requests.exceptions.ReadTimeout) as error:
			print(ALERT + "Timeout taking screenshot for host. See report for details. Skipping.")
			self.error_msg = error
			return False