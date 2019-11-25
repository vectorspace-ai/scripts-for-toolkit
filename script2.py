"""By Radek, modified by Magnus
25-11-2019
I use Pandas for dealing with the dataset beacuse I am more fluent in Pandas than the more native
native way of dealing with .csv files. The public script can probably revert back to this for the reading
of the dataset and the get_intersected() function. What I have worked on is to make the depth processing
part of the script work.
One "notable tweak I did was to include the root symbol AND the correlated symbol in each dict entry,
so pairing them together in a graph would be easier. If it's possible to do it without this....
well...more data is usually always better.
I will also try to make it so that a user can limit the branches, where only the top n branches(n being
the number branches desired to be displayed) are displayed.
This is on hold, because the current issue to me is that the script has a problem properly caluculating the
current depth level it is currently in for some reason. Thus it produces wrong depth keys in the dictionary
entries. My plan is to use the depth keys to iterate through each dict entry depending on the depth
and then remove the entries within a specific depth that doesn't fall within the top n scores.

I really hope you can all understand my retarded way of explaining. If not, hit me up on Telegram for this
or simply run the script.
In addition, the last thing Kasian wanted for this script would be to limit the amount of nodes.
I think this will be easy to implement. Just sort all the dict entries by score, then keep those that are
in the top n(n here again being the max number of nodes desired to be displayed)
Of course I could be wrong on all of this, and you guys know of a better way to do it. 
"""
import sys
import pip
import pandas as pd
import json

SCORE = 0.01

if len(sys.argv) != 5:
	print('*****')
	print('Usage: print script.py <symbol> <depth> <branches> <file_name>')
	print('Example: python script.py abc 3 2 test.csv')
	print('*****')
	exit()

root_symbol = sys.argv[1]
max_depth = int(sys.argv[2])
branches = int(sys.argv[3])
file_name = sys.argv[4]

#this reads the dataset(.csv format) to a 2D list
df=pd.read_csv(file_name, index_col=0)

def get_intersected(symbol, df, depth=1, branches=1):
	result=[]
	for index, i in enumerate(df.columns):
		if df.loc[i][symbol] > SCORE:
			result.append({'root_symbol':symbol, 'cor_symbol':df.columns[index], 'score':df.loc[symbol][i], 'depth':depth, 'branches':branches})
	return result

result = get_intersected(root_symbol, df, branches)


if max_depth > 1:
	#initialize 2 lists containing symbols
	symbols=[]
	covered_symbols=[]

	#this is used for the while loop
	remainer_depth=max_depth

	while remainer_depth>0:
		#removes all symbols previously covered
		symbols=[x for x in symbols if x not in covered_symbols]

		for j in range(len(result)):
			#checking if the symbol in question has already been covered or not
			if(result[j]['cor_symbol'] not in covered_symbols and result[j]['cor_symbol'] not in symbols):
				symbols.append(result[j]['cor_symbol'])

		for name in symbols:
			#performs the same function as with the root symbol
			result[(len(result)):]=(get_intersected(name, df, max_depth-remainer_depth+1, branches))
		remainer_depth-=1

		#updates symbols already covered
		covered_symbols.extend(symbols)

if branches > 1:


with open('output.json', 'w') as outfile:
	json.dump(result, outfile)

import pprint
pprint.pprint(result)