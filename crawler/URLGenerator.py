list = open("crawl-listing", 'w')
currenciesToCrawl = ["GBP", "EUR", "USD", "JPY", "CHF", "CNY", "HKD", "AUD", "KYD"]
URLToFill  = "http://www.xe.com/currencyconverter/convert/?Amount=1&From={0}&To={1}"
for currency in currenciesToCrawl:
    currenciesTo = [elem for elem in currenciesToCrawl if elem != currency]
    for currencyTo in currenciesTo:
        urlToAdd = URLToFill.format(currency, currencyTo)
        list.write(urlToAdd + "\n")
list.close()
