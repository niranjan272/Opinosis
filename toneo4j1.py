#using Geoff format to import data into neo4j...http://nigelsmall.com/geoff 

import re
import sys
import os
import pickle

InputFilePointerNodes=open("/home/shek/my_repo/newoutput","r")
InputNodeData=InputFilePointerNodes.readlines()


####Code to convert node list from hdfs newoutput folder to node list for neo4j........[input file newoutput]

CreateNodeSyntax="({name='',properties=''})"
OutputFilePointer=open("/home/shek/my_repo/input1.txt","w");
for DataLineNode in InputNodeData:
	DataLineNode=DataLineNode.strip()
	NodeList=DataLineNode.split("\t")
 	NodeFinalLineToWrite=CreateNodeSyntax[0:1]+NodeList[0]+CreateNodeSyntax[1:8]+NodeList[0]+CreateNodeSyntax[8:22]+NodeList[1]+CreateNodeSyntax[22:25]+"\n"
	OutputFilePointer.write(NodeFinalLineToWrite)

####
####Code to convert edgelist for neo4j....working just need right values to input and weight of the relationships


CreateRelationshipSyntax="""()-[:CONNECTS{"weight":}]->()"""

InputPicklePointerRelationship=open('/home/shek/my_repo/edge_strength_output.txt','rb')

InputPickleData = pickle.load(InputPicklePointerRelationship)

for line in InputPickleData:

	RelFinalLineToWrite=CreateRelationshipSyntax[0:1]+line[0]+CreateRelationshipSyntax[1:23]+str(line[2])+CreateRelationshipSyntax[23:28]+line[1]+CreateRelationshipSyntax[28:29]+"\n"
	OutputFilePointer.write(RelFinalLineToWrite)

####	
OutputFilePointer.close()
InputFilePointerNodes.close()
