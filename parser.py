from BeautifulSoup import BeautifulSoup
import urllib

f = urllib.urlopen("http://aspectwerkz.codehaus.org/apidocs/org/codehaus/aspectwerkz/aspect/AbstractAspectContainer.html")
html = f.read()
soup = BeautifulSoup(''.join(html))
 
tables = soup.findAll('table', border="1")
fields = []
methods = []
cons = []
for table in tables:
	isField = False
	isMethod = False
	isCons = False

	headings = table.findAll('th')
	for heading in headings:
  	   if heading.find(text="Field Summary")!=None:
  			isField = True
  	   elif heading.find(text="Constructor Summary")!=None:
  		isCons = True
  	   elif heading.find(text="Method Summary")!=None:
		isMethod = True
  	   rows = table.findAll('tr')
  	   for tr in rows:
  		cols = tr.findAll('td')
		count = 0 
  		for td in cols:
     			texts = td.find('a', href=True)
			if texts!=None:
				link = texts['href']
				beforeSig = link.find('#')
				if beforeSig!=-1:
					name=link[beforeSig+1:]
     					#name=texts.find(text=True)
     					if count >0 and isField:
						fields.append(name)
     						print "Field:" + name
					elif count > 0 and isMethod:
						methods.append(name)
						print "Method:" + name
					elif isCons:
						cons.append(name)
						print "Cons:" + name
			count+=1
