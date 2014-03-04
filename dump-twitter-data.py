#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Alexandre Coninx
    Imperial College London, 04/03/2014
""" 

import twitter
import codecs

topics = ("evolution","Darwin","natural selection","survival of the fittest")

filename = "twitter.txt"


def main():
	api =  twitter.Api(consumer_key='XKQ0jsxPiDcUuGZjU2nYSA',
			consumer_secret='jU4xkJlOg9j3tQi3UCY80TVUGu4MBsHjXpVSD31TQY',
			access_token_key='2349861931-AuTecfyzW3aSvinkywuD65RHD4U1vhYktePSEOi',
			access_token_secret='84dFSLjIfj8f2894tzLEXlUFbRhGPA4qeCEAGo1CW2Rx7')

	f = codecs.open(filename,'w','utf-8')
	for topic in topics:
		tweets = api.GetSearch(term=topic, lang='en', count=1000)
		print(str(len(tweets))+" tweets found about "+topic)
		for t in tweets:
			f.write(t.text)
	f.close()
	






if __name__ == "__main__":
	main()
