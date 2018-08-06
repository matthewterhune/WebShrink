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

#Read in get and post arguments from the page submission. Should only have GET currently
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

#Add the default stylesheet
sheets = ["default"]

if (len(GET) == 0):
	showinfo = True
elif (GET["url"] == u""):
	showinfo = True
else:
	showinfo = False
	url = urllib.unquote(GET["url"])

	r = False
	if (url.find("https://") != 0 and url.find("http://") != 0):
		try:
			r = requests.get("http://" + url, allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'})
		except:
			try:
				r = requests.get("https://" + url, allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'})
			except:
				pass
	else:
		try:
			r = requests.get(url, allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'})
		except:
			pass

	if (r == False):
		url = "https://bing.com/search?q=" + url.replace(" ", "+")
		r = requests.get(url, allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'})

	domain = find_domain(url)

	#Retrieve the url. Spoof Firefox user agent to avoid looking like a bot
	#r = requests.get(url, allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'})

	#Create soup object, then extract and discard the tags we don't want
	soup = BeautifulSoup(r.text, "html.parser")
	[s.extract() for s in soup(['script', 'style', 'svg', 'img', 'video', 'iframe'])]

	#Delete any inline style from the remaining tags
	for tag in soup():
	    for attribute in ["style"]:
	        del tag[attribute]

	#Convert soup object back to string, then add our custom domain to any links
	myblob = replace_links(soup.body.prettify(), domain)

	#Remove the body tags so we can add our own header
	eb = myblob.find("</body>")
	if (eb != -1):
	    myblob = myblob[:eb] + myblob[eb+7:]

	lines = myblob.splitlines() #Python freaks out if we print a super long string, so split into lines

	if (lines[0].find("<body") == 0):
	    lines[0] = lines[0][lines[0].find(">")+1:]

	#Assemble list of custom stylesheets
	sheets.append(domain[domain.find("//")+2:])

#Print the page
print template.header()
print template.head(sheets)

if showinfo:
	print template.info()
else:
	for line in lines:
	    print codecs.encode(line, 'utf8', 'ignore')

print template.foot()










