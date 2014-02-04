import re
import sys
import os
import pickle
fp=open("/home/shek/Project/Done_code/newoutput","r")
dataln=fp.readlines()


####Code to convert node list from hdfs newoutput folder to node list for neo4j//////input file newoutput
lineb="create n={name='',properties=''};"
fp1=open("/home/shek/Project/Done_code/input1.txt","w");
fp1.write("BEGIN\n")
for line in dataln:
	line1=line.strip()
	linen=line1.split("\t")
 	line2=lineb[0:16]+linen[0]+lineb[16:30]+linen[1]+lineb[30:33]+"\n"
	fp1.write(line2)

####
####Code to convert edgelist for neo4j....working just need right values to input and weight of the relationships


line_e_base="start n1=node:node_auto_index(name=''),n2=node:node_auto_index(name='') create n1-[:{weight:}]->n2;"

pkl_file=open('/home/shek/Project/edge_strength_output.txt','rb')

data1 = pickle.load(pkl_file)

for line in data1:

	line2=line_e_base[0:36]+line[0]+line_e_base[36:69]+line[1]+line_e_base[69:92]+str(line[2])+line_e_base[92:97]+"\n"
	fp1.write(line2)

####
fp1.write("COMMIT")	
fp1.close()
fp.close()
