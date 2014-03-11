twitter-ga
==========

Genetic algorithms and twitter stuff.


What you need
-------------
* You will need python3
* That code depends on sixohsix's Python3 twitter API. It is included in the repository as a subodule. In order to use it you will need to do the following after cloning/pulling from the twitter-ga repository:

	cd twitter-ga
	git submodule init
	git submodule update


How to test stuff
-----------------
* Edit markov-twitter.py. In the "configuration" section you will find the sourcs on which the Markov chain will be trained. You can specify:
  * Text sources, by default Darwin's *On the Origin of Species*
  * Twitter topics which will be searched, by default: "evolution", "Darwin", "natural selection" and "survival of the fittest"
* Run markov-twitter.py to generate tweets about those topics, based on the training material. (Nothing is actually tweeted, tweets are only printed.)

References
----------
* Bot IRC Triplie-NG : https://github.com/spion/triplie-ng/
* King James Programming : http://kingjamesprogramming.tumblr.com/
* Et le code qui va derriere : https://github.com/Barrucadu/markov
* Library twitter compatible Python 3 : https://github.com/sixohsix/twitter
* Doc officielle de l'API twitter : https://dev.twitter.com/doc
