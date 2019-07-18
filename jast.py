#!/usr/bin/env python
# Name: JAST - Just Another Screenshot Tool
# Description: JAST is a tool to capture web server screenshots
#   and server information using headless Firefox/Selenium.
# Version: 0.4
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
from docopt import docopt

from host import Host
from browser import Browser
from report import Report
from alert import SUCCESS, FAIL, WARN

header = "\n\
     ██╗ █████╗ ███████╗████████╗\n\
     ██║██╔══██╗██╔════╝╚══██╔══╝\n\
     ██║███████║███████╗   ██║   \n\
██   ██║██╔══██║╚════██║   ██║   \n\
╚█████╔╝██║  ██║███████║   ██║   \n\
 ╚════╝ ╚═╝  ╚═╝╚══════╝   ╚═╝   \n\
                                 \n\
Just Another Screenshot Tool v 0.4\n\
\n\
Author: Mike Lisi (@MikeHacksThings)"

def process_hosts(data, args):
	hosts = []
	for item in data:
		u = item.rstrip('\n')
		if 'http' not in u:
			print(FAIL + "No protocol supplied for host: {0}. Use format http(s)://<host> Skipping...".format(u))
			continue
		try:
			host = Host(store_headers=args['--headers'], follow_redirects=args['--follow-redirects'])
			host.set_url(u)
			hosts.append(host)
			print(SUCCESS + "Adding host to list: {0}".format(host.get_url()))

		except IndexError:  # URL doesn't begin with a protocol
			print(FAIL + "No protocol supplied for host: {0}. Use format http(s)://<host>. Skipping...".format(u))
			continue

	return hosts


def take_screenshot(h, b, args):
	print(SUCCESS + "Taking screenshot for URL: {0}".format(h.get_url()))
	if host.check_host():
		try:
			b.get_url(h.get_url())
			host.set_image(b.get_image())

		except:
			print(FAIL + "Error taking screenshot for host: {0}. Skipping.".format(h.get_url()))
			host.error = True
	else:
		host.error = True


if __name__ == '__main__':
	args = docopt(__doc__, version='JAST - Just Another Screenshot Tool v0.4')

	data = []
	hosts = []
	size = "800x600"
	output_file = args['-o'] + '.html'

	# Check for output file and prompt for overwrite if it already exists
	if os.path.exists(output_file) and os.path.isfile(output_file):
		overwrite = input(WARN + "Output file exists (" + output_file), overwrite? (Y/n): ") or 'y'

		if 'n' in overwrite.lower():
			print(FAIL + "Report not being overwritten, exiting.")
			sys.exit(-1)
		elif 'y' not in overwrite.lower():
			print(FAIL + "Unknown response, exiting.")
			sys.exit(-1)

	print(header)

	# Parse host file/host
	print(SUCCESS + "Processing host(s)...")
	if args['-f']:
		if os.path.exists(args['-f']) and os.path.isfile(args['-f']):
			f = open(args['-f'], 'r')
			data = f.readlines()
			f.close()
		else: # File doesn't exist
			print(FAIL + "Host file not found! Exiting.")
			sys.exit(-1)

	elif args['-u']:
		data = [args['-u']]

	hosts = process_hosts(data, args)

	if len(hosts) == 0:
		print(FAIL + "No hosts processed, exiting...")
		sys.exit(-1)

	print(SUCCESS + "All hosts processed.")

	print(SUCCESS + "Starting browser.")
	browser = Browser(size=args['--size'])
	for host in hosts:
		take_screenshot(host, browser, args)

	print(SUCCESS + "Stopping browser.")
	browser.close()

	print(SUCCESS + "Creating report.")
	report = Report(args)
	report.start()
	for host in hosts:
		report.write_host(host)
	report.finish()

	print(SUCCESS + "Report written to {0}".format(output_file))
