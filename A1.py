# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 14:35:58 2014

@author: shek
"""

"""
A1-1
"""
from collections import defaultdict
import pickle



def A1(product):
    productPath="/home/shek/my_repo/data/"+product+".txt.data"
    review_files=open(productPath,'r')
    edges = []
    nodes_pri = defaultdict(list)
    for i, line in enumerate(review_files,start=1):
        line = line.strip()
        if not line:
            continue
        words = line.split()
        words2 = words[1:][:]
        words1 = words[:-1]
        bigram = zip(words1, words2)
        edges.extend(bigram)
        for j,word in enumerate(words,start=1):
            nodes_pri[word].append((i,j))

    prifile=open("/home/shek/my_repo/sas",'w')
    for key,value in  nodes_pri.iteritems():
        value=str(value)
        value=value.rstrip(']')
        value=value.lstrip('[')
        value=value.replace(" ","")
        prifile.writelines(key+"\t"+value+"\n")
        
    x=open("/home/shek/my_repo/rel",'w')
    for From,To in edges:
        x.writelines(From+"\t"+To+"\n")

    prifile.close()
    x.close()
    
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
