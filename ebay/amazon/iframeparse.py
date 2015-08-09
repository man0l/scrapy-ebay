import lxml
import lxml.html
from bs4 import BeautifulSoup
from bs4 import BeautifulStoneSoup

import urllib2
from lxml.html.clean import Cleaner
import unicodedata
from lxml import etree
import re



def cleanMe(text):
       cleaner = Cleaner()
       cleaner.javascript = True
       cleaner.style = True
       #text = unicodedata.normalize("NFKD", text).encode('ascii','ignore')
       clean = cleaner.clean_html(text) 
       return clean


with open("test.html", "r") as myfile:
    data=myfile.read()

udata = unicode(data, "utf-8")
doc = lxml.html.fromstring(udata)
b = doc.cssselect(".a-container")[0]
c = etree.tostring(b)

if doc.cssselect(".a-container")[0].xpath("script[contains(.,'ProductDescriptionIframeResize')]"):
    v = doc.cssselect(".a-container")[0].xpath("script[contains(.,'ProductDescriptionIframeResize')]")[0]
    c = etree.tostring(v)

p = re.compile("var iframeContent = \"(.*?)\"")
m = p.search(c)

a = m.group(1)

a = cleanMe(urllib2.unquote(a))


doc = lxml.html.fromstring(a)
v = doc.cssselect(".productDescriptionWrapper")[0]
a = etree.tostring(v)

a = unicode(a, "utf-8")
 
soup = BeautifulSoup(a, "lxml")
print soup.get_text().strip()

