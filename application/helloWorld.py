from urlparse import urlunparse
from sets import Set
from random import randint
import random
import web
import json
import urllib2
import sys
import copy
import math
import time

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

def bellmanFord(currency,nb_currencies):
    tab=matrix = [[0]*nb_currencies for i in range(nb_currencies)]
    listOfRate = ["USD","JPY", "GBP", "EUR"]
    for i in range(0,nb_currencies):
        for j in range(0,nb_currencies):
          tab[i][j]=currency.getRateFromTo(listOfRate[i],listOfRate[j]).value

    for i in range(0,nb_currencies):
        for j in range(0,nb_currencies):
            tab[i][j]= -math.log(tab[i][j])

    dis = []
    pre = []

    for i in range(0,nb_currencies):
        dis.append(float("infinity"))
        pre.append(-1)

    dis[0]=0

    for k in range(0,nb_currencies):
        for i in range(0,nb_currencies):
            for j in range(0,nb_currencies):
                if(j != i):
                    if(dis[i]+tab[i][j] < dis[j]):
                        dis[j]=dis[i]+tab[i][j]
                        pre[j]=i

    findCycle = False
    cycle = []
    for i in range(0,nb_currencies):
        for j in range(0,nb_currencies):
            if(dis[i]+tab[i][j]<dis[j]):
                findCycle = True
                start = pre[i]

    if(findCycle):
        z = start
        cycle.append(listOfRate[z])
        count = 0
        while (pre[z] != start):
            count = count + 1
            z = pre[z]
            cycle.append(listOfRate[z])
            if (count > nb_currencies + 1):
                print("Error need to check that")
                for i in range(0,nb_currencies):
                    print(pre[i])
                break
        cycle.append(listOfRate[pre[z]])


    return cycle

def acceptance_probability(old_cost,new_cost,T):
    return math.exp((new_cost - old_cost)/T)

def anneal(currencies,nb_currencies):
    popInit = Individual(currencies)
    rateInit = popInit.getToTalValue(currencies)
    T = 1.0
    T_min = 0.00001
    alpha = 0.9
    population = copy.deepcopy(popInit)
    population.changeNeighbor(currencies,nb_currencies)
    while T > T_min :
        i = 1
        while i <= 100:
            population.changeNeighbor(currencies,nb_currencies)
            costNeighbor = population.getToTalValue(currencies)
            ap = acceptance_probability(rateInit,costNeighbor,T)
            if ap > random.random():
                popInit = copy.deepcopy(population)
                rateInit = popInit.getToTalValue(currencies)
            i += 1
        T = T * alpha
    return popInit

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
    totalValue = 1

    def getToTalValue(self, currency):
        totalValue = 1
        newWay = self.way
        newWay = [elem for elem in self.way if elem != "NONE"]
        waySize = len(newWay)
        for i in range (1, waySize):
            totalValue = currency.getRateFromTo(safe_list_get(newWay, i - 1, "lol"), safe_list_get(newWay, i, "lol")).value * totalValue
        return totalValue

    def __init__(self, currency):
        way = []
        listOfRate = ["JPY", "GBP", "EUR"]
        way.append("USD")
        for i in range (1,4):
            way.append(random.choice(listOfRate))
        way.append("USD")
        self.way = way
        self.cleanWay()
        self.totalValue = self.getToTalValue(currency)

    def changeNeighbor(self,currencies,nb_currencies):
        listOfRate = ["JPY", "GBP", "EUR","NONE"]
        self.way[randint(1,nb_currencies - 1)]=listOfRate[randint(0,3)]
        self.cleanWay()
        self.totalValue = self.getToTalValue(currencies)


    def cleanWay(self):
        for i in range (0, len(self.way) - 1):
            for j in range (0, i):
                if safe_list_get(self.way, i, "lol") == safe_list_get(self.way, j, "lol"):
                    self.way[i] = "NONE"

    def __str__(self):
        wayToDisplay = []
        for i in range (len(self.way)):
            wayToDisplay.append(safe_list_get(self.way, i, "lol"))
        return str(wayToDisplay ) + " " + str(self.totalValue)

    def setWay(self, way):
        self.way = way

    def setTotalValue(self,currency):
        totalValue = 1
        wayWithoutNone = [elem for elem in self.way if elem != "NONE"]
        for i in range (0, len(wayWithoutNone)-1):
            totalValue = totalValue * currency.getRateFromTo(wayWithoutNone[i],wayWithoutNone[i+1]).value
        self.totalValue = totalValue

class Currencies(object):

    def __init__ (self):
        with open('currencies.json') as data_file:
            res = json.load(data_file)
        for key, value in res.iteritems():
            setattr(self, key, Rate(value, key[0:3], key[4:7]))
        self.EUR_EUR = Rate(1.000000, "EUR", "EUR")
        self.USD_USD = Rate(1.000000, "USD", "USD")
        self.JPY_JPY = Rate(1.000000, "JPY", "JPY")
        self.GBP_GBP = Rate(1.000000, "GBP", "GBP")
        self.EUR_EUR = Rate(1.000000, "CHF", "CHF")
        self.USD_USD = Rate(1.000000, "AUD", "AUD")
        self.JPY_JPY = Rate(1.000000, "CNY", "CNY")
        self.GBP_GBP = Rate(1.000000, "GBP", "GBP")
        self.GBP_GBP = Rate(1.000000, "KYD", "KYD")

    def getRateFromTo(self, fromCurrency, toCurrency):
        return getattr(self, fromCurrency + "_" + toCurrency)

class Index(object):
    def GET(self):
        currencies = Currencies()
        individual = Individual(currencies)
        t0_anneal = time.time()
        res_anneal = anneal(currencies,4)
        t_final_anneal = time.time() - t0_anneal
        t0_bellman = time.time()
        cycle = bellmanFord(currencies,4)
        t_final_bellman = time.time() - t0_bellman
        testBellmanFord = Individual(currencies)
        testBellmanFord.setWay(cycle)
        testBellmanFord.setTotalValue(currencies)
        data = {"BellmanFord" :{ 'timer': t_final_bellman, 'totalRate':testBellmanFord.totalValue, 'way':testBellmanFord.way },"Annealing" :{ 'timer' : t_final_anneal, 'totalRate':res_anneal.totalValue, 'way':res_anneal.way}
        }
        with open('static/result.js', 'w') as outfile:
                outfile.write("var json =")
                json.dump(data, outfile)
        return static.index(res = currencies)


if __name__ == "__main__":
    app.run()
