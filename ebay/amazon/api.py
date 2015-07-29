#!/usr/bin/python
import csv
from amazonproduct import API

filename = '../spiders/ebay_details3.csv'


def get_upc(upc):
  api = API(locale='us')
  response = api.item_lookup(upc, SearchIndex="Blended", IdType="UPC")
  print response
  #for item in response.Items.Item:
  #  print item


with open(filename, 'r') as csvfile:
	reader = csv.reader(csvfile, delimiter=",")
	i = 0
	for row in reader:
          print i
	  if i > 0:
   	    if row[3]:
  	      upc = row[3]
	      print upc
	      get_upc(upc)
          i += 1 
		  

csvfile.close()		
