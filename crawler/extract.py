from HTMLParser import HTMLParser

currencies=["AUD","CHF","CNY","EUR","GBP","HKD","JPY","KYD","USD"]
for currencyFrom in currencies:
    currenciesTo = [elem for elem in currencies if elem != currencyFrom]
    for currencyTo in currenciesTo :
        file = "pages/" + currencyFrom + "_" + currencyTo + ".html"
        data =  html2text.html2text(open(file,'r').read())
        print(data)
        break
