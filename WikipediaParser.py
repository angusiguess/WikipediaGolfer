"""
wikipediagolfer.py

Created by Angus Fletcher on 2011-06-20.

Copyright (c) 2011 Angus Fletcher

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
from json.encoder import JSONEncoder as jencoder
import re

def process_pages(infile, outfile):
	"""Runs through the xml tree and extracts the titles and links for each
	page, returns a dictionary with keys equal to the pages and a list of
	values which are strings of outgoing links."""
	
	count = 0
	
	encoder = jencoder()
	
	if os.path.exists(outfile):
		print "Error: " + outfile + " already exists."
		return
		
	
	graph_file = open(outfile, 'w')
	
	parser = etree.iterparse(infile, events=('start', 'end'))
	
	graph_values = []
	
	pattern = re.compile("\[\[([^\]\[]+)\]\]", re.UNICODE | re.MULTILINE)
	
	namespace = '{http://www.mediawiki.org/xml/export-0.5/}'
	
	root = None
	
	for event, elem in parser:
		if event == 'start' and root == None:
			root = elem
		elif event == 'end' and elem.tag == namespace + 'title':
			page_title = elem.text
			#This clears bits of the tree we no longer use.
			elem.clear()
		elif event == 'end' and elem.tag == namespace + 'text':
			page_text = elem.text
			#Clear bits of the tree we no longer use
			elem.clear()

			#Now lets grab all of the outgoing links and store them in a list
			key_vals = []
			
			try:
				matches = pattern.finditer(page_text)
			except TypeError:
				matches = pattern.finditer(' ')
			
			for match in matches:
				curr_link = match.group(1)
				#Get the real page name.
				if '|' in curr_link:
					link_index = curr_link.find('|')
					curr_link = curr_link[:link_index]
				key_vals.append(curr_link)
			
			#Eliminate duplicate outgoing links.
			key_vals = set(key_vals)
			key_vals = list(key_vals)
			
			curr_pair = {page_title : key_vals }
			
			graph_file.write(encoder.encode(curr_pair) + '\n')
			
			count += 1
			
			if count % 1000 == 0:
				print str(count) + ' records processed.'
		elif event == 'end' and elem.tag == namespace + 'page':
			root.clear()
	graph_file.close()
	return		
	
def help():
	print """This tool converts a wikipedia export to a JSON graph representation.
	\tUsage: python wikipediaparser.py <export file> <output file>"""		 		

def main(argv=sys.argv):
	if len(sys.argv) is not 3:
		help()
		return 0
	
	
	process_pages(infile=argv[1], outfile=argv[2])
	
	return 0

if __name__ == "__main__":
	sys.exit(main())
