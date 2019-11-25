import sys
import csv
import json

SCORE = 0.01

if len(sys.argv) != 3:
	print('*****')
	print('Usage: print script.py <symbol> <depth> <file_name>')
	print('Example: python script.py abc test.csv')
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
	return [{'symbol':headers[i], 'score':score, 'depth':depth} for i, score in enumerate(dict[symbol]) if score > SCORE]

result = get_intersected(root_symbol, data)

	
with open('output.json', 'w') as outfile:
	json.dump(result, outfile)

import pprint
pprint.pprint(result)