#!/usr/bin/python
import re
import urllib2
from bs4 import BeautifulSoup
import lxml
from lxml.html.clean import Cleaner
from dandelion import DataTXT


p = re.compile('iframe.*?src="(.*?)"')
f = open("index.html", "r")
content = f.read()
m = p.search(content)

url = m.group(1)

response = urllib2.urlopen(m.group(1))
html = response.read()


cleaner = Cleaner()
cleaner.javascript = True
cleaner.style = True

#print lxml.html.tostring(cleaner.clean_html(lxml.html.parse(url)))
clean = cleaner.clean_html(lxml.html.parse(url)) 
clean = lxml.html.tostring(clean)

soup = BeautifulSoup(clean, 'lxml')
text = soup.get_text()

datatxt = DataTXT(app_id='d40305b7', app_key='7d432531dfb0d3173212d4203f25d4b6')

#response = datatxt.sim(text, "The ultimate skel-ebration of monster mania, this year's Monster High dance will be the monster bash to end all bashes (if it happens)! And as the Monster High ghouls make new beast friends, the horror show really begins. This freaky fabulous new character is larger than unlife at 17 inches tall! And of course, she wears an over-the-tent fashion with lots of ")

paragraphs = list()
match  = list()

for line in text.splitlines(): 
  if len(line) > 20:
    paragraphs.append(line)

paragraphs = paragraphs[0:5]
for p in paragraphs:     
  response = datatxt.sim(p, "The ultimate skel-ebration of monster mania, this year's Monster High dance will be the monster bash to end all bashes (if it happens)! And as the Monster High ghouls make new beast friends, the horror show really begins. This freaky fabulous new character is larger than unlife at 17 inches tall! And of course, she wears an over-the-tent fashion with lots of ")
  match.append(response.similarity)


match.sort(reverse=True)
print match


