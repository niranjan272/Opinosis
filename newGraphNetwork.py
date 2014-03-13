# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 11:54:31 2014

@author: sh
"""




#Function to create graph
def CreateGraph():
    tagger=nltk.data.load('POSTrainedTagger.pickle')
    InputFilePointerNodes=open("/home/shek/my_repo/opnosis/newoutput","r")
    InputNodeData=InputFilePointerNodes.readlines()
    for DataLineNode in InputNodeData:
        DataLineNode=DataLineNode.strip()
        NodeList=DataLineNode.split("\t")
        ListTaggedName=tagger.tag([NodeList[0]])
        TupleTaggedName=ListTaggedName[0]
        StrTag=str(TupleTaggedName[1])
        NodeList[1]=NodeList[1].rstrip(',')
        G.add_node(NodeList[0],PRI=NodeList[1],pos_tag=StrTag)
    
    InputPicklePointerRelationship=open('/home/shek/my_repo/opnosis/edge_strength_output.txt','rb')
    InputPickleData = pickle.load(InputPicklePointerRelationship)

    for line in InputPickleData:
        G.add_edge(line[0],line[1],weight=line[2])

  
    
#Function to detect valid start node
def VSN(n,data):
    ListValidStart=["I"]
    PIDList=[]
    PRIstr=data['PRI']
    PIDList=re.findall("(\d{1,}(?=\)))",PRIstr,0)
    PIDList = map(int, PIDList)                    #To convert list of string to list of Intergers  
    if(numpy.mean(PIDList)<3 or n in ListValidStart):
        return 1
    else:
        return 0

#Function to Traverse and find valid paths
def Traverse(cList,Nnode,score,PRI,pos_tag,pathLen):
    print "\n"

import pickle
import nltk
import networkx as nx
import re
import numpy
G=nx.DiGraph()
count=0
CreateGraph()

for Nnode,Ndata in G.nodes(data=True):
    if(VSN(Nnode,Ndata)):
        count=count+1        
        print count
        pathLen=1
        score=0
        cList=[]
        Traverse(cList,Nnode,score,Ndata['PRI'],Ndata['pos_tag'],pathLen)
        print Nnode
        print Ndata
