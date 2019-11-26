"""By Radek, modified by Magnus
25-11-2019

This script was originally made by Radek, but modified by Magnus. This is basically the original script except
it's just for the first level of depth,to create a cluster single-level graph.
"""

import sys
import csv
import json
import time
import pprint
import operator


start=time.time()


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
delim= "null"
if file_name[:4]=='.csv':
	delim=','
else:
	delim='\t'
with open(file_name) as file:
	csv_reader = csv.reader(file, delimiter=delim)
	headers = next(csv_reader)[1:]
	for row in csv_reader:
		data[row[0]] = [float(x) for x in row[1:]]

def Main():
	result=sorted(get_intersected(root_symbol, data), key=operator.itemgetter('score'), reverse=True)

	with open('output_script1.json', 'w') as outfile:
		json.dump(result, outfile, indent=2)

	pprint.pprint(result)
	end=time.time()
	print("Elapsed time: ", end-start)

	

def get_intersected(symbol, dict, depth=1):
	return [{'root_symbol':symbol, 'cor_symbol':headers[i].strip(), 'score':score, 'depth':depth} for i, score in enumerate(dict[symbol]) if score > SCORE and headers[i].strip()!=symbol]


if __name__ == '__main__':
	Main()