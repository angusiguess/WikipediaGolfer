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
import re

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
			
			page_text = page_text.replace('\r', '').replace('\n', '')

			#Now lets grab all of the outgoing links and store them in a list
			pattern = '\[\[([^\]\[]+)\]\]'
			
			key_vals = []
			
			for match in re.finditer(pattern, page_text, re.UNICODE):
				curr_link = match.group(1)
				#Get the real page name.
				if '|' in curr_link:
					link_index = curr_link.find('|')
					curr_link = curr_link[:link_index]
				key_vals.append(curr_link)
			
			#Eliminate duplicate outgoing links.
			key_vals = set(key_vals)
			key_vals = list(key_vals)
			
			page_dict[page_title] = key_vals
			
	return page_dict
	
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
	try:
		wikitree = etree.parse(file_name)
	except IOError:
		print 'Cannot parse' + file_name
	
	root = wikitree.getroot()
	
	wiki_graph = process_pages(root)
	
	wiki_graph = strip_edges(wiki_graph)
	
	return 0

if __name__ == "__main__":
	sys.exit(main())
