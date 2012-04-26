#!/usr/bin/env python

import bs4
import urllib2
import sys
import os

def parse(path, dest):
    # f = urllib2.urlopen(path)
    # html = f.read()
    # print 'path ' + path
    f = open(path, 'r')
    html = f.read()
    f.close()
    # print html
    soup = bs4.BeautifulSoup(html)
    
    # print soup.prettify()
    # print tables
    #fields = []
    #methods = []
    #cons = []
    # (base, ext) = os.path.splitext(path)

    lastDoc = path.rfind(".")
    lastSlash = path.rfind("/")
    className = ""
    #get the className to create xml file that has the className
    if lastSlash != -1:
        className = path[lastSlash+1:lastDoc]
    else:
        className = line[0:lastDoc]

    dataDict = {}
    tables = soup.findAll('table')
    for table in tables:
        # print str(table).find("Method Summary")
        # print table.find("Method Summary")
        # print table.previousSibling
        headings = table.findAll('th')
        # print headings
        for heading in headings:
            # print 'heading ' + str(heading)

            if str(table).find("Field Summary") != -1:
                dataType = 'cfield'
            elif str(table).find("Constructor Summary") != -1:
                dataType = 'ccons'
            elif str(table).find("Method Summary") != -1:
                dataType = 'cmethod'
            else:
                dataType = None
            rows = table.findAll('tr')
            for tr in rows:
                # print tr
                cols = tr.findAll('td')
                count = 0
                for td in cols:
                    #print count
                    #print isMethod
                    texts = td.find('a', href=True)
                    # print texts
                    if texts!=None:
                        link = texts['href']
                        # print link
                        beforeSig = link.find('#')
                        if beforeSig!=-1:
                            name=link[beforeSig+1:]
                            #name=texts.find(text=True)
                            if count > 0 and None != dataType:
                                dataDict.setdefault(name, dataType)
                    count = count + 1
    # print dataDict
    xmlFilePath = os.path.join(dest,className + '.xml')
    print 'generating ' + xmlFilePath
    xmlFile = open(xmlFilePath, 'w')

    for key in dataDict.keys():
        line = "<" + dataDict[key] + ">" + key + "</" + dataDict[key] + ">\n"
        xmlFile.write(line) 
        print line
    
    xmlFile.close()

path = sys.argv[1]
dest = sys.argv[2]

for root, dirs, files in os.walk(path):
    for fileName in files:
        (base, ext) = os.path.splitext(fileName)
        if -1 == ext.find('.html'):
            continue

        fullPath = os.path.join(root,fileName)
        print 'processing ' + fullPath
        parse(fullPath, dest)
        # sys.exit(0)
