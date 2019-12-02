# scripts-for-toolkit
:)<br/>
The scripts automatically detect if the file is .csv or .tsv(aslong as the file has the extension) and uses the appropiorate delimiter<br/>

FOR SCRIPT1.PY<br/>
Usage: python script.py [symbol] [file_name] <br/>
Example: python script1.py BTC dataset.csv<br/>

FOR SCRIPT2.PY<br/>
Usage: python script.py [symbol] [depth] [branches] [nodes] [min_score] [file_name]<br/>
Example: python script2.py BTC 3 2 5 0.01 dataset.csv<br/>
Note: passing the argument for branches and nodes as 0 gives the max possible amount of nodes and branches<br/>
Passing all numerical arguments as 0 makes the script behave the same as script1.py<br/>