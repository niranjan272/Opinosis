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
    ms=data['PRI']    
    return 1

#Function to Traverse and find valid paths
def Traverse(cList,Nnode,score,PRI,pos_tag,pathLen):
    print "Hello"

import pickle
import nltk
import networkx as nx

G=nx.DiGraph()
CreateGraph()

for Nnode,Ndata in G.nodes(data=True):
    if(VSN(Nnode,Ndata)):
        pathLen=1
        score=0
        cList=[]
        Traverse(cList,Nnode,score,Ndata['PRI'],Ndata['pos_tag'],pathLen)

