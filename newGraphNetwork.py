# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 11:54:31 2014

@author: sh
"""
#global definations
import pickle
import nltk
import networkx as nx
import re
import numpy
import shlex

G=nx.DiGraph()  #Directed Graph (GLOBAL)
count=0

SIGMAvsn=3  #valid start node
SIGMAr=4    
GAP=3    

#Function to create graph
def CreateGraph():
    tagger=nltk.data.load('POSTrainedTagger.pickle')
    InputFilePointerNodes=open("/home/shek/my_repo/opnosis/newoutput","r")
    InputNodeData=InputFilePointerNodes.readlines()
    #NODES    
    for DataLineNode in InputNodeData:
        DataLineNode=DataLineNode.strip()
        NodeList=DataLineNode.split("\t")
        ListTaggedName=tagger.tag([NodeList[0]])
        TupleTaggedName=ListTaggedName[0]
        StrTag=str(TupleTaggedName[1])
        YetAnotherTemperoryList=shlex.split(NodeList[1])
        TemperoryList=re.split(',',YetAnotherTemperoryList[0])   #to strip the last comma
        i=0
        FinalList=[] #List containing pri of the node
        while i<len(TemperoryList)-1:
            Temp1=int(re.split('\(',TemperoryList[i])[1]) #to strip '('
            Temp2=int(re.split('\)',TemperoryList[i+1])[0]) #to strio')'
            FinalList.append([Temp1,Temp2])
            i=i+2
        G.add_node(NodeList[0],PRI=FinalList,pos_tag=StrTag)
    
    InputPicklePointerRelationship=open('/home/shek/my_repo/opnosis/edge_strength_output.txt','rb')
    InputPickleData = pickle.load(InputPicklePointerRelationship)

    #RELATIONSHIPS
    for line in InputPickleData:
        G.add_edge(line[0],line[1],weight=line[2])

  
    
#Function to detect valid start node
def VSN(n,data):
    ListValidStart=["I"]
    PIDList=[]
    PIDList=[pid for sid,pid in data]
     
    if(numpy.mean(PIDList)<SIGMAvsn or n in ListValidStart):
        return True
    else:
        return False

#function to detect valid end node
def VEN(n,data):
    ListValidEnd=[".","!","?","yet","but","and"]
    if(n in ListValidEnd):
        return True
    else:
        return False
    

    
def ValidSentence(sentence):
    return False
    
"""
Function to get PRI of neighbour. Used in Traverse function
"""
def getPRI(Node):
    for Nnode,Ndata in G.nodes(data=True):
        if Node == Nnode:
            return Ndata['PRI']


"""
Fuction to find Intersect between PRIoverlap and PRInode to get PRInew
"""
def intersect(PRIoverlap,PRInode):
    #print "This is PRIoverlap",PRIoverlap
    #print "This is PRInode",PRInode    
    newPRI=[]    
    for i in PRIoverlap:
        isid,ipid=i
        for j in PRInode:
            jsid,jpid=j
            if jsid==isid and jpid-ipid>0 and jpid-ipid <= GAP:
                newPRI.append(i)
                break
    
    for i in PRInode:
        isid,ipid=i
        for jsid,jpid in PRIoverlap:
            if jsid==isid and ipid-jpid>0 and ipid-jpid <= GAP:
                newPRI.append(i)
                break
    #print "THis is new PRI:"
    #print newPRI
    #if (len(newPRI)==0):
    #    return PRIoverlap
    #else:
    return newPRI
    
def pathScore(redundancy,length):
    return numpy.log2(length) * redundancy
    
#Function to Traverse and find valid paths
def Traverse(cList,Nnode,score,NodePRI,pathLen,PRIoverlap,sentence,count):
    
    if len(sentence) > 20:
        return
    
    redundancy=len(PRIoverlap)
    if(redundancy>=SIGMAr):
        if(VEN(Nnode,Ndata)):
            if (ValidSentence(sentence)):
                final_score = score/float(len(sentence))
                cList=sentence
                print "THis is the final Sentence------>>>>>", cList            
                return
                #calculate final score
                #add candidate
                
                
    for neighbor in G.successors(Nnode) :
        PRIneighbor=getPRI(neighbor)
        PRInew=intersect(PRIoverlap,PRIneighbor)
        redundancy=len(PRInew)
        if(redundancy>0):  
            #print "This is new PRI",PRInew            
            new_sentence = sentence[:]
            new_sentence.append(neighbor)
            #print "This is the sentence:\n\n",sentence
            newPathLen=pathLen+1
            new_score=score+pathScore(redundancy,len(new_sentence))
            count=count +1
            
            Traverse(cList,neighbor,new_score,PRIneighbor,newPathLen,PRInew,new_sentence,count)

#MAIN
CreateGraph()
for Nnode,Ndata in G.nodes(data=True):   
    
    if(VSN(Nnode,Ndata['PRI'])):
        count=count+1
        #print Ndata
        pathLen=1
        G.nodes()
        score=0
        cList=[]
        sentence = [Nnode]
        NodePRI= Ndata['PRI']
        PRIoverlap=Ndata['PRI']
        
        Traverse(cList,Nnode,score,NodePRI,pathLen,PRIoverlap,sentence,count)
