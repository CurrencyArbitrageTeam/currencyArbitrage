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
    listOfRate = ["USD","EUR","JPY","GBP","CHF","AUD","CNY","HKD","KYD"]
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

def anneal(currencies,nb_currencies,**keyword_parameters):
    if ('optional' in keyword_parameters):
        popInit = keyword_parameters['optional']
    else:
        popInit = Individual(currencies)
    rateInit = popInit.getToTalValue(currencies)
    T = 0.00001
    T_min = 0.0000001
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
    newWay = []
    popInit.clearWayForHtlm()
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

class Population(object):

    pop = []

    def __init__(self, currency):
        for i in range(0,40):
            self.pop.append(Individual(currency))

    def nbOfDominations(self,individual):
        numberOfDomination = 0
        for population in self.pop:
            if ((population.nbCurrencies <= individual.nbCurrencies) & (population.totalValue > individual.totalValue)):
                numberOfDomination += 1
        return numberOfDomination

    def isDominated(self,individual):
        if self.nbOfDominations(individual) > 0 :
            return True
        return False

    def pareto(self,pop,sizePop):
        selected = []
        count = 0
        nbOfDomination = 0
        while count < sizePop :
            for individual in pop:
                if self.nbOfDominations(individual) == nbOfDomination :
                    selected.append(individual)
                    count += 1
                    if count == sizePop:
                        break
            nbOfDomination += 1
        return selected

    def mutation(self,pop,currencies):
        listOfRate = ["EUR","JPY","GBP","CHF","AUD","CNY","HKD","KYD"]
        for individual in pop:
            for currency in individual.way:
                if currency != "USD":
                    if random.random() < 0.1:
                        currency = listOfRate[randint(0,7)]
            individual.setIndividuals(currencies,individual.way)
        return pop

    def cross_over(self, selected, currencies):
            listOfChild = []
            while len(selected) != 0:
                parent1 = random.choice(selected)
                selected = [elem for elem in selected if elem != parent1]
                parent2 = random.choice(selected)
                selected = [elem for elem in selected if elem != parent2]
                sizeIndividualWay = len(parent1.way)
                sonWay1 = []
                sonWay2 = []
                sizeIndex = 0
                while sizeIndex != sizeIndividualWay:
                    if random.random() < 0.5:
                        sonWay1.append(safe_list_get(parent1.way, sizeIndex, "Not found"))
                    else:
                        sonWay1.append(safe_list_get(parent2.way, sizeIndex, "Not found"))
                    if random.random() < 0.5:
                        sonWay2.append(safe_list_get(parent1.way, sizeIndex, "Not found"))
                    else:
                        sonWay2.append(safe_list_get(parent2.way, sizeIndex, "Not found"))
                    sizeIndex += 1
                son1 = Individual(currencies)
                son2 = Individual(currencies)
                son1.setIndividuals(currencies, sonWay1)
                son2.setIndividuals(currencies, sonWay2)
                listOfChild.append(son1)
                listOfChild.append(son2)
            return listOfChild

    def evolution(self,currencies):
        convergenceVisualisationRate = []
        convergenceVisualisationCurrency = []
        parents = copy.deepcopy(self.pop)
        parents = self.pareto(parents,40)
        for i in range(0,20):
            summNbCurrencies = 0
            populationNbCurrencies = []
            for j in parents:
                summNbCurrencies += j.nbCurrencies
                individualPositionRate = []
                individualPositionRate.append(i)
                individualPositionRate.append(j.totalValue)
                convergenceVisualisationRate.append(individualPositionRate)
            populationNbCurrencies.append(i)
            populationNbCurrencies.append(float(summNbCurrencies)/float(len(parents)))
            convergenceVisualisationCurrency.append(populationNbCurrencies)
            kids = self.cross_over(parents,currencies)
            pop = copy.deepcopy(parents + kids )
            popMutated = self.mutation(pop,currencies)
            popRanked = self.pareto(popMutated,40)
            parents = copy.deepcopy(popRanked)
        with open('static/convergence.js', 'w') as outfile:
                outfile.write("var jsonConvergenceRate =")
                json.dump(convergenceVisualisationRate, outfile)
                outfile.write(";\n var jsonConvergenceCurrencies =")
                json.dump(convergenceVisualisationCurrency, outfile)
        self.pop = copy.deepcopy(parents)


    def setPopulation(self,newPopulation,popSize):
        for i in range(0,popSize):
            self.pop.append(newPopulation[i])

class Individual(object):

    way = []
    totalValue = 1
    nbCurrencies = 0

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
        listOfRate = ["EUR","JPY","GBP","CHF","AUD","CNY","HKD","KYD"]
        way.append("USD")
        for i in range (0,len(listOfRate)):
            way.append(random.choice(listOfRate))
        way.append("USD")
        self.way = way
        self.cleanWay()
        self.totalValue = self.getToTalValue(currency)
        self.nbCurrencies = self.getNbCurrencies()

    def changeNeighbor(self,currencies,nb_currencies):
        listOfRate = ["EUR","JPY","GBP","CHF","AUD","CNY","HKD","KYD"]
        self.way[randint(1,nb_currencies - 1)]=listOfRate[randint(0,7)]
        self.cleanWay()
        self.totalValue = self.getToTalValue(currencies)

    def getNbCurrencies(self):
        fnewWay = [elem for elem in self.way if elem != "NONE"]
        return len(fnewWay)

    def cleanWay(self):
        for i in range (0, len(self.way) - 1):
            for j in range (0, i):
                if safe_list_get(self.way, i, "lol") == safe_list_get(self.way, j, "lol"):
                    self.way[i] = "NONE"

    def __str__(self):
        wayToDisplay = []
        for i in range (len(self.way)):
            wayToDisplay.append(safe_list_get(self.way, i, "lol"))
        return str(wayToDisplay ) + " " + str(self.totalValue) + " " + str(self.nbCurrencies)

    def setWay(self, way):
        self.way = way

    def setTotalValue(self,currency):
        totalValue = 1
        wayWithoutNone = [elem for elem in self.way if elem != "NONE"]
        for i in range (0, len(wayWithoutNone)-1):
            totalValue = totalValue * currency.getRateFromTo(wayWithoutNone[i],wayWithoutNone[i+1]).value
        self.totalValue = totalValue

    def setNbCurrencies(self):
        newWay = [elem for elem in self.way if elem != "NONE"]
        self.nbcurrencies = len(newWay)

    def setIndividuals(self, currency, way):
        self.setWay(way)
        self.cleanWay()
        self.setTotalValue(currency)
        self.setNbCurrencies()

    def clearWayForHtlm(self):
            newWay = []
            for i in range (0, len(self.way)):
                if safe_list_get(self.way, i, "lol") != "NONE":
                    newWay.append( safe_list_get(self.way, i, "lol"))
            self.way = newWay

class Currencies(object):

    tableOfRate = []

    def __init__ (self):
        with open('currencies.json') as data_file:
            res = json.load(data_file)
        for key, value in res.iteritems():
            setattr(self, key, Rate(value, key[0:3], key[4:7]))
        self.EUR_EUR = Rate(1.000000, "EUR", "EUR")
        self.USD_USD = Rate(1.000000, "USD", "USD")
        self.JPY_JPY = Rate(1.000000, "JPY", "JPY")
        self.GBP_GBP = Rate(1.000000, "GBP", "GBP")
        self.CHF_CHF = Rate(1.000000, "CHF", "CHF")
        self.AUD_AUD = Rate(1.000000, "AUD", "AUD")
        self.CNY_CNY = Rate(1.000000, "CNY", "CNY")
        self.HKD_HKD = Rate(1.000000, "HKD", "HKD")
        self.KYD_KYD = Rate(1.000000, "KYD", "KYD")
        self.setTableOfRate()

    def setTableOfRate (self) :
        listOfRate = ["EUR","USD","JPY","GBP","CHF","AUD","CNY","HKD","KYD"]
        for currencyFrom in range(0,len(listOfRate)):
            for currencyTo in range(0,len(listOfRate)):
                self.tableOfRate.append(self.getRateFromTo(listOfRate[currencyFrom],listOfRate[currencyTo]))

    def getRateFromTo(self, fromCurrency, toCurrency):
        return getattr(self, fromCurrency + "_" + toCurrency)

class Index(object):
    def GET(self):
        currencies = Currencies()
        individual = Individual(currencies)
        t0_bellman = time.time()
        cycle = bellmanFord(currencies,9)
        t_final_bellman = time.time() - t0_bellman
        testBellmanFord = Individual(currencies)
        testBellmanFord.setWay(cycle)
        testBellmanFord.setTotalValue(currencies)
        t0_GA = time.time()
        population = Population(currencies)
        population.evolution(currencies)
        res_GA = population.pop
        res_GA.sort(key=lambda x: x.totalValue, reverse=True)
        res_GA_final = res_GA[0]
        res_for_anneal = copy.deepcopy(res_GA_final)
        res_GA_final.clearWayForHtlm()
        t_final_GA = time.time() - t0_GA
        res_anneal_GA = anneal(currencies,9,optional=res_for_anneal)
        t_final_anneal_GA = time.time() - t0_GA
        t0_anneal = time.time()
        res_anneal = anneal(currencies,9)
        t_final_anneal = time.time() - t0_anneal
        data = {"BellmanFord" :{ 'timer': t_final_bellman, 'totalRate':testBellmanFord.totalValue, 'way':testBellmanFord.way },"Annealing" :{ 'timer' : t_final_anneal, 'totalRate':res_anneal.totalValue, 'way':res_anneal.way},
        "GA" :{ 'timer' : t_final_GA, 'totalRate':res_GA_final.totalValue, 'way':res_GA_final.way},"GA_Annealing" :{ 'timer' : t_final_anneal_GA, 'totalRate':res_anneal_GA.totalValue, 'way':res_anneal_GA.way}}
        with open('static/result.js', 'w') as outfile:
                outfile.write("var json =")
                json.dump(data, outfile)
        listOfRate = ["EUR","USD","JPY","GBP","CHF","AUD","CNY","HKD","KYD"]
        return static.index(res = currencies, listOfRate = listOfRate)

if __name__ == "__main__":
    app.run()
