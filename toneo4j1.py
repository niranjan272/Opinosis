#using Geoff format to import data into neo4j...http://nigelsmall.com/geoff 

import re
import sys
import os
import pickle

InputFilePointerNodes=open("/home/niranjan/project/opnosis/newoutput","r")
InputNodeData=InputFilePointerNodes.readlines()
NodeIdName=""
ListNodeIdvsNodeName=[]
i=1;

####Code to convert node list from hdfs newoutput folder to node list for neo4j........[input file newoutput]
CreateNodeSyntax="""({name:"",properties:''}),"""
OutputFilePointer=open("/home/niranjan/project/opnosis/InputForNeo4j.txt","w");
OutputFilePointer.write("CREATE ")
for DataLineNode in InputNodeData:
	DataLineNode=DataLineNode.strip()
	NodeList=DataLineNode.split("\t")
	NodeIdName="n"+str(i)
	ListNodeIdvsNodeName.append([NodeIdName,NodeList[0]]) #list to store Node Ids of resprective names of nodes
        i=i+1;
 	NodeFinalLineToWrite=CreateNodeSyntax[0:1]+NodeIdName+CreateNodeSyntax[1:8]+NodeList[0]+CreateNodeSyntax[8:22]+NodeList[1]+CreateNodeSyntax[22:26]+"\n"
	OutputFilePointer.write(NodeFinalLineToWrite)

####
####Code to convert edgelist for neo4j....working just need right values to input and weight of the relationships


CreateRelationshipSyntax="""()-[:CONNECTS{weight:}]->(),"""

InputPicklePointerRelationship=open('/home/niranjan/project/opnosis/edge_strength_output.txt','rb')

InputPickleData = pickle.load(InputPicklePointerRelationship)

for line in InputPickleData:
	for Id in ListNodeIdvsNodeName:
		if(Id[1]==line[0]):
			line[0]=Id[0]
			break
	for Id in ListNodeIdvsNodeName:
		if(Id[1]==line[1]):
			line[1]=Id[0]
			break	
	RelFinalLineToWrite=CreateRelationshipSyntax[0:1]+line[0]+CreateRelationshipSyntax[1:21]+str(line[2])+CreateRelationshipSyntax[21:26]+line[1]+CreateRelationshipSyntax[26:28]+"\n"
        #RelFinalLineToWrite=CreateRelationshipSyntax[0:1]+line[0]+CreateRelationshipSyntax[1:20]+str(line[2])+CreateRelationshipSyntax[20:25]+line[1]+CreateRelationshipSyntax[25:27]+"\n"

	OutputFilePointer.write(RelFinalLineToWrite)

####	
OutputFilePointer.close()

#to remove last comma



InputFilePointerNodes.close()
