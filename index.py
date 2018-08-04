#!/usr/bin/python

from bs4 import BeautifulSoup
import requests
import re
import codecs
import os
import sys
import urllib
import template

def find_domain (s):
    d = s.find("/", 8)
    if (d == -1):
        return s
    else:
        return s[:d]

def add_domain (tochange, domain):
    if (tochange.find("http://") == 0 or tochange.find("https://") == 0):
        return tochange
    elif (tochange.find("./") == 0):
        return domain + tochange[1:]
    elif (tochange.find("/") == 0):
        return domain + tochange
    else:
        return domain + "/" + tochange

def indexes (s, f):
    results = []
    x = s.find(f)
    while (x != -1):
        results.append(x)
        x = s.find(f, x+len(f))
    return results

def replace_links (s, domain):
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
        link = urllib.quote(add_domain(s[item[0]:item[1]], domain), safe="")
        links.append("http://terhune.xyz/shrink/index.py?url=" + link)
    
    if (len(links) == 1):
        return nonlinks[0]
    else:
        for x in range(len(links)-1):
            returnstring = returnstring + nonlinks[x]
            returnstring = returnstring + links[x]
        returnstring = returnstring + nonlinks[len(links)-1]
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
domain = find_domain(url)

r = requests.get(url, allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'})

soup = BeautifulSoup(r.text, "html.parser")
[s.extract() for s in soup(['script', 'style', 'svg', 'img', 'video'])]

myblob = replace_links(soup.body.prettify(), domain)

eb = myblob.find("</body>")
if (eb != -1):
    myblob = myblob[:eb] + myblob[eb+7:]

lines = myblob.splitlines()

if (lines[0].find("<body>") == 0):
    lines[0] = lines[0][6:]


print template.header
print template.head

for line in lines:
    print codecs.encode(line, 'utf8', 'ignore')

print template.foot









