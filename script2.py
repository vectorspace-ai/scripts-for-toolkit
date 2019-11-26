"""By Radek, modified by Magnus
25-11-2019
This script is a modified version of Radek's featuring a slightly faster depth-algorithm(if you can
call this an algorithm), user-specified amount of branches per node and user specified amount of nodes.
In addition, I have implemented a measure to clean the graph of mirrored duplicates that occur in 
correlation matrices.

I really hope you can all understand my retarded way of explaining. If not, hit me up on Telegram for this
or simply run the script.

TODO: 
-probably make the script load default argument values if no arguments are passed

"""
import sys
import csv
import json
import pprint
import time
import operator

start=time.time()

SCORE = 0.01
if len(sys.argv) != 6:
	print('*****')
	print('Usage: print script.py <symbol> <depth> <branches> <nodes> <file_name>')
	print('Example: python script2.py BTC 3 2 5 dataset.csv')
	print('Note: passing the argument for branches and nodes as 1 gives the max possible amount of nodes and branches')
	print('Passing all numerical arguments as 0 makes the script behave the same as script1.py')
	print('*****')
	exit()
######Please suggest me some proper limits
"""if sys.argv[2]>10 or sys.argv[3]>5 or sys.argv[4]>50:
	print('*****')
	print('Arguments out of range')
	print('depth<10, branches<5, nodes<50')"""

#assign argument values to variables
root_symbol = sys.argv[1]
max_depth = int(sys.argv[2])
branches = int(sys.argv[3])
nodes = int(sys.argv[4])
file_name = sys.argv[5]


#Read the dataset
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



	result = get_intersected(root_symbol, data)
	result = set_depth(result, max_depth)
	result = remove_duplicates(result)
	if branches>0:
		result = set_branches(result, branches)
	else:
		result=sorted(result, key=operator.itemgetter('depth')) 

	if nodes>0:
		result = set_nodes(result, nodes)
	else:
		result=sorted(result, key=operator.itemgetter('depth')) 


	with open('output_script2.json', 'w') as outfile:
		json.dump(result, outfile, indent=2)

	pprint.pprint(result)
	end=time.time()
	print("Elapsed time: ", end-start)

"""------------------------------------------------------------------------------------------------"""

#this function gets all the correlated symbols of the root symbol
def get_intersected(symbol, dict, depth=1):
	return [{'root_symbol':symbol, 'cor_symbol':headers[i].strip(), 'score':score, 'depth':depth} for i, score in enumerate(dict[symbol]) if score > SCORE and headers[i].strip()!=symbol]


def set_depth(result, max_depth):
	#initialize 2 lists containing symbols
	symbols=[]
	covered_symbols=[]
	#this is used for the while loop(subtracted by 1 because first level has already been covered above)
	remainer_depth=max_depth-1
	while remainer_depth>0:
		#removes all symbols previously covered
		symbols=[x for x in symbols if x not in covered_symbols]
		for j in range(len(result)):
			#checking if the symbol in question has already been covered or not
			if(result[j]['cor_symbol'] not in covered_symbols and result[j]['cor_symbol'] not in symbols):
				symbols.append(result[j]['cor_symbol'])
		for name in symbols:
			#performs the same function as with the root symbol
			result[(len(result)):]=(get_intersected(name, data, max_depth-remainer_depth+1))
		remainer_depth-=1
		#updates symbols already covered
		covered_symbols.extend(symbols)

	return result

#removes duplicates because a correlation matrix is mirrored right? Please contribute if there's a better way of doing this
def remove_duplicates(result):
	duplicates=[]
	for i in range(len(result)):
		for j in range(len(result)):
			#long if condition lmao
			if ((result[i]['root_symbol']==result[j]['cor_symbol'] and result[i]['cor_symbol']==result[j]['root_symbol'] or 
				result[i]['root_symbol']==result[j]['root_symbol'] and result[i]['cor_symbol']==result[j]['cor_symbol'] and 
				result[i]['depth']!=result[j]['depth']) and result[i] not in duplicates):
				duplicates.append(result[j])

	return [x for x in result if x not in duplicates]
#limits the amount of branches per depth. May need to work more on this one
def set_branches(result, branches):
	temp=[]
	temp2=[]
	symbol="null"
	result=sorted(result, key=operator.itemgetter('score'), reverse=True)
	result=sorted(result, key=operator.itemgetter('root_symbol', 'depth')) 
	for i in range(len(result)):
		if symbol!=result[i]['root_symbol']:
			symbol=result[i]['root_symbol']
			temp.clear()
			for item in result:
				if item['root_symbol'] == symbol:
					temp.append(item)
			temp=temp[:branches]
			temp2.extend(temp)

	return temp2


#limits amount of nodes by only displaying the top n nodes, prioritizing lower levels of depth
def set_nodes(result, nodes):
	temp=[]
	temp=sorted(result, key=operator.itemgetter('score'), reverse=True)
	return sorted(temp, key=operator.itemgetter('depth'))[:nodes]

if __name__ == '__main__':
	Main()