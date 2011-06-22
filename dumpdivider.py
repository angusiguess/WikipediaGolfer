""""
dumpdivider.py

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

def create_skeleton():
	"""
	Create a skeleton document based on a template, returns an ElementTree
	of the base document.
	"""
	new_doc = etree.parse('skeleton.xml')
	return new_doc
	
def write_articles(doc, dump_iter, num_pages):
	"""
	Take a document, a parse iterator from the article, the number of pages you
	want in a dump article.
	"""
	page_elements = ['{http://www.mediawiki.org/xml/export-0.5/}page', '{http://www.mediawiki.org/xml/export-0.5/}title',
	'{http://www.mediawiki.org/xml/export-0.5/}text']
	
	page_count = 0
	
	root = doc.getroot()
	
	for curr_event, curr_elem in dump_iter:
		print str(curr_elem)
		if curr_event == 'end' and curr_elem.tag in page_elements:
			new_elem = root.SubElement(doc, curr_elem, attrib=curr_elem.attrib)
		if curr_elem == '{http://www.mediawiki.org/xml/export-0.5/}page':
			page_count += 1
		if page_count >= num_pages:
			break
	
	


def main():
	dump = etree.iterparse('enwiki-latest-pages-articles.xml')
	newdoc = create_skeleton()
	write_articles(newdoc, dump, 100)
	etree.tostring(newdoc)
	pass


if __name__ == '__main__':
	main()

