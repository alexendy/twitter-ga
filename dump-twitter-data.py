#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" Alexandre Coninx
    Imperial College London, 04/03/2014
""" 

import importlib.machinery
import codecs
import sys

sys.path.append("lib/twitter")

from twitter import *


topics = ("evolution","Darwin","natural selection","survival of the fittest")

filename = "twitter.txt"


def main():
	api =  Twitter(auth=OAuth('2349861931-AuTecfyzW3aSvinkywuD65RHD4U1vhYktePSEOi', # OAUTH_TOKEN
			'84dFSLjIfj8f2894tzLEXlUFbRhGPA4qeCEAGo1CW2Rx7', # OAUTH_SECRET
			'XKQ0jsxPiDcUuGZjU2nYSA', # CONSUMER_KEY
			'jU4xkJlOg9j3tQi3UCY80TVUGu4MBsHjXpVSD31TQY')) # CONSUMER_SECRET
			

	f = open(filename,'w')
	for topic in topics:
		r = api.search.tweets(q=topic,lang='en',count=150)
		tweets = r['statuses']
		print(str(len(tweets))+" tweets found about "+topic)
		for t in tweets:
			# Brutally convert to ASCII
			asciidata=t['text'].encode('UTF-8').decode("ascii","ignore")
			f.write(asciidata+'\n')
	f.close()
	






if __name__ == "__main__":
	main()
