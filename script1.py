"""By Radek, modified by Magnus
25-11-2019

This script was originally made by Radek, but modified by Magnus. This is basically the original script except
it's just for the first level of depth,to create a cluster single-level graph.
"""

import sys
import csv
import json

SCORE = 0.01

if len(sys.argv) != 3:
	print('*****')
	print('Usage: print script.py <symbol> <file_name>')
	print('Example: python script1.py BTC dataset.csv')
	print('*****')
	exit()

root_symbol = sys.argv[1]
file_name = sys.argv[2]

headers = []
data = {}
with open(file_name) as file:
	csv_reader = csv.reader(file, delimiter=',')
	headers = next(csv_reader)[1:]
	for row in csv_reader:
		data[row[0]] = [float(x) for x in row[1:]]

def get_intersected(symbol, dict, depth=1):
	return [{'root_symbol':symbol, 'cor_symbol':headers[i], 'score':score, 'depth':depth} for i, score in enumerate(dict[symbol]) if score > SCORE and headers[i]!=symbol]

result = get_intersected(root_symbol, data)

	
with open('output_script1.json', 'w') as outfile:
	json.dump(result, outfile)

import pprint
pprint.pprint(result)