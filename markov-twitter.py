#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" Alexandre Coninx
    Imperial College London, 04/03/2014
""" 

from markovstate import MarkovState
import codecs

topics = ("evolution","Darwin","natural selection","survival of the fittest")




def main():
	chain = MarkovState()

	print("Initializing Markov chain...")
	trainingdata = codecs.open("twitter.txt",'r','utf-8')
	chain.train(3,trainingdata,True)
	trainingdata.close()
#	chain.dump("foo.mkv")
	print("Done init. Testing:")
	for topic in topics:
		print ("According to Twitter, here is some stuff about "+topic+":")
		print (chain.generate(1))
	






if __name__ == "__main__":
	main()
