#!/usr/bin/env python
# encoding: utf-8
"""
WikipediaParser.py

Created by Angus Fletcher on 2011-06-25.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys
import os
from xml.etree import ElementTree as etree
import re
import unittest


class WikipediaParser:
	"""
	A parser to iterate over a wikipedia dump file downloaded from
	http://en.wikipedia.org/wiki/Wikipedia:Database_download and extract the
	title and a list of links that appear in the wikipedia article as a 
	key/value pair.
	"""
	def __init__(self):
		pass
	
	def __init__(self, filename):
		"""
		Given the filename, create a parser we can use to iterate over the
		export file.
		"""
		self.parser = etree.iterparse(filename)
		
	def __iter__(self):
		



class WikipediaParserTests(unittest.TestCase):
	def setUp(self):
		pass
		


if __name__ == '__main__':
	unittest.main()