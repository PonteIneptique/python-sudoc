python-sudoc
============

pySudoc.py helps you to crawl RDFs descriptions of books or thesis from SUDOC search engine

It is highly recommanded to rewrite for your own use pySudoc.CSV() and pySudoc.getDetails() functions as they have been written for Phd thesis data. Documentation is included so you should not be lost.

Pushing modifications for this snippet is highly welcomed, most of all if they aim to generalize functionnalities or correct bugs.

I am just sharing it as I needed to develop it and thought it might be nice to let you use it ;) 

#Example
You can run exemple.py
It will run a query on phd Thesis with Augustin in its title and latin in subjects.

#Dependencies
* BeautifulSoup
* urllib
* re
* os

