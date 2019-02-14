#!/usr/bin/env python
# Name: JAST - Just Another Screenshot Tool
# Description: JAST is a tool to capture web server screenshots
#   and server information using headless Firefox/Selenium.
# Version: 0.2.0
# Author: Mike Lisi (mike@mikehacksthings.com)

"""
JAST

Usage:
  jast.py [options] (-u URL | -f FILE) -o DIR
  jast.py (-h | --help)
  jast.py (-v | --version)

Arguments:
  -u	Single URL to screenshot.
  -f	File containing hosts to screenshot.
  -o	Output directory.

Screenshot Options:
  -s --size SIZE  	Screenshot window size [default: 800x600].
  --headers  		Include HTTP Headers in report.
  --follow-redirects  	Follow redirects before taking screenshot.

Options:
  -h --help  		Show this screen.
  -v --version  	Show version.
"""

import os
import sys
import time
import requests
import hashlib
import urllib3
from docopt import docopt
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

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
				print("\033[0;31m[!]\033[0m Bad HTTP response code from host: {0}. Skipping.".format(str(request.status_code)))
				return False

		except (requests.ConnectionError, requests.HTTPError) as error:
			print("\033[0;31m[!]\033[0m Error taking screenshot for host. See report for details. Skipping.")
			host.error_msg = error
			return False

		except (urllib3.exceptions.ReadTimeoutError, requests.exceptions.ReadTimeout) as error:
			print("\033[0;31m[!]\033[0m Timeout taking screenshot for host. See report for details. Skipping.")
			host.error_msg = error
			return False


class Report:
	def __init__(self, args={}):
		self._args = args
		self._report_dir = args['-o']
		self._header = """
		<!DOCTYPE html>
		<html>
			<head>
				<title>JAST Report</title>
				<link rel="stylesheet" type="text/css" href="style.css">
				<link href="https://fonts.googleapis.com/css?family=EB+Garamond" rel="stylesheet">
				<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
				<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
			</head>
		<body class="m-4 p-4">
		<center>
		<nav class="navbar fixed-top navbar-dark bg-dark">
		  <a class="navbar-brand brand-text mx-auto" href="#">JAST Report</a>
		</nav>
		"""

		self.footer = """
			</body></html>
		"""

		self.style = """
		body {
			font-family: "EB+Garamond", sans-serif;
			background-color: #FFF;
		}
		hr {
			width: 50%;
		}

		"""

	def create_report_dir(self):
		if os.path.isdir(self._report_dir) and os.path.exists(self._report_dir):
			print("\033[0;31m[!]\033[0m Failed to create directory {0}. Directory already exists! Exiting.".format(self._report_dir))
			sys.exit(-1)
		else:
			try:
				os.mkdir(self._report_dir)
				os.mkdir(self._report_dir + "/screenshots")
				return
			except OSError:
				print("\033[0;31m[!]\033[0m Failed to create {0}.".format(self._report_dir))

				sys.exit(-1)

	def start(self):
		f = open(self._report_dir + "/report.html", 'w')
		f.write(self._header)
		f.close()

		f = open(self._report_dir + "/style.css", 'w')
		f.write(self.style)
		f.close()

	def write_host(self, host):
		host_data = "<div class =\"card mt-4 mb-4\">\n"

		if host.error:
			host_data += "\t<div class =\"card-footer\">\n\t\t<p class=\"card-text\"><h4>"
			host_data += "{0}</h4>\n<h5>Error taking screenshot:</h5><br>\n{1}<br>\n".format(host.get_url(), host.error_msg)
			f = open(self._report_dir + "/report.html", 'a')
			f.write(host_data)
			f.close()
		else:
			host_data += "\t<img src=\"{0}\" class =\"card-img-top\" />\n".format(host.get_ss_filename())
			host_data += "\t<div class =\"card-footer\">\n\t\t<p class=\"card-text\"><h4>"
			host_data += "<a href=\"{0}\" target=\"_blank\">{1}</a></h4>".format(host.get_url(), host.get_url())

			f = open(self._report_dir + "/report.html", 'a')
			f.write(host_data)

			if host.store_headers() is True:
				for key, value in host.get_headers().items():
					f.write("<b>" + key + ": " + value + "</b><br>")

			f.write("</p>\n\t</div>\n</div>")
		f.close()

	def finish(self):
		f = open(self._report_dir + "/report.html", 'a')
		f.write(self.footer)
		f.close()


class Browser:
	def __init__(self, size="800x600"):
		try:
			self._width, self._height = size.split('x')

		except:
			print("\033[0;31m[!]\033[0m Error parsing browser window size, defaulting to 800x600")
			self._width = 800
			self._height = 600

		self._browser = self.start_browser(self, self._width, self._height)

	def get_url(self, url):
		self._browser.get(url)

	def save_image(self, path):
		self._browser.save_screenshot(path)


	@staticmethod
	def start_browser(self, width, height):
		options = Options()
		options.add_argument('--headless')
		b = Firefox(executable_path='geckodriver',
					options=options)
		b.set_window_size(width, height)
		return b

	def close(self):
		self._browser.quit()


def process_hosts(data, args):
	hosts = []
	for item in data:
		u = item.rstrip('\n')
		if 'http' not in u:
			print("\033[0;31m[!]\033[0m No protocol supplied for host: {0}. Use format http(s)://<host> Skipping...".format(u))
			continue
		try:
			image_file = u.split('//')[1]
			for c in [':', '/', '.']:
				image_file = image_file.replace(c, '_')

			output_file = "screenshots/" + image_file + "_" + str(int(time.time())) + ".png"
			host = Host(store_headers=args['--headers'],
						follow_redirects=args['--follow-redirects'])
			host.set_url(u)
			host.set_ss_filename(output_file)
			hosts.append(host)

		except IndexError:  # URL doesn't begin with a protocol
			print("\033[0;31m[!]\033[0m No protocol supplied for host: {0}. Use format http(s)://<host> Skipping...".format(u))
			continue

	return hosts


def take_screenshot(h, b, args):
	print("\033[0;32m[+]\033[0m Taking screenshot for URL: {0}".format(h.get_url()))
	if host.check_host():
		try:
			b.get_url(h.get_url())
			b.save_image(args['-o'] + "/" + h.get_ss_filename())

		except:
			# There was an error
			print("\033[0;31m[!]\033[0m Error taking screenshot for host{0}, skipping.".format(h.get_url()))
			host.error = True
	else:
		host.error = True


if __name__ == '__main__':
	args = docopt(__doc__, version='JAST - Just Another Screenshot Tool v0.0.2')

	data = []
	hosts = []

	print("\033[0;32m[+]\033[0m Processing host(s)...")
	if args['-f']:
		if os.path.exists(args['-f']) and os.path.isfile(args['-f']):
			f = open(args['-f'], 'r')
			data = f.readlines()
			f.close()
		else: # File doesn't exist
			print("\033[0;31m[!]\033[0m Host file not found! Exiting.")
			sys.exit(-1)

	elif args['-u']:
		data = [args['-u']]

	hosts = process_hosts(data, args)

	if len(hosts) == 0:
		print("\033[0;31m[!]\033[0m No hosts processed, exiting...")
		sys.exit(-1)

	report = Report(args)
	report.create_report_dir()

	browser = Browser(size=args['--size'])
	for host in hosts:
		take_screenshot(host, browser, args)
	browser.close()

	report.start()
	for host in hosts:
		report.write_host(host)
	report.finish()

	print("\033[0;32m[+]\033[0m Complete.")
	print("\033[0;32m[+]\033[0m Report written to {0}/report.html".format(args['-o']))
