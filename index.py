#!/usr/bin/python

from bs4 import BeautifulSoup
import requests
import re
import codecs
import os
import sys
import urllib

def indexes (s, f):
	results = []
	x = s.find(f)
	while (x != -1):
		results.append(x)
		x = s.find(f, x+len(f))
	return results

def find_links (s):
	singlequote = indexes(s, "href='")
	doublequote = indexes(s, 'href="')
	results = []
	for item in singlequote:
		results.append([item+6, s.find("'", item+6)])
	for item in doublequote:
		results.append([item+6, s.find('"', item+6)])
	return results



defaultstyle = '''
<style>
html {
	background-color: #b5c9d1 !important;
}
body {
	width: 760px !important;
	background-color: white !important;
	margin: 24px auto !important;
	padding: 50px !important;
	line-height: 1.3;
	font-size: 1.05em;
}
div {
	margin: 0 !important;
	padding: 0 !important;
}
a {
	color: #031DB5;
}
</style>
'''

GET={}
args=os.getenv("QUERY_STRING").split('&')

for arg in args:
    t=arg.split('=')
    if len(t)>1: k,v=arg.split('='); GET[k]=v

POST={}
args=sys.stdin.read().split('&')

for arg in args:
    t=arg.split('=')
    if len(t)>1: k, v=arg.split('='); POST[k]=v


r = requests.get(GET["url"], allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'})

soup = BeautifulSoup(r.text, "html.parser")
[s.extract() for s in soup(['script', 'style', 'svg', 'img', 'video'])]

myblob = soup.body.prettify()

print "Content-Type: text/html\r\n"
print "<!DOCTYPE html>"
print "<html>"
print '<head><meta charSet="utf8"/>' + defaultstyle + '</head>'

'''for line in codecs.iterencode(myblob.splitlines(), encoding='utf8'):
    print line'''
for line in myblob.splitlines():
    print codecs.encode(line, 'utf8', 'ignore')

print "</html>"