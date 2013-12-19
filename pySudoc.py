#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen # py3k 
import os
import re
from bs4 import BeautifulSoup

#Define a pattern for regExp
pattern = "<\/?([a-zA-Z]+\:[a-zA-Z]+)[>|\s]"
xmlNamespace = re.compile(pattern, re.U)

def getRDF(name, url, path = "./data/", debug = False, dic = False):
	"""Retrieve cached rdf file or crawl and cache given url

    Keyword arguments:
    name  -- Name to save file, usually contains the RDF id of SUDOC
    url	  -- URL of Sudoc Rdf document
    path  -- Path to cache folder
    debug -- Print debug data during execution
    dic   -- If True, Returns a dic containing xml code and path of cached file
    

	"""
	if debug:
		print "Page Request : " + url
	#Creating path
	if not os.access(path, os.R_OK):
		os.makedirs(path)
	
	path += name
	
	#If file exist, return file
	if os.path.exists(path):
		f = open(str(path), 'rt') 
		code = f.read()
		f.close()
	#Else, use urlopen
	else:
		#Get stream
		code = urlopen(url)
		#Read stream
		code = code.read()
		#Save stream
		f = open(str(path), 'wt') 
		f.write(code)
		f.close()
	
	if debug:
		print "Page Done : " + url
	
	#Dictionary or path, depending on dic True or false
	if dic:
		return {"html" : code, "path" : path}
	else:
		return path

def getURL(params, page, debug = False):
	"""Crawl a result page on Sudoc

    Keyword arguments:
    params -- Get parameters of search request
    page   -- Integer for page number
    debug  -- Print debug data during execution
    

	"""
	url = "http://www.sudoc.abes.fr//DB=2.1/CMD"
	#Creating start item int
	uid = page * 10 - 9
	uid = "&FRST=" + str(uid)
	#Returning socket
	if debug:
		print "Page " + str(page) + " : Link -> " + url + params + uid
		
	return urlopen(url + "?" + params + uid)

def getPage(name, params, page, path = "./data/", debug = False, dic = False):
	"""Retrieve cached result-page file or crawl and cache given results page with given params

    Keyword arguments:
    name   -- Name to save cache file
    params -- Get parameters of search request
    path   -- Path to cache folder
    debug  -- Print debug data during execution
    dic    -- If True, Returns a dic containing html code and path of cached file
    

	"""
	if debug:
		print "Page " + str(page) + " : Request"
	#Creating path
	if not os.access(path, os.R_OK):
		os.makedirs(path)
	
	path += name + "-page-" + str(page)
	
	#If file exist, return file
	if os.path.exists(path):
		f = open(str(path), 'rt') 
		code = f.read()
		f.close()
	#Else, use getURL
	else:
		#Get stream
		code = getURL(params, page, True)
		#Read stream
		code = code.read()
		#Save stream
		f = open(str(path), 'wt') 
		f.write(code)
		f.close()
	
	if debug:
		print "Page " + str(page) + " : Done"
	
	#Dictionary or path, depending on dic True or false
	if dic:
		return {"html" : code, "path" : path}
	else:
		return path

def getNumberItem(page):
	"""Returns the number of page available

    Keyword arguments:
    code -- Code of a page result, usually first one
    

	"""
	
	BS = BeautifulSoup(page)
	#Last link is found through it's image
	last = BS.find(src="http://cinabre.sudoc.abes.fr:80/img_psi/3.0/gui/nav-dernier.gif")
	
	#If we dont have last, we have only one page
	if not last:
		nbItem = 10
	else:
		#Getting a markup
		last = last.parent.parent
		#Getting href
		href = last["href"]
		
		#Regular expression
		pattern = "FRST=([0-9]+)"
		preg = re.compile(pattern)
		result = preg.findall(href)


		#Returning only first result
		nbItem = int(result[0])
	
	rest = nbItem % 10
	nbPage = nbItem / 10
	
	if rest > 0:
		nbPage += 1
	
	return nbPage

def getIndexes(name, params, path = "./data/", debug = False):
	"""Retrieve every results page for given params on Sudoc in a list

    Keyword arguments:
    name   -- Name to save cache file
    params -- Get parameters of search request
    path   -- Path to cache folder
    debug  -- Print debug data during execution
    

	"""
	indexes = []
	page= getPage(name, params, 1, path, debug, True)
	indexes.append(page["path"])
	#Number of Pages
	nbPage = getNumberItem(page["html"])
	
	#Getting all pages !
	i = 2
	while i < nbPage:
		page = getPage(name, params, i, path, debug)
		indexes.append(page)
		i += 1
	return indexes

