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

#sources = ["twitter.txt"]
sources = ["twitter.txt", "texts/origin-of-species.txt"]

# Get generator objetcs from a list of files
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
			


# Get 140-characters max messages strting with a prefix from the chain
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




class TwitterBot:
	def __init__(self, chain_length=2):
		self.chain = MarkovState()
		self.n = chain_length
	
	def init_from_texts(self, sources):
		self.chain.train(self.n, get_generator_for_files(sources), noparagraphs=True)
	
	def get_tweet_about(self, prefix):
		return(get_characters_about(self.chain, prefix))

	def print_chain_info(self):
		c = self.chain.markov # the Markov object
		occurences = {}
		outdegree = {}
		n_links = 0
		for k in c.data.keys():
			if(c.data[k][0] in occurences.keys()):
				occurences[c.data[k][0]] += 1
			else:
				occurences[c.data[k][0]] = 1
			if(len(c.data[k][1]) in outdegree.keys()):
				outdegree[len(c.data[k][1])] += 1
			else:
				outdegree[len(c.data[k][1])] = 1
			n_links += len(c.data[k][1])
		print("That chain is composed of "+str(self.n)+"-grams (and shorter)")
		print(str(len(c.data.keys()))+" nodes and "+str(n_links)+" links in the graph:")
		ok = list(occurences.keys())
		ok.sort(reverse=True)
		odk = list(outdegree.keys())
		odk.sort(reverse=True)
		print("Occurence statistics:\n---------------------")
		for n in ok:
			print(str(occurences[n])+" n-grams were encountered "+str(n)+" times")
		print("Outdegree statistics:\n---------------------")
		for n in odk:
			print(str(outdegree[n])+" nodes have an outdegree of "+str(n))
	
	def print_ngram_info(self, ngram):
		ng = ngram
		if(len(ngram) > self.n):
			i = len(ngram) - self.n
			ng = ngram[i:]
			print("WARNING: truncating "+str(ngram)+" to "+str(ng)+" because it is longer than the chain length of "+str(self.n))

		if(ngram not in self.chain.markov.data.keys()):
			print("n-gram "+str(ng)+" does not appear in the chain")
		else:
			node = self.chain.markov.data[ng]
			print("n-gram "+str(ng)+" occured "+str(node[0])+" times in training set and has an outdegree of "+str(len(node[1])))
			print("Outer connectivity:")
			ok = list(node[1].keys())
			ok.sort()
			for k in ok:
				print("* "+str(k)+" : "+str(node[1][k])+" ("+str(int(round((100*node[1][k]/float(node[0])))))+"%)")


	def mutate_links_weights(self, p_mutation, mutation_power):
		"""Mutate the links weights.
    		Each link has a probability p_mutation to be affected.
	    	mutation_power is the gaussian mutation strength,
		relative to the existing weight (= big weights will be more
		altered than small ones in any way)
		"""
		n_mutated = 0
		for k in self.chain.markov.data.keys(): # For each node
			delta_total = 0
			for k2 in self.chain.markov.data[k][1].keys(): # For each link
				if(random.random() < p_mutation):
					original_v = self.chain.markov.data[k][1][k2]
					delta = int(round(random.gauss(0.,mutation_power*original_v))) # mutation_power is a coefficient of variation
					self.chain.markov.data[k][1][k2] += delta
					delta_total += delta
					n_mutated += 1
			self.chain.markov.data[k][0] += delta_total # adjust number of occurences
		print("Links mutation done. "+str(n_mutated)+" links were altered.")


def main():
	b = TwitterBot(2)
	b.init_from_texts(sources)
	print("Done init. Testing:")
#	b.print_chain_info()
#	b.print_ngram_info(("evolution","of"))
	b.mutate_links_weights(0.05,0.5)
	for topic in topics:
		b.print_ngram_info(tuple(topic.split()))
		print ("According to Twitter and Charles Darwin, here is some stuff about "+topic+":")
		print(b.get_tweet_about(topic)+"\n")
		time.sleep(1)


if __name__ == "__main__":
	main()
