import requests
import re
import urlparse
import time

crawlListing = open('URLListing')
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
}
lineCounter = 0
for URL in iter(crawlListing):
    query = urlparse.urlparse(URL).query
    regexFrom = re.search('From=(.*)&', query)
    regexTo = re.search('To=(.*)', query)
    fileToCreate = "pages/" + regexFrom.group(1) + "_" + regexTo.group(1) + ".html"
    page = requests.get(URL, headers=headers)
    with open(fileToCreate, 'w') as outfile:
        outfile.write(page.content)
    lineCounter = lineCounter + 1
    print "Number of pages crawled = %d" %(lineCounter)
    time.sleep(3)
crawlListing.close()
