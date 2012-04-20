#!/usr/bin/env python

import bs4
import urllib2
import os
import sys
import time
import commands

def getClassHierarchyLinks(page, key):
    links = []
    urlHandle = urllib2.urlopen(page + 'overview-tree.html')
    soup = bs4.BeautifulSoup(urlHandle.read())

    print 'processing ' + soup.title.string.strip()
    
    for link in soup.find_all('a'):
        linkString = link.get('href')
        # print linkString
        if None == linkString or -1 == linkString.find(key):
            continue
        links.append(link.get('href'))

    return links

def getRelatedText(page):
    text = []
    urlHandle = urllib2.urlopen(page)
    soup = bs4.BeautifulSoup(urlHandle.read())

    return soup.prettify()

destination = sys.argv[1]
parseDict = {'http://db.apache.org/derby/javadoc/publishedapi/jdbc3/':'derby',
             'http://www.thinwire.com/api/':'thinwire/'}

for page in parseDict.keys():
    links = getClassHierarchyLinks(page, parseDict[page])

    for link in links:
        text = getRelatedText(page + link)
        path = os.path.join(destination,link.replace('/','_'))
        fd = open(path, 'w')
        fd.write(text)
        fd.close()
