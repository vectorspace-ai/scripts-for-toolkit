#VERIFIES IF THE PRESENTED DATASET IS A GENUINE CORRELATION MATRIX


import pandas as pd
import sys


file_name= sys.argv[1]

df=pd.read_csv(file_name, index_col=0, header=0)
is_genuine=True
for i in range(len(df.index)):
	for j in range(len(df.columns)):
		if(df.iloc[i][j] != df.iloc[j][i]):
			print("DATASET IS NOT A GENUINE CORRELATION MATRIX")
			print("INDEXES: ", i, j, " DOES NOT HAVE SAME VALUES ON THEIR RESPECTIVE CELLS")
			is_genuine=False
if(is_genuine==True):
	print("DATASET IS A GENUINE CORRELATION MATRIX! :)")
