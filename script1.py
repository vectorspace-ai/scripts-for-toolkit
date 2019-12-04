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


SCORE = 0.0001

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
if file_name[-4:]=='.csv':
	delim=','
elif file_name[-4:]=='.tsv':
	delim='\t'
else:
	print('*****')
	print('ERROR: Passed dataset is not a supported file. Use Comma-Seprated Values(.csv) or Tab-Seperated Values(.tsv) files')
	print('*****')
	exit()

with open(file_name) as file:
	csv_reader = csv.reader(file, delimiter=delim)
	headers = next(csv_reader)[1:]
	for row in csv_reader:
		data[row[0]] = [float(x) for x in row[1:]]

def Main():
	try:
		result=sorted(get_intersected(root_symbol, data), key=operator.itemgetter('score'), reverse=True)
	except:
		"""-------------Windows 10----------------"""
		"""Something Happened"""
		#Something Happened
		print('*****')
		print("ERROR: The dataset is of an invalid format or the symbol was not found")
		print('*****')
		exit()


	result=sorted(sorted(result, key=operator.itemgetter('score'), 
		reverse=True), key=operator.itemgetter('depth', 'root_symbol')) 

	array=list(map(operator.itemgetter('root_symbol', 'cor_symbol'), result)) 


	pprint.pprint(result)
	print("Nodes: ", len(result))

	save_results(array, "output/output.json")
	save_results(result, "output/output_full.json")
	end=time.time()
	print("Elapsed time: ", end-start)

def get_intersected(symbol, dict, depth=1):
	return [{'root_symbol':symbol, 'cor_symbol':headers[i].strip(), 'score':score, 'depth':depth} for i, score in enumerate(dict[symbol]) if score > SCORE and headers[i].strip()!=symbol]

def save_results(list, name):
	with open(name, 'w') as outfile:
		json.dump(list, outfile, indent=2)

if __name__ == '__main__':
	Main()