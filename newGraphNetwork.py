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
def VSN(node,data):
    ListValidStart=["I"]
    PIDList=[]
    PIDList=[pid for sid,pid in data]
     
    if(numpy.mean(PIDList)<SIGMAvsn or node in ListValidStart):
        return True
    else:
        return False

#function to detect valid end node
def VEN(node,data):
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
    """
    CC Coordinating conjunction
    CD Cardinal number
    DT Determiner
    IN Preposition or subordinating conjunction
    JJ Adjective
    NN Noun, singular or mass
    PRP Personal pronoun
    RB Adverb   
    VB Verb, base form
    VBZ Verb, 3rd person singular present
    WDT Wh­determiner
    TO to
    """    
    sent=[]    
    for i in sentence:
        pos_tag=getPosTag(i)
        sent=sent[:]
        sent.append(i+'/'+pos_tag)
    last=sent[-1]
    w,t=last.split("/")
    if t in set(["TO", "VBZ", "IN", "CC", "WDT", "PRP", "DT", ","]):
        return False
    sent=" ".join(sent)
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
"""
msdsa,;sda
"""
def intersection_sim(can1, can2):
    set1 = set(can1.split())
    set2 = set(can2.split())

    return float(len(set1.intersection(set2)))/len(set1.union(set2))

def removeDuplicates(temp):
   
    newTemp={}
    flag=False
    for key,value in temp.iteritems():
       for nkey,nvalue in temp.iteritems():
           if (jaccard(key,nkey)>=0.7):
               continue
           else:
               """
               making sure sentence is not in list, then comparing it with sentences already
               present in the list and removing it if it matches a sentence already in the final list
               """
               if nkey not in newTemp:
                   if newTemp:
                       for i in newTemp:
                           if(jaccard(i,nkey)>=0.7):
                               flag=True
                       if not flag:
                           newTemp[nkey]=nvalue
                   else:
                        newTemp[nkey]=nvalue
    if not newTemp:
        v=list(temp.values()) #list of scores of sentences
        newTemp[list(temp.keys())[v.index(max(v))]]=max(v) # [v.index(max(v)) will return index of score having maximum value use this to get the sentence from the list of sentecnces
    return newTemp
    
# Function to calculate average path score...for collapse function        
def averagePathScore(temp):
    return numpy.mean(temp.values())
    
    
    
def Stich(ccAnchor,cc):
    if len(cc) == 1:
        return cc.keys()[0]
    return " xx ".join(cc.keys())
    sents = cc.keys()
    anchor_str = " ".join(ccAnchor)
    anchor_len = len(anchor_str)
    sents = [e[anchor_len:] for e in sents]
    sents = [e for e in sents if e.strip() != "./." and e.strip() != ",/,"]
    s = anchor_str + " xx " + " AND ".join(sents)
    return s + " ."
    
#Function to Traverse and find valid paths
def Traverse(cList,Nnode,score,NodePRI,PRIoverlap,sentence,count,collapsed):
    
    if len(sentence) > 20:
        return
    
    redundancy=len(PRIoverlap)
    if(redundancy>=SIGMAr):
        if(VEN(Nnode,Ndata)):
            if (ValidSentence(sentence)):
                finalScore = score/float(len(sentence))
                cList[" ".join(sentence)]=finalScore
                #print "\n\nThis is the sentence formed----->>>",sentence            
                return
                
                
    for neighbor in G.successors(Nnode) :
        #print "\n THis is neighbour====>", neighbor       
        
        #print "\nThis is overallPRI----> ", PRIoverlap     
        PRIneighbor=getPRI(neighbor)
       # print "\nThis is PRI of neighbour----> ", PRIneighbor           
        PRInew=intersect(PRIoverlap,PRIneighbor)
        redundancy=len(PRInew)
        if(redundancy>0):  
            new_sentence = sentence[:]
            new_sentence.append(neighbor)
            new_score=score+pathScore(redundancy,len(new_sentence))
#            if collapsible(neighbor) and not collapsed:
#                ccAnchor=new_sentence
#                anchorScore=new_score + pathScore(redundancy, len(new_sentence)+1)
#                temp={}
#                for vx in G.successors(neighbor):
#                    vxPRI=getPRI(neighbor)
#                    vxNewPRI= intersect(PRInew,vxPRI)
#                    vxSentence = new_sentence[:]
#                    vxSentence.append(vx)
#                    Traverse(temp,vx,anchorScore,vxPRI,vxNewPRI,vxSentence,count,True)
#                    if temp:     
#                        temp=removeDuplicates(temp)
#                        ccPathScore = averagePathScore(temp)
#                        finalScore = float(anchorScore)/len(new_sentence) + ccPathScore
#                        StichedSent=Stich(ccAnchor,temp)
#                        #print "This is StichedSent--->",StichedSent
#                        cList[StichedSent]=finalScore
#            else:
            Traverse(cList,neighbor,new_score,PRIneighbor,PRInew,new_sentence,count,False)
                    

#function to calculate jaccard index
def jaccard(a, b):
    a=set(a.split())
    b=set(b.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))

"""
Main

"""
    
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
        Traverse(cList,Nnode,score,NodePRI,PRIoverlap,sentence,count,False)
        if cList:
            TempList=removeDuplicates(cList)
            print TempList