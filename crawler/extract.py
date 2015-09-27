from bs4 import BeautifulSoup
import json

currenciesFile = open("currencies.json", 'w')
currencies=["AUD","CHF","CNY","EUR","GBP","HKD","JPY","KYD","USD"]
mapCurrencies = dict()
for currencyFrom in currencies:
    currenciesTo = [elem for elem in currencies if elem != currencyFrom]
    for currencyTo in currenciesTo :
        rate = currencyFrom + "_" + currencyTo
        HTMLfile = "pages/" + rate + ".html"
        soup = BeautifulSoup(open(HTMLfile))
        data = soup.find("td", { "class" : "rightCol" }).contents[0]
        mapCurrencies.update({rate : float(data)})
json.dump(mapCurrencies,currenciesFile)
