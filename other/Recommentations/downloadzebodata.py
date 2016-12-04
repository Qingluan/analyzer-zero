from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
import re

chare = re.complile(r'[!-\.&]')
itemowns = {}

#words to removed

dropwords = ['a','new','some','more','my','own','the','meny','other','another']

currentuser = 0
for i in range(1,51):
    c = urlopen()