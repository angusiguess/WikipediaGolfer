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

def process_pages(filename):
	"""Runs through the xml tree and extracts the titles and links for each
	page, returns a dictionary with keys equal to the pages and a list of
	values which are strings of outgoing links."""
	
	count = 0
	
	encoder = jencoder()
	
	graph_file = open('graphfile.txt', 'w')
	
	parser = etree.iterparse(filename)
	
	graph_values = []
	
	pattern = re.compile("\[\[([^\]\[]+)\]\]", re.UNICODE | re.MULTILINE)
	
	namespace = '{http://www.mediawiki.org/xml/export-0.5/}'
	
	for event, elem in parser:
		if event == 'end' and elem.tag == namespace + 'title':
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
			elem.clear()
	graph_file.close()
	return
	
def strip_edges(graph):
	"""Given a graph in the form of a dictionary with key being the vertex name
	and vertices being a list of edges, strip out any edges that don't correspond
	to an existing vertex"""
	
	list_keys = graph.keys()
	
	#Go through the values and cut out the ones that don't correspond to keys
	for curr_key in list_keys:
		values = graph[curr_key]
		#This filter expression should do nicely
		values = [curr_value for curr_value in values if curr_value in list_keys]
		graph[curr_key] = values
		
	return graph				
			 		

def main(argv=None):
	process_pages('enwiki-latest-pages-articles.xml')
	
	#wiki_graph = strip_edges(wiki_graph)
	
	print wiki_graph
	
	return 0

if __name__ == "__main__":
	sys.exit(main())
