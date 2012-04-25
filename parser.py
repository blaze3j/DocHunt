from BeautifulSoup import BeautifulSoup
import urllib,sys
if (len(sys.argv) != 2):
 sys.exit("Must provide file list")
else:
 doc = open(sys.argv[1], 'r')
 for line in doc:
   #for handling raw url like: 
   #http://aspectwerkz.codehaus.org/apidocs/org/codehaus/aspectwerkz/aspect/AbstractAspectContainer.html
   if line.startswith("http"):
   	f = urllib.urlopen(line)
   #for the case where the html files are downloaded
   else:
	if line.startswith("./"):
		line = line[2:len(line)]
	if line.endswith("\n"):
		line = line[0:len(line)-1]
	f = open(line,'r')
   
   html = f.read()
   soup = BeautifulSoup(''.join(html))
 
   tables = soup.findAll('table', border="1")
   #fields = []
   #methods = []
   #cons = []
   lastDoc = line.rfind(".")
   lastSlash = line.rfind("/")
   className =""
   #get the className to create xml file that has the className
   if lastSlash != -1:
     className = line[lastSlash+1:lastDoc]
   else:
     className = line[0:lastDoc]
   xmlFile = open(className+ '.xml', 'w+')
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
						#fields.append(name)
						xmlFile.write("<cfield>" + name + "</cfield>\n") 
     						print "Field:" + name
					elif count > 0 and isMethod:
						#methods.append(name)
						xmlFile.write("<cmethod>" +  name + "</cmethod>\n")
						print "Method:" + name
					elif isCons:
						#cons.append(name)
						xmlFile.write("<ccons>" + name + "</ccons>\n")
						print "Cons:" + name
			count+=1
