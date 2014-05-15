# -*- coding: utf-8 -*-
"""
Created on Thu May 15 11:17:08 2014

@author: shek
"""
from urllib2 import urlopen
from json import load
import pickle
api_key="bcpmsnrrfrbce3nm594xj7y6"
product=raw_input("Product:")
f=open('/home/shek/my_repo/skuDATABASE.pickle','rb')
database=pickle.load(f)
sku_pro=database[product]
print sku_pro
url="http://api.remix.bestbuy.com/v1/reviews(sku="+sku_pro+")?show=comment&apiKey="+api_key+"&format=json"
response=urlopen(url)
i=load(response)
for j in i['reviews']:
    print j['comment']
