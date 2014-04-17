# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 11:54:31 2014

@author: sh
"""
#global definations
import pickle
import networkx as nx
import nltk
import re
import numpy
import shlex
import A1
import sys
from multiprocessing import Pool

"""
Global declarations
"""

G=nx.DiGraph()  #Directed Graph (GLOBAL)
count=0
SIGMAvsn=5  #valid start node
SIGMAr=2    
GAP=2    #difference in pid

"""
Functions :
"""
#Function to create graph
def CreateGraph():
    tagger=nltk.data.load('POSTrainedTagger.pickle')
    InputFilePointerNodes=open("/home/shek/my_repo/sas","r")
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
    
    #print G.nodes()
    InputPicklePointerRelationship=open('/home/shek/my_repo/edge_strength_output.txt','rb')
    InputPickleData = pickle.load(InputPicklePointerRelationship)

    #RELATIONSHIPS
    for line in InputPickleData:
        G.add_edge(line[0],line[1],weight=line[2])

  
#Function to detect valid start node
def VSN(node,data):
    ListValidStart=["I"]
    PIDList=[]
    PIDList=[pid for sid,pid in data]
     
    if(numpy.mean(PIDList)<SIGMAvsn or node in ListValidStart):
        return True
    else:
        return False

#function to detect valid end node
def VEN(node):
    ListValidEnd=[".","!","?"]
    if(node in ListValidEnd):
        return True
    else:
        return False

#function to get pos tag
def getPosTag(node):
    for Nnode,Ndata in G.nodes(data=True):
        if(Nnode==node):
            StrPosTag=Ndata['pos_tag']
            return StrPosTag


#Function to Validate sentence    
def ValidSentence(sentence):
    
    sent=[]    
    for i in sentence:
        pos_tag=getPosTag(i)
        sent=sent[:]
        sent.append(i+'/'+pos_tag)
    last=sent[-1]
    w,t=last.split("/")
    if t in set(["TO", "VBZ", "IN", "CC", "WDT", "PRP", "DT", ","]):
        return False
    sent= " ".join(sent)
    if re.match(".∗(/NN)+.∗(/VB)+.∗(/JJ)+.∗", sent):
        return True
    elif re.match(".*(/PRP|/DT)+.*(/VB)+.*(/RB|/JJ)+.*(/NN)+.*", sent):
        return True
    elif re.match(".*(/JJ)+.*(/TO)+.*(/VB).*", sent):
        return True
    elif re.match(".*(/RB)+.*(/IN)+.*(/NN)+.*", sent):
        return True
    else:
        return False
    return False
"""
Function to get PRI of neighbour. Used in Traverse function
"""
def getPRI(node):
    for Nnode,Ndata in G.nodes(data=True):
        if node == Nnode:
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
   # print "\nTHis is new PRI:"
    #print newPRI
    return newPRI
    
#Function to calculate pathscore
def pathScore(redundancy,length):
    return numpy.log2(length) * redundancy


#Function to determine if node is collapsible
def collapsible(node):
    pos_tag=getPosTag(node)
    if (pos_tag=='VB' or pos_tag=='IN'):
        return True
    else:
        return False

def removeDuplicates(temp,final=False):    
    if not temp:
        return
    if not final:
        compareValue=0.7
    if final:
        compareValue=0.5
    
    newTemp={}
   
    for key,value in temp.iteritems():
       for nkey,nvalue in temp.iteritems():
           flag=False
           if (jaccard(key,nkey)>=compareValue):
               continue
           else:
               """
               making sure sentence is not in list, then comparing it with sentences already
               present in the list and removing it if it matches a sentence already in the final list
               """
               if nkey not in newTemp:
                   if newTemp:
                       for i in newTemp:
                           if(jaccard(i,nkey)>=compareValue):
                               flag=True
                       if not flag:
                           newTemp[nkey]=nvalue
                   else:
                        newTemp[nkey]=nvalue
    if final:
       # print "___________final___________"
        return newTemp
    if not newTemp:
        #print "___________not____final___________"
        v=list(temp.values()) #list of scores of sentences
        newTemp[list(temp.keys())[v.index(max(v))]]=max(v) # [v.index(max(v)) will return index of score having maximum value use this to get the sentence from the list of sentecnces
    return newTemp

    
    
#Function to Traverse and find valid paths
def Traverse(cList,Nnode,score,nodePRI,PRIoverlap,sentence,count,AND):
    
    if len(sentence) > 20:
        return
    
    redundancy=len(PRIoverlap)
    if(redundancy>=SIGMAr):
        if(VEN(Nnode)):
            if (ValidSentence(sentence)):
                finalScore = score/float(len(sentence))
                cList[" ".join(sentence)]=finalScore
                #print "\n\nThis is the sentence formed----->>>",sentence            
                return
                
                
    for neighbor in G.successors(Nnode):
        if AND:
            return

        #print "\n THis is neighbour====>", neighbor       
        
        #print "\nThis is overallPRI----> ", PRIoverlap     
        PRIneighbor=getPRI(neighbor)
       # print "\nThis is PRI of neighbour----> ", PRIneighbor           
        PRInew=intersect(PRIoverlap,PRIneighbor)
        redundancy=len(PRInew)
        if(redundancy>0):  
            new_sentence = sentence[:]
            new_sentence.append(neighbor)
            new_score =score+pathScore(redundancy,len(new_sentence))
            if (neighbor==Nnode):
                
                
                Traverse(cList,neighbor,new_score,PRIneighbor,PRInew,new_sentence,count,True)
            else:
            
                Traverse(cList,neighbor,new_score,PRIneighbor,PRInew,new_sentence,count,False)


#function to calculate jaccard index
def jaccard(a, b):
    a=set(a.split())
    b=set(b.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


def xyz(ListOfARGS):
    cList=ListOfARGS[0]
    Nnode=ListOfARGS[1]
    score=ListOfARGS[2]
    nodePRI=ListOfARGS[3]
    PRIoverlap=ListOfARGS[4]
    sentence=ListOfARGS[5]
    count=ListOfARGS[6]
    AND=ListOfARGS[7]
    Traverse(cList,Nnode,score,nodePRI,PRIoverlap,sentence,count,AND)
    return cList

def removeExtras(Sent):
    reword = Sent.split()
    m=0   
    for i in reword:
        if i=='as':
            m=m+1
        if m==2:
            return
    return Sent
            
    
    
"""
Main

"""
  
A1.A1(sys.argv[1])  
CreateGraph()


"""
Parameters for the traverse function:
    1. A list that will contain the sentence when it is(the sentence) found to be valid.
    2. Current node that is under consideration
    3. Redundancy score of the sentence SO FAR
    4. PRI information of the node under consideration
    5. overlap of PRI or the overall pri covered by the sentence
    6. List containing node that will form a sentence
    7. Count...temp parameter to control iterations  
"""



candidateSummaries={}
vsnDIC=[]

for Nnode,Ndata in G.nodes(data=True):   
    
    if(VSN(Nnode,Ndata['PRI'])):
        #print "THis is valid start node==>>", Nnode        
        count=count+1        
        pathLen=1  #pathlen removed from parameters coz it can be calculated by using the len of list function
        G.nodes()
        score=0
        cList={}
        sentence = [Nnode]
        NodePRI= Ndata['PRI']
        PRIoverlap=Ndata['PRI']
        vsnDIC.append([cList,Nnode,score,NodePRI,PRIoverlap,sentence,count,False])
         
p = Pool(3)
results= p.map(xyz,vsnDIC)

p.close()
p.join()

candidateSummaries={}

p=Pool(3)


candidateSummaries=p.map(removeDuplicates,results)
p.close()
p.join()

final={}

for key in candidateSummaries:
    if key:
        for keySent,scoreValue in key.iteritems():
            final[keySent]=scoreValue

            
final=removeDuplicates(final,True)



res = list(sorted(final, key=final.__getitem__, reverse=True))            
p=Pool(3)


res=p.map(removeExtras,res)
p.close()
p.join()
res=[i for i in res if i!= None]
print "This is the final summary \n",res[:5]      
