#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" Alexandre Coninx
    Imperial College London, 04/03/2014
""" 

from markovstate import MarkovState
import time
import fileinput
import glob
import os
import random


topics = ("evolution","Darwin","natural selection","survival of the fittest")

sources = ["twitter.txt"]


def get_generator_for_files(files):
	paths = [path
		for ps in files
		for path in glob.glob(os.path.expanduser(ps))]

	def charinput(paths):
		with fileinput.input(paths) as fi:
			for line in fi:
				for char in line:
					yield char
	return charinput(paths)
			


def get_characters_about(chain, prefix, nmax=140):
	# Abide by the 140 charcters limit
	sentence = prefix+" "
	s = int(time.time())
	chunk = chain.generate(chunks=1, seed=s, prefix=tuple(prefix.split()))
	sentence += chunk
	while True:
		chunk = chain.more()
		if(len(sentence) + len(chunk) + 1 > nmax):
			break
		else:
			sentence += (" "+chunk)
	return sentence





def main():
	chain = MarkovState()
	print("Initializing Markov chain...")
	chain.train(2,get_generator_for_files(sources),noparagraphs=True)
	print("Done init. Testing:")
	for topic in topics:
		print ("According to Twitter, here is some stuff about "+topic+":")
		print(get_characters_about(chain, topic)+"\n")
		time.sleep(1)
	






if __name__ == "__main__":
	main()
