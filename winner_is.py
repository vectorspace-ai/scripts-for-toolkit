from statistics import mean 

file= open("output.txt", 'r')
for line in file.readlines():
	l= [float(i) for i in line.split(",") if i.strip()]

file2= open("output2.txt", 'r')
for line in file2.readlines():
	l2= [float(i) for i in line.split(",") if i.strip()]

average=mean(l)
average2=mean(l2)
print("Average time of 1000 runs")
print("Radek method: ", average, "Magnus method: ", average2)