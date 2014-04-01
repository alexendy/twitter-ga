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
import sys
import copy
import re
import sys

sys.path.append("lib/twitter")
from twitter import *

# Configuration
# =============

# Twitter topics for initial chain training
topics = ("#evolution","#Darwin","#naturalSelection","#survivalOfTheFittest")
#topics = () # Train only from texts

# Textual sources for initial
#sources = ["texts/origin-of-species.txt"]
sources = [] # Train only from Twitter

# Twitter topics on which the chain will be tested
query_topics = ("evolution", "Darwin", "natural selection")

# Learning depth.
# Higher = more coherence
# Lower = more diversity
chain_depth = 2

# Do we include HTTP(S) links in the Markov chain ?
nohttp = True

# Do we include hashtags in the Markov chain ?
nohashtags = False

# Do we include @users tags in the Markov chain ?
noatuser = True

# ============




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

def tweet_to_asciistring(tweet, no_http=True, no_hashtags=False, no_at_user=False):
	string = tweet['text'].encode('UTF-8').decode("ascii","ignore") # Brutally convert to ASCII
	string = re.sub('\n',' ',string)
	if(no_http):
		string = re.sub(r'http(s)?://\S+',r'',string)
	if(no_hashtags):
		string = re.sub(r'#\S+',r'',string)
	if(no_at_user):
		string = re.sub(r'@\S+',r'',string)
	return string.strip()
	

class TwitterBot:
	def __init__(self, chain_length=2):
		self.chain = MarkovState()
		self.n = chain_length
		self.seed = time.time()
		self.twitter = Twitter(auth=OAuth('2349861931-AuTecfyzW3aSvinkywuD65RHD4U1vhYktePSEOi', # OAUTH_TOKEN
					'84dFSLjIfj8f2894tzLEXlUFbRhGPA4qeCEAGo1CW2Rx7', # OAUTH_SECRET
					'XKQ0jsxPiDcUuGZjU2nYSA', # CONSUMER_KEY
					'jU4xkJlOg9j3tQi3UCY80TVUGu4MBsHjXpVSD31TQY')) # CONSUMER_SECRET
		self.chain_initialized = False
	
	def clone(self):
		return copy.deepcopy(self)

	def train_chain(self, gen, noparagraphs):
		if(self.chain_initialized):	
			self.chain.train_more(gen, noparagraphs)
		else:
			self.chain.train(self.n, gen, noparagraphs)
		self.chain_initialized = True

	def train_from_texts(self, sources):
		self.train_chain(get_generator_for_files(sources), noparagraphs=True)
	


	def train_from_twitter(self, topics, lang='en', n_min_per_tweet=200, no_http=True, no_hashtags=False, no_at_user=False):
		def get_twitter_generator(api, tpcs, l, c, nlinks, nh, nat):
			for tp in tpcs:
				reply = api.search.tweets(q=tp,lang=l,count=100)
				tweet_count = len(reply['statuses'])
				if(tweet_count == 0):
					print("WARNING: Twitter did not return anu tweet for {}. Maybe the number of requests available is exhausted. Will not use that topic for learning )".format(tp))
					continue

				for t in reply['statuses']:
					string = tweet_to_asciistring(t, nlinks, nh, nat)
					for char in string:
						yield char

				while (tweet_count < c):
					last_id = min([t['id'] for t in reply['statuses']])
					reply = api.search.tweets(q=tp,lang=l,count=100,max_id=(last_id - 1))
					if(len(reply['statuses']) == 0):
						print("WARNING: Could not find enough tweets for {} (Twitter returned zero tweets before ID {})".format(tp,last_id))
						break
					tweet_count += len(reply['statuses'])
					for t in reply['statuses']:
						string = tweet_to_asciistring(t, nlinks, nh, nat)
						for char in string:
							yield char
				print(str(tweet_count)+" tweets about "+tp)
		self.train_chain(get_twitter_generator(self.twitter, topics, lang, n_min_per_tweet, no_http, no_hashtags, no_at_user), noparagraphs=True)

		

	def renew_seed(self):
		sr = random.SystemRandom()
		self.seed = sr.randint(0,1000000000)

	def get_tweet_about(self, prefix, nchar=140):
		# Abide by the 140 charcters limit
		self.renew_seed()
		sentence = prefix+" "
		chunk = self.chain.generate(chunks=1, seed=self.seed, prefix=tuple(prefix.split()))
		sentence += chunk
		while True:
			chunk = self.chain.more()
			if(len(sentence) + len(chunk) + 1 > nchar):
				break
			else:
				sentence += (" "+chunk)
		return sentence


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
	print("Instantiating TwitterBot and connecting to Twitter...")
	b = TwitterBot(chain_depth)
	if(sources):
		print("Training the bot from text sources: "+str(sources))
		b.train_from_texts(sources)
	if(topics):
		print("Training the bot from twitter. Topics: "+str(topics))
		b.train_from_twitter(topics, 'en', 200, nohttp, nohashtags, noatuser)
	print("Done with training.")
	
#	print("Chain statistics :")
#	b.print_chain_info()

	print("Mutating weights...")
	b.mutate_links_weights(0.05,0.5)

	print("All done. Testing the chain output:")
	for topic in query_topics:
		#b.print_ngram_info(tuple(topic.split()))
		print ("According to Twitter, and Charles Darwin, here is some stuff about "+topic+":")
		for i in range(5):
			print("- "+b.get_tweet_about(topic))
		print("\n")


if __name__ == "__main__":
	main()
