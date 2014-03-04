#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Alexandre Coninx
    Imperial College London, 04/03/2014
""" 

import numpy as np

import twitter
import markov







def main():
	chain = markov.Markov()
	print "Loading sources..."
	chain.load("texts/origin-of-species.txt")
	print "Done"

	api =  twitter.Api(consumer_key='XKQ0jsxPiDcUuGZjU2nYSA',
			consumer_secret='jU4xkJlOg9j3tQi3UCY80TVUGu4MBsHjXpVSD31TQY',
			access_token_key='2349861931-AuTecfyzW3aSvinkywuD65RHD4U1vhYktePSEOi',
			access_token_secret='84dFSLjIfj8f2894tzLEXlUFbRhGPA4qeCEAGo1CW2Rx7')

	tweets = api.GetSearch(term='evolution', count=200)
	print str(len(tweets))+" tweets found about evolution"
	for t in tweets:
		print "* "+t.text





if __name__ == "__main__":
	main()