def readIndex(path, debug = False):
	"""Retrieve every Sudoc entry for a given results page

    Keyword arguments:
    path   -- Path to cache file
    debug  -- Print debug data during execution
    

	"""
	f = open(path, 'rt') 
	html = f.read()
	f.close()
	
	array = []
	
	BS = BeautifulSoup(html)
	table = BS.find(summary="short title presentation")
	lines = table.find_all("tr")
	for line in lines:
		td = line.findAll('td',{'class':'rec_title'})
		td = td[0]
		id = td.find(type="hidden")
		id = id["value"]
		url = "http://www.sudoc.fr/" + id + ".rdf"
		array.append({"url" : url, "uid" : id})
		if debug:
			print "URL : " + url
	return array
	
def getItems(path, debug = False):
	"""Retrieve every results for a list of indexes or a simple index 

    Keyword arguments:
    path   -- Path to cache file
    debug  -- Print debug data during execution
    

	"""
	array = []
	if isinstance(path, list):
		for item in path:
			array += readIndex(item, debug)
	else:
		array += readIndex(path, debug)
		
	if debug:
		"URL : " + str(len(array)) + " Item(s) to be crawled"
		
	return array
	
def getSingleUnits(name, params, pathIndex = "./data/indexes", pathUnit = "./data/units", debug=False):	 
	"""Returns a list of rdf cached files's path for a given query

    Keyword arguments:
    name        -- Name to save cached index files
    params      -- Get parameters of search request
    pathIndex   -- Path to cache folder for results page
    pathUnit    -- Path to cache folder for rdf files
    debug       -- Print debug data during execution
    

	"""
	indexes = getIndexes(name, params, pathIndex, debug)
	items = getItems(indexes, debug)
	rdf = []
	for item in items:
		rdf += [getRDF("rdf-sudoc-"+item["uid"], item["url"], pathUnit, debug, False)]
		
	return rdf
	

def xmlNormalize(m):
	"""Normalize xml/rdf nameSpace so keys like key:Key could be retrieved through BeautifulSoup4 through keyKey

    Keyword arguments:
    m -- re.sub variables
    

	"""
	string = m.group(1)
	string = m.group(0).replace(string, string.replace(":", ""))
	return string

def getDetails(array, debug = False):
	"""Returns a dictionary with title, date, author, director and organization for each rdf file

    Keyword arguments:
    array       -- List of RDF files
    debug       -- Print debug data during execution
    

	"""
	array = set(array)
	
	ret = []
	for rdf in array:
		
		if debug:
			print "Reading " + rdf
			
		f = open(str(rdf), 'rt')
		code = f.read()
		f.close()
		
		code = xmlNamespace.sub(xmlNormalize, code)
		BS = BeautifulSoup(code, "xml")
		book = BS.find("biboBook")
		
		#Title
		title = book.find("dctitle")
		if title:
			title = title.text
		else:
			title = ""
		
		#Date of publication
		date = book.find("dcdate")
		if date:
			date = date.text
		else:
			date = ""
		
		#Author
		author = book.find("marcrelaut")
		if author:
			author = author.find("foafname").text
		else:
			author = ""
		
		#Directors
		directors = []
		for director in book.findAll("marcrelths"):
			directors.append(director.find("foafname").text)
			
		#Organizations
		organizations = []
		for organi in book.findAll("marcreldgg"):
			organizations.append(organi.find("foafname").text)
		
		#Subjects
		sub = []
		for subject in book.findAll("dcsubject"):
			sub.append(subject.text)
		
		a = {"path" : rdf,"title" : title, "date" : date, "subjects" : sub, "author" : author, "directors" : directors, "organization" : organizations}
		ret.append(a)
	return ret

def saveData(data = [], path = "./data/save.json", mode = "rt"):
	"""Save data in a json file, or read a saved file

    Keyword arguments:
    data   -- Date to be saved, string|list|dictionnary
    path   -- Path to cache file
    mode   -- Reading or writing mode
	"""
	import json
	if mode == "wt":
		f = open(path, "wt")
		f.write(json.dumps(data))
		f.close()
		return True
	else:
		f = open(path, "rt")
		data = json.load(f)
		f.close()
		return data
		
def CSV(details, path = "./data/_export.csv", headSeparator = "#", minorSeparator = ";"):
	"""Save data in a CSV

    Keyword arguments:
    details        -- Results of getDetails function or cached results
    path           -- Path to CSV file
    headSeparator  -- CSV's separator for columns
    minorSeparator -- CSV's separator for list in columns
    

	"""
    
	f = open(path, "wt+")
	#Headers
	row = ["path", "title", "date", "subjects", "author", "directors", "organization"]
	f.write(headSeparator.join(row).encode('utf-8') + "\n")
	#Contents
	for detail in details:
		row = [detail["path"], detail["title"], detail["date"], minorSeparator.join(detail["subjects"]), detail["author"], minorSeparator.join(detail["directors"]), minorSeparator.join(detail["organization"])]
		f.write(headSeparator.join(row).encode('utf-8') + "\n")
	f.close()

