#!/usr/bin/env python
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

from alert import ALERT, SUCCESS

class Browser:
	def __init__(self, size="800x600"):
		try:
			self._width, self._height = size.split('x')

		except:
			print(AKERT + "Error parsing browser window size, defaulting to 800x600")
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