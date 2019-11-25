import sys
import csv
import json

SCORE = 0.01

if len(sys.argv) != 4:
	print('*****')
	print('Usage: print script.py <symbol> <depth> <file_name>')
	print('Example: python script.py abc 3 test.csv')
	print('*****')
	exit()

root_symbol = sys.argv[1]
max_depth = int(sys.argv[2])
file_name = sys.argv[3]

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

if max_depth > 1:
	stack = [result]
	while(len(stack)>0):
		x = stack.pop(0)
		for child in x:
			new_depth = child['depth'] + 1
			if new_depth <= max_depth:
				child['children'] = get_intersected(child['symbol'], data, new_depth)
				stack.append(child['children'])

with open('output.json', 'w') as outfile:
	json.dump(result, outfile)

import pprint
pprint.pprint(result)