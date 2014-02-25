#!/usr/bin/env python
# -*- coding: utf-8 -*-
#on va pas détailler.

import twitter #library python-twitter proposé par david
import random 
import time 

api = twitter.Api(consumer_key='XKQ0jsxPiDcUuGZjU2nYSA',
consumer_secret='jU4xkJlOg9j3tQi3UCY80TVUGu4MBsHjXpVSD31TQY', access_token_key='2349861931-AuTecfyzW3aSvinkywuD65RHD4U1vhYktePSEOi', access_token_secret='84dFSLjIfj8f2894tzLEXlUFbRhGPA4qeCEAGo1CW2Rx7')

withBact=api.GetSearch(term='bacteria',count=200)


print len(withBact)

answer=["We run the world!","Never forget : archaea>bacteria>eukarya","don't mess with us","here we are!","everywhere","we are the proud","we are legion","in archaea god trusts","at the begining there was archaea","socrate was an archaea","to be [an archaea] or not to be","one archaea to rule them all","kernel sucks","we don't forgive", "don't think we are bacteria","archaea!!!!!!!","trust us!","love us!","bacteria are for archaea  what internet is for /b/","yes","present","I'm here","We are here","check!","archaea rocks","Why should we wear kernel? stupid fashion","hihi","youla!","forza!","power","force","honneur","proud","mefiez vous de l'eau qui dort","yes?"]

random.shuffle(withBact)

for i in withBact:
	print i.user.screen_name,";",i.GetText()
	print "--------------------------------"
	val=random.randint(0,len(answer)-1)	
	newstatus= "@"+i.user.screen_name+" "+answer[val]
	api.PostUpdate(status=newstatus,in_reply_to_status_id=i.id)
	time.sleep(900)
