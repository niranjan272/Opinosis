# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 14:35:58 2014

@author: shek
"""

"""
A1-1
"""
import networkx as nx
from collections import defaultdict

G=nx.DiGraph()

review_files=open("/home/shek/my_repo/speed_windows7.txt.data",'r')

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
        nodes_pri[word].append([i,j])


for key,value in  nodes_pri.iteritems():
    G.add_node(key,PRI=value)

for bigram in edges:
    G.add_edge(bigram[0],bigram[1])


print G.nodes(data=True)
print G.edges()