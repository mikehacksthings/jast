#!/usr/bin/env python
import os
import sys

from alert import ALERT

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
			pass
		else:
			try:
				os.mkdir(self._report_dir)
				os.mkdir(self._report_dir + "/screenshots")
				return
			except OSError:
				print(ALERT + "Failed to create {0}.".format(self._report_dir))
				sys.exit(-1)

	def start(self):
		f = open(self._report_dir + "/report.html", 'w')
		f.write(self._header)
		f.close()

		f = open(self._report_dir + "/style.css", 'w')
		f.write(self.style)
		f.close()

	def write_host(self, host):
		host_data = "<div class =\"card mt-4 mb-4 w-75 border\">\n"

		if host.error:
			host_data += "\t\t<div class =\"card-footer\">\n\t\t<p class=\"card-text\"><h4>{0}</h4>\n".format(host.get_url())
			host_data += "\t\t<h5>Error taking screenshot:</h5></p>\n\t\t\t<p>{0}</p>\n\t\t</div>\n\t</div>\n".format(host.error_msg)
			f = open(self._report_dir + "/report.html", 'a')
			f.write(host_data)
		else:
			host_data += "\t<img src=\"{0}\" class =\"card-img-top\" />\n".format(host.get_ss_filename())
			host_data += "\t\t<div class =\"card-footer\">\n\t\t<p class=\"card-text\">"
			host_data += "<h4><a href=\"{0}\" target=\"_blank\">{1}</a></h4></p>\n\t</div>\n".format(host.get_url(), host.get_url())

			f = open(self._report_dir + "/report.html", 'a')
			f.write(host_data)

			if host.store_headers() is True:
				f.write("<table class=\"table table-responsive\" style=\"word-wrap:break-word;\">\n")
				for key, value in host.get_headers().items():
					f.write("\t<tr>\n\t\t<th scope=\"row\" class=\"text-right w-50\">" + key + "</th>\n\t\t<td class=\"text-left w-50\">" + value +"</td>\n\t</tr>\n")
				f.write("</table>\n")

		f.write("</div>\n")
		f.close()

	def finish(self):
		f = open(self._report_dir + "/report.html", 'a')
		f.write(self.footer)
		f.close()
