#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" Alexandre Coninx
    Imperial College London, 04/03/2014
""" 

from markovstate import MarkovState
import time

topics = ("evolution","Darwin","natural selection","survival of the fittest")




def main():
	chain = MarkovState()

	print("Initializing Markov chain...")
	trainingdata = open("twitter.txt")
	chain.train(2,trainingdata,True)
	trainingdata.close()
	chain.dump("foo.markov")
	print("Done init. Testing:")
	for topic in topics:
		print ("According to Twitter, here is some stuff about "+topic+":")
		print (chain.generate(5))
		time.sleep(1)
	






if __name__ == "__main__":
	main()
