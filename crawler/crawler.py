import requests
import re
import urlparse
import time

list = open("crawl-listing", 'w')
currenciesToCrawl = ["GBP", "EUR", "USD", "JPY", "CHF", "CNY", "HKD", "AUD", "KYD"]
URLToFill  = "http://www.xe.com/currencyconverter/convert/?Amount=1&From={0}&To={1}"
for currency in currenciesToCrawl:
    currenciesTo = [elem for elem in currenciesToCrawl if elem != currency]
    for currencyTo in currenciesTo:
        urlToAdd = URLToFill.format(currency, currencyTo)
        list.write(urlToAdd + "\n")
list.close()

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
