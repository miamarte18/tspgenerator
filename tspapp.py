#TSP project
#Purpose: From the starting point of the path, we wanna find the shorterst path of the distance.
#Last day edited: 6/20/2023
#Autors: Mia Marte, Sofia Torres, Stephanie Saenz

import random
from math import sqrt
import streamlit as st 

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path
 

cityL = []
demographic = []

with st.container():
    
    st.title('Travelling salesman problem')
    st.subheader("Project 2 by Sofia Torres, Stephanie Seanz, and Mia Marte")
    st.write("Using the travelling salesman problem we incorporate generic algorithms to find\n the shortest path of the distance from the starting point ")


class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, city):
        xdis = abs(self.x - city.x)
        ydis = abs(self.y - city.y)
        dis = sqrt((xdis**2) + (ydis**2))
        return dis

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"
n = st.slider('How many destinations to generate?', 5, 200, 5)
class Fitness:
    def __init__(self, route):
        self.route = route
        self.dis = 0
        self.fit = 0

    def routeDistance(self):
        if self.dis == 0:
            pathDis = 0
            # looping through route to calculate distance
            for i in range(0, len(self.route)):
                fromCity = self.route[i]
                toCity = None
                if i + 1 < len(self.route):
                    # getting next city in route
                    toCity = self.route[i + 1]
                else:
                    # returning to start city
                    toCity = self.route[0]
                pathDis += fromCity.distance(toCity)
            self.dis = pathDis
        return self.dis

    def fitnessScore(self):
        if self.fit == 0:
            self.fit = 1/float(self.routeDistance())
        return self.fit

def plotCities():
    x = [cities.x for cities in cityL]
    y = [cities.y for cities in cityL]
    plt.scatter(x, y)
    plt.plot(x, y)
    plt.xlabel("X values")
    plt.ylabel("Y values")
    plt.show()


def initValues(size):
    # Initial City List
    for i in range(0, 25):
        cityL.append(City(x=int(random.random()*200),
                        y=int(random.random()*200)))

    # Initial demographic
    for i in range(0, size):
        demographic.append(createRoute())

def createRoute():
    route = random.sample(cityL, len(cityL))
    return route


def rankRoutes():
    results = {}

    for i in range(0, len(demographic)):
        results[i] = Fitness(route=demographic[i]).fitnessScore()

    return sorted(results.items(), key=lambda kv: kv[1], reverse=True)


def slection(rankedList, size):
    selectionResults = []

    for i in range(0, size):
        selectionResults.append(rankedList[i][0])
    for i in range(0, len(rankedList) - size):
        player_1 = random.randint(0, len(rankedList)-1)
        player_2 = random.randint(0, len(rankedList)-1)
        if rankedList[player_1][1] >= rankedList[player_2][1]:
            selectionResults.append(rankedList[player_1][0])
        else:
            selectionResults.append(rankedList[player_2][0])

    return selectionResults

def matingPool(demographic, selectionResults):
    pool = []

    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        pool.append(demographic[index])
    return pool


def breed(p1, p2):
    child = []
    childP1 = []
    childP2 = []

    # ordered crossover
    geneA = int(random.random() * len(p1))
    geneB = int(random.random() * len(p1))

    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(p1[i])

    childP2 = [gene for gene in p2 if gene not in childP1]

    child = childP1 + childP2
    return child

def breedPop(pool, size):
    children = []
    total = len(pool) - size
    sameplePool = random.sample(pool, len(pool))

    # using elitism
    for i in range(0, size):
        children.append(pool[i])

    # breed for rest of pool
    for i in range(0, total):
        child = breed(sameplePool[i], sameplePool[(len(pool) - i) - 1])
        children.append(child)
    return children


def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))

            city1 = individual[swapped]
            city2 = individual[swapWith]

            individual[swapped] = city2
            individual[swapWith] = city1
    return individual

def mutatedemographic(children, mutationRate):
    mutatedPop = []

    for i in range(0, len(children)):
        mutated = mutate(children[i], mutationRate)
        mutatedPop.append(mutated)
    return mutatedPop


def nextGeneration(currentGen, eliteSize, mutationRate):
    rankedList = rankRoutes()
    selectionResults = slection(rankedList, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPop(matingpool, eliteSize)
    nextGeneration = mutatedemographic(children, mutationRate)
    return nextGeneration
def geneAlgo(popSize, eliteSize, mutationRate, generations):
    global demographic
    initValues(popSize)
    progress = []
    print("The initial distance is: " + str(1 / rankRoutes()[0][1]))
    progress.append(1 / rankRoutes()[0][1])

    for i in range(0, generations):
        demographic = nextGeneration(demographic, eliteSize, mutationRate)
        progress.append(1 / rankRoutes()[0][1])

    print("The final distance is: " + str(1 / rankRoutes()[0][1]))
    bestRouteIndex = rankRoutes()[0][0]
    bestRoute = demographic[bestRouteIndex]
    fig, axs = plt.subplots(2)
   

    axs[0].plot(progress)
    axs[0].set_title("Progress Graph")
    #axs[1].set_ylabel('\nDistance\n')
    

    x = [cities.x for cities in bestRoute]
    x.append(bestRoute[0].x)
    y = [cities.y for cities in bestRoute]
    y.append(bestRoute[0].y)
 
    axs[1].set_title("Final Path Graph")
    axs[1].scatter(x, y)
    axs[1].plot(x, y)
    axs[1].set_xlabel("X values")
    axs[1].set_ylabel("Y values")

    plt.tight_layout()
    plt.show()
    return bestRoute
if __name__ == '__main__':
    print("Start")

    initValues(size=25)
    plotCities()
    bestRoute = geneAlgo(popSize=100, eliteSize=20,
                         mutationRate=0.01, generations=500)
    
    cityL = []
    for i in range (0, 25):
        cityL.append(City(x=int(random.random() * 200), y=int(random.random() *200)))
