"""
####Program to calculate strength of edges in graph
####using exception because some values in data are missing which are causing array out of bound exceptions
###example values...they have only one value and hence cause exception when accesing the second value
#['on']
#['portable']
#['portable']
#['proof']
#['quality']
###

###DONE :P
"""
import pickle
arr=[]
input_file=open("/home/shek/my_repo/rel","r")
data_line=input_file.readlines()

output_file=open("/home/shek/my_repo/edge_strength_output.txt","w")
for line in data_line:
	flag=0
	line=line.strip()
	line=line.split('\t')
	if not arr:
		try:
  			arr.append([line[0],line[1],1])
		except IndexError:
			print line
			continue
	for index in range(0,(len(arr))):
		try:
			if(line[0]==arr[index][0] and line[1]==arr[index][1]):
				arr[index][2]=arr[index][2]+1
				flag=1
		except IndexError:
			print line
			continue	
	if(flag==0):
		try:
  			arr.append([line[0],line[1],1])
		except IndexError:
			print line
			continue	 

pickle.dump(arr, output_file)

#output_file.write("\n".join(str(elem) for elem in arr))









