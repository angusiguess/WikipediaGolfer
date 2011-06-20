"""
wikipediagolfer.py

Created by Angus Fletcher on 2011-06-20.

Copyright (c) <year> <copyright holders>

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
from xml.etree import ElementTree as etree

#temporary file hardcoded
file_name = 'Wikipedia-dump.xml'

def process_pages(root):
	'''Runs through the xml tree and extracts the titles and links for each
	page, returns a dictionary with keys equal to the pages and a list of
	values which are strings of outgoing links.'''
	page_dict = {}
	
	#Rip through the pages to process what we need.
	for child in root:
		if child.tag == '{http://www.mediawiki.org/xml/export-0.5/}page':
			page_title = child.find('{http://www.mediawiki.org/xml/export-0.5/}title').text
			#Right now we should pick one rev and use it, the dumps have only one so we can just get it
			page_revision = child.find('{http://www.mediawiki.org/xml/export-0.5/}revision')
			page_text = page_revision.find('{http://www.mediawiki.org/xml/export-0.5/}text').text
			
		

def main(argv=None):
	try:
		wikitree = etree.parse(file_name)
	except IOError:
		print 'Cannot parse' + file_name
	
	root = wikitree.getroot()
	
	process_pages(root)
	
		
	
	return 0

if __name__ == "__main__":
	sys.exit(main())
