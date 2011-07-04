#!/usr/bin/env python
# encoding: utf-8
"""
benford.py

Created by Angus Fletcher on 2011-06-29.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import json

#For commas in numbers
import locale


def main():
	benford_dict = {}
	counter = 0
	maxvalue = 0
	minvalue = sys.maxint
	
	jdecoder = json.JSONDecoder()
	
	benford_file = open('benford_dataset.txt')
	
	for curr_line in benford_file:
		record = jdecoder.decode(curr_line)
		links_count = record.values()[0]
		first_digit = str(links_count)[0]
		if first_digit in benford_dict:
			benford_dict[first_digit] += 1
		elif first_digit == '0':
			pass
		else:
			benford_dict[first_digit] = 1
		
		
		if links_count < minvalue:
			minvalue = links_count
			
		if links_count > maxvalue:
			maxvalue = links_count
		
		counter += 1
	
	keys = benford_dict.keys()
	
	keys.sort()
	
	print '{'
	
	print '\t"values": {'
	
	for key in keys:
		percentage = float(benford_dict[key]) / counter * 100
		formatted_output = '\t\t"%d": "%.2f"' % (int(key), percentage)
		if key != keys[-1]:
			formatted_output += ','
		print formatted_output
		
	print '\t},'
	
	print '\t"%s": "%d",' % ('num_records', counter)
	print '\t"%s": "%d",' % ('min_value', minvalue)
	print '\t"%s": "%d",' % ('max_value', maxvalue)
	print '\t"%s": "%s"' % ('source', 'http://en.wikipedia.org/wiki/Wikipedia:Database_download')
	
	print '}'
		
	
	pass


if __name__ == '__main__':
	main()

