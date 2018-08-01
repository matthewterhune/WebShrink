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

def replace_links (s):
	singlequote = indexes(s, "href='")
	doublequote = indexes(s, 'href="')

	results = []
	nonlinks = []
	links = []
	returnstring = ""

	for item in singlequote:
		results.append([item+6, s.find("'", item+6)])
	for item in doublequote:
		results.append([item+6, s.find('"', item+6)])

	results.append([len(s), len(s)])
	nonlinks.append(s[:results[0][0]])
	for x in range(len(results)-1):
		nonlinks.append(s[results[x][1]:results[x+1][0]])

	for item in results:
		links.append("http://terhune.xyz/shrink/index.py?url=" + urllib.quote(s[item[0]:item[1]], safe=""))
	
	for x in range(len(links)):
		returnstring = returnstring + nonlinks[x]
		returnstring = returnstring + links[x]
	return returnstring


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

url = urllib.unquote(GET["url"])

r = requests.get(url, allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'})

soup = BeautifulSoup(r.text, "html.parser")
[s.extract() for s in soup(['script', 'style', 'svg', 'img', 'video'])]

myblob = replace_links(soup.body.prettify())


print "Content-Type: text/html\r\n"

print '''
<!DOCTYPE html>"
<html>"
<head>
	<meta charSet="utf8"/>
	<link rel="stylesheet" type="text/css" href="default.css">
</head>
'''

for line in myblob.splitlines():
    print codecs.encode(line, 'utf8', 'ignore')

print "</html>"