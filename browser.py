#!/usr/bin/env python
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

from alert import FAIL

class Browser:
	def __init__(self, size="800x600"):
		try:
			self._width, self._height = size.split('x')

		except:
			print(FAIL + "Error parsing browser window size, defaulting to 800x600")
			self._width = 800
			self._height = 600

		self._browser = self.start_browser(self._width, self._height)

	def get_url(self, url):
		self._browser.get(url)

	def get_image(self):
		return self._browser.get_screenshot_as_base64()

	@staticmethod
	def start_browser(width, height):
		options = Options()
		options.add_argument('--headless')
		b = Firefox(executable_path='geckodriver', options=options)
		b.set_window_size(width, height)
		b.set_page_load_timeout(30)
		return b

	def close(self):
		self._browser.quit()