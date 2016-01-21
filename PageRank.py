#!/usr/bin/python

from collections import namedtuple
import time
import sys
import random
import operator

class Airport:
    def __init__ (self, iden=None, name=None):
        self.code = iden
        self.name = name
        self.outweight =  0
        self.pageRank = 0

    def __repr__(self):
        return "Code: {0}\t PageRank: {1}\t  Out Weight: {2}\n".format(self.code,self.pageRank,self.outweight)

edgeHash = dict() # hash of edge to ease the match
airportList = [] # list of Airport
airportHash = dict() # hash key IATA code -> Airport

def readAirports(fd):
	print "Reading Airport file from {0}".format(fd)
	airportsTxt = open(fd, "r");
	cont = 0
	for line in airportsTxt.readlines():
		a = Airport()
		try:
			cont += 1
			temp = line.split(',')
			if len(temp[4]) != 5 :
				raise Exception('not an IATA code')
			a.name=temp[1][1:-1] + ", " + temp[3][1:-1]
			a.code=temp[4][1:-1]
			airportList.append(a)
			airportHash[a.code] = a
			edgeHash[a.code] = dict()
		except Exception as inst:
			pass
	airportsTxt.close()
	print "There were {0} Airports with IATA code".format(cont)


def readRoutes(fd):
	print "Reading Routes file from {0}".format(fd)
	routesTxt = open(fd, "r");
	cont = 0
	for line in routesTxt.readlines():
		try:
			temp = line.split(',')
			if len(temp[4]) != 3 :
				raise Exception('not an IATA code')
			if len(temp[2]) != 3 :
				raise Exception('not an IATA code')
			OriginAirport=temp[2]
			DestinyAirport=temp[4]
			if OriginAirport in airportHash.keys() and DestinyAirport in airportHash.keys():
				cont += 1
				airportHash[OriginAirport].outweight = airportHash[OriginAirport].outweight + 1
				if OriginAirport in edgeHash[DestinyAirport].keys():
					edgeHash[DestinyAirport][OriginAirport] = edgeHash[DestinyAirport][OriginAirport] + 1
				else:
					edgeHash[DestinyAirport][OriginAirport] = 1
		except Exception as inst:
			pass		
	routesTxt.close()
	print "There were {0} Routes with IATA code".format(cont)


def distribuirRank() :
	for a in airportHash:
		if airportHash[a].outweight == 0 : 
			aux = random.choice(airportHash.keys())
			edgeHash[aux][a] = 1
			airportHash[a].outweight = 1
			
def converge(vec1, vec2, n) :
 # n indica el numero de decimales a comparar
	for a in vec1.keys():
		if round(vec1[a],n) != round(vec2[a],n) : 
			return False
	return True

def computePageRanks():
    n = len(airportHash.keys())
    P = dict()
    for i in airportHash.keys():
		P[i] = 1.0/n
    L = 0.85
    stopping_condition = False
    while (not stopping_condition):
		time1 = time.time()
		Q = dict()
		for node in airportHash.keys():
			Q[node] = 0

		for dest in edgeHash.keys() :
			total = 0.0
			for org in edgeHash[dest].keys() :
				w = edgeHash[dest][org]
				out = airportHash[org].outweight
				total = total + P[org]*w/out
			Q[dest] = L*total+(1-L)/n

		if converge(P,Q,9):
			stopping_condition = True
			for j in airportHash.keys() :
				airportHash[j].pageRank = P[j]
		P = Q
		time2 = time.time()
		print sum(P.values())
		

def outputPageRanks():
	pageranks = []
	for j in airportHash.keys() :
		pageranks.append((airportHash[j].pageRank,airportHash[j].code))
	pageranks.sort(key=operator.itemgetter(0),reverse=True)
	f = open('pageranks.txt', 'w')
	for p in pageranks :
		f.write(str(p))
		f.write('\n')
	f.close()


def main(argv=None):
	time1 = time.time()
	readAirports("airports.txt")
	readRoutes("routes.txt")
	time2 = time.time()
	print "Time for reading airports and routes:", time2-time1
	
	time1 = time.time()
	distribuirRank()
	computePageRanks()
	time2 = time.time()
	print "Time for computing pagerank:", time2-time1
	
	time1 = time.time()
	outputPageRanks()
	time2 = time.time()
	print "Time for writing pagerank:", time2-time1


if __name__ == "__main__":
	sys.exit(main())
