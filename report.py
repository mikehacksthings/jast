#!/usr/bin/env python
import os
import sys

from alert import FAIL

class Report:
	def __init__(self, args={}):
		self._args = args
		self._report = args['-o']
		self._fd = ''
		self._header = """
		
<!DOCTYPE html>
<html>
	<head>
		<title>JAST Report</title>
		<link href="https://fonts.googleapis.com/css?family=EB+Garamond" rel="stylesheet">
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
		<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
		<style>
			body {
				font-family: "EB+Garamond", sans-serif;
				background-color: #FFF;
			}
			hr {
				width: 50%;
			}
		</style>
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

		"""

	def start(self):
		self._report = self._report + ".html"
		try:
			self._fd = open(self._report, 'w')
			self._fd.write(self._header)
			return
		except OSError:
			print(FAIL + "Failed to create output file: {0}.".format(self._report))
			sys.exit(-1)

	def write_host(self, host):
		host_data = "<div class =\"card mt-4 mb-4 w-75 border\">\n"

		if host.error:
			host_data += "\t\t<div class =\"card-footer\">\n\t\t<p class=\"card-text\"><h4>{0}</h4>\n".format(host.get_url())
			host_data += "\t\t<h5>Error taking screenshot:</h5></p>\n\t\t\t<p>{0}</p>\n\t\t</div>\n\t</div>\n".format(host.error_msg)
			self._fd.write(host_data)
		else:
			host_data += "\t<img class =\"card-img-top\" src=\"data:image/png;base64, {0}\" />\n".format(host.get_image())
			host_data += "\t\t<div class =\"card-footer\">\n\t\t<p class=\"card-text\">"
			host_data += "<h4><a href=\"{0}\" target=\"_blank\">{1}</a></h4></p>\n\t</div>\n".format(host.get_url(), host.get_url())

			self._fd.write(host_data)

			if host.store_headers() is True:
				self._fd.write("<div class=\"table-responsive\"><table class=\"table\" style=\"word-wrap:break-word;\">\n")
				for key, value in host.get_headers().items():
					self._fd.write("\t<tr>\n\t\t<th scope=\"row\" class=\"text-right w-50\">" + key + "</th>\n\t\t<td class=\"text-left w-50\">" + value +"</td>\n\t</tr>\n")
				self._fd.write("</table></div>\n")

		self._fd.write("</div>\n")

	def finish(self):
		self._fd.write(self.footer)
		self._fd.close()
