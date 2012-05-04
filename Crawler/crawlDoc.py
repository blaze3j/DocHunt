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

def fixLinks(soup, page, tag):
    for link in soup.find_all(tag):
        linkString = link.get('href')
        if None == linkString:
            continue
        mark = linkString.rfind('../')
        if -1 == mark:
            continue
        link['href'] = page + linkString[mark+3:]

def getRelatedText(page, link):
    text = []
    urlHandle = urllib2.urlopen(page + link)
    soup = bs4.BeautifulSoup(urlHandle.read())
    fixLinks(soup, page, 'a')
    fixLinks(soup, page, 'link')
    return soup.prettify()

def lemurTag(text,fileName):
    tag = fileName.replace(' ','')
    prefixTag = '<DOC>\n' + '<DOCNO> ' + tag + ' </DOCNO>\n'
    postfixTag = '</DOC>'
    print tag
    textTag = prefixTag + text + postfixTag
    return textTag

def lemurWriteText(text, fileName):
    handle = open(fileName, 'w')
    text = lemurTag(text, fileName)
    # text = text.encode('ascii', errors='ignore')
    handle.write(text)
    handle.close()
    print "dumped to " + fileName

destination = sys.argv[1]
parseDict = {'http://db.apache.org/derby/javadoc/publishedapi/jdbc3/':'derby',
             'http://www.thinwire.com/api/':'thinwire/',
             'http://aspectwerkz.codehaus.org/apidocs/':'aspect',
             'http://www.jfree.org/jfreechart/api/javadoc/':'jfreechart',
             'http://lucene.apache.org/core/3_6_0/api/all/':'lucene'}
#parseDict = {'http://db.apache.org/derby/javadoc/publishedapi/jdbc3/':'derby'}

for page in parseDict.keys():
    links = getClassHierarchyLinks(page, parseDict[page])

    for link in links:
        text = getRelatedText(page, link)
        path = os.path.join(destination,link.replace('/','_'))
        lemurWriteText(text, path)
