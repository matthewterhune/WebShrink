#!/usr/bin/python

import Cookie
import os
import sys
import template

GET={}
args=os.getenv("QUERY_STRING").split('&')

for arg in args:
    t=arg.split('=')
    if len(t)>1: k,v=arg.split('='); GET[k]=v

print "Content-Type: text/html"

if (len(GET) != 0):
	c = Cookie.SimpleCookie()
	for key in GET:
		c[key] = GET[key]
		c[key]["max-age"] = "315000000"
	print c

print "\r\n"

print template.head(["default"])
print template.settings()
print template.foot()
