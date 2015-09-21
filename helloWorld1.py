from urlparse import urlunparse
from sets import Set
from random import randint
import random
import web
import json
import urllib2
import sys
import copy

urls = (
  '/', 'Index',
  '/data', 'Data'
)

app = web.application(urls, globals())

static = web.template.render('static/')
template = web.template.render('templates/')


def safe_list_get (l, idx, default):
    try:
        return l[idx]
    except IndexError:
        return default

class Rate(object):
    value = 0.0
    fromCurrency = ""
    toCurrency = ""

    def __init__(self, value = 0.0, fromCurrency = "", toCurrency = ""):
        self.value = value
        self.fromCurrency = fromCurrency
        self.toCurrency = toCurrency

    def __str__(self):
        return str(self.value)


class Individual(object):
    way = []

    def __init__(self, currency):
        way = []
        totalValue = 1.0
        way.append(currency.getRandomRateFromACurrency("USD"))
        for i in range (1, 14):
            way.append(currency.getRandomRateFromACurrency(safe_list_get(way, i-1, "lol").toCurrency))
        way.append(currency.getRandomRateToUSD(safe_list_get(way, 13, "lol").toCurrency))
        for i in range (0, 15):
            #print(safe_list_get(way, i, "lol").fromCurrency, safe_list_get(way, i, "lol").toCurrency)
            #print(totalValue, safe_list_get(way, i, "lol").value)
            totalValue = totalValue * (safe_list_get(way, i, "lol").value)
        self.way = way
        self.totalValue = totalValue

    def __str__(self):
        wayToDisplay = []
        wayToDisplay.append("USD")
        for i in range (0, 15):
            wayToDisplay.append(safe_list_get(self.way, i, "lol").toCurrency)
        return str(self.totalValue) + " " + str(wayToDisplay)

    def __eq__(self, other):
        return self.totalValue == other.totalValue

    def __cmp__(self,other):
        return cmp(self.totalValue, other.totalValue)


    def setWay(self, way):
        self.way = way

    def setTotatlValue(self):
        totalValue = 1
        for i in range (0, 15):
            totalValue = totalValue * (safe_list_get(self.way, i, "lol").value)
        self.totalValue = totalValue


class Population():
    individuals = []

    def getBest5Indivuals(self):
        sortedIndividuals = sorted(self.individuals)
        best = []
        for i in range (4, 10):
            best.append(safe_list_get(sortedIndividuals, i, "lol"))
        return best

    def crossOver(self, listOfIndividuals, currencies):
        crossedIndividuals = []
        for i in range(0,2):
            individual1 = copy.deepcopy(safe_list_get(listOfIndividuals, randint(0,5), "lol"))
            individual2 = copy.deepcopy(safe_list_get(listOfIndividuals, randint(0,5), "lol"))
            crossPosition = randint(3,13)
            DNAson1 = []
            DNAson2 = []
            for i in range(0, crossPosition):
                DNAson1.append(safe_list_get(individual1.way, i, "lol"))
                DNAson2.append(safe_list_get(individual2.way, i, "lol"))
            DNAson1.append(currencies.getRateFromTo(safe_list_get(individual1.way, crossPosition - 1, "lol").toCurrency, safe_list_get(individual2.way, crossPosition + 1, "lol").fromCurrency))
            DNAson2.append(currencies.getRateFromTo(safe_list_get(individual2.way, crossPosition - 1, "lol").toCurrency, safe_list_get(individual1.way, crossPosition + 1, "lol").fromCurrency))
            for i in range(crossPosition + 1, 15):
                DNAson1.append(safe_list_get(individual2.way, i, "lol"))
                DNAson2.append(safe_list_get(individual1.way, i, "lol"))
            individual1.setWay(DNAson1)
            individual2.setWay(DNAson2)
            individual1.setTotatlValue()
            individual2.setTotatlValue()
            crossedIndividuals.append(individual1)
            crossedIndividuals.append(individual2)
        return crossedIndividuals

    def mutation(self):
        print("mutation")

    def __init__(self, setOfIndividuals):
        self.individuals = setOfIndividuals

    def __str__(self):
        valueToDisplay = ""
        for i in range(0,10):
            valueToDisplay = valueToDisplay + str(safe_list_get(self.individuals, i, "lol"))
            valueToDisplay = valueToDisplay + "\n"
        return valueToDisplay



class Currencies(object):

    def __init__ (self):
        try:
            rates = urllib2.urlopen("http://fx.priceonomics.com/v1/rates/")
        except urllib2.URLError as e:
            return e.reasonx
        res = json.load(rates)
        self.EURToEUR = Rate(1.000000, "EUR", "EUR")
        self.USDToUSD = Rate(1.000000, "USD", "USD")
        self.JPYToJPY = Rate(1.000000, "JPY", "JPY")
        self.BTCToBTC = Rate(1.000000, "BTC", "BTC")
        self.EURToUSD = Rate(float(res['EUR_USD']), "EUR", "USD")
        self.EURToJPY = Rate(float(res['EUR_JPY']), "EUR", "JPY")
        self.EURToBTC = Rate(float(res['EUR_BTC']), "EUR", "BTC")
        self.USDToEUR = Rate(float(res['USD_EUR']), "USD", "EUR")
        self.USDToBTC = Rate(float(res['USD_BTC']), "USD", "BTC")
        self.USDToJPY = Rate(float(res['USD_JPY']), "USD", "JPY")
        self.BTCToEUR = Rate(float(res['BTC_EUR']), "BTC", "EUR")
        self.BTCToJPY = Rate(float(res['BTC_JPY']), "BTC", "JPY")
        self.BTCToUSD = Rate(float(res['BTC_USD']), "BTC", "USD")
        self.JPYToEUR = Rate(float(res['JPY_EUR']), "JPY", "EUR")
        self.JPYToUSD = Rate(float(res['JPY_USD']), "JPY", "USD")
        self.JPYToBTC = Rate(float(res['JPY_BTC']), "JPY", "BTC")

    def getRandomRateFromACurrency(self, currency):
        return random.choice([v for attr, v in vars(self).items()if len(attr) == 8 and attr[0:3] == currency])

    def getRandomRateToUSD(self, currency):
        if(currency == "JPY"):
            return self.JPYToUSD
        if(currency == "BTC"):
            return self.BTCToUSD
        if(currency == "EUR"):
            return self.EURToUSD
        else:
            return self.USDToUSD

    def getRateFromTo(self, fromCurrency, toCurrency):
        return getattr(self, fromCurrency + "To" + toCurrency)

    def getRandomRate(self):
        return random.choice([v for attr, v in vars(self).items()if len(attr) == 8 and attr[3:5] == 'To'])



class Index(object):
    def GET(self):
        currencies = Currencies()
        individual = Individual(currencies)
        firstGenList = []
        for i in range(0, 20):
            firstGenList.append(Individual(currencies))
        population = Population(firstGenList)
        for i in range(0, 10000):
            bests = population.getBest5Indivuals()
            crossed = population.crossOver(bests, currencies)
            newIndividuals = bests + crossed
            population = Population(newIndividuals)
        resFromGenetic = safe_list_get(population.individuals, 9, "lol")
        print(population)
        return static.index(res = currencies, random = resFromGenetic)

if __name__ == "__main__":
    app.run()
