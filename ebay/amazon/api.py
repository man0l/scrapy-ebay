#!/usr/bin/python
import csv
from amazonproduct import API
import re
from time import sleep
import pprint

filename = '../spiders/ebay_details.csv'
p = re.compile("\d+")

def get_upc(upc):
  api = API(locale='us')
  response = api.item_lookup(upc, SearchIndex="Blended", IdType="UPC")
  
  for item in response.Items.Item:
    print item.ASIN    


with open(filename, 'r') as csvfile:
	reader = csv.reader(csvfile, delimiter=",")
	i = 0
	for row in reader:          
	  if i > 0:
   	    if row[3] and p.match(row[3]) :
  	      upc = row[3]
	      print upc   
                 
	      get_upc(upc) 
          i += 1 
          sleep(1)   
          
		  

csvfile.close()		
