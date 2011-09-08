#!/usr/bin/python2
import xmpp,sys,time,os,re
from urllib import urlopen
import urllib, json
from difflib import context_diff,ndiff
from itertools import chain

# Variablen:

greeting="The diff-bot on joip.de is reporting changes!"
pause=60
kurs=7

login = 'bot' # @gmail.com 
pwd   = 'xxxxxxxxxx'

cnx = xmpp.Client('joip.de')
cnx.connect( server=('joip.de',5222) )
cnx.auth(login,pwd,'joip.de Server monitoring mtGox.')
cnx.sendInitPresence()



while (True):
	"""Returns latest mtGox USD rate"""
	# Get a file-like object for the Python Web site's home page.
	f = urllib.urlopen('http://mtgox.com/api/0/data/ticker.php')
	# Read from the object, storing the page's contents in 's'.
	line=f.read();
	u=line.decode('utf-8');
	s = json.loads(u)
	oldkurs=kurs
	kurs=s['ticker']['last']
	kurs_str=str(kurs)
	kurs_str += ' USD'
	f.close()
	
	if kurs != oldkurs:
		if oldkurs<kurs:
			pres = xmpp.Presence()
			pres.setStatus(kurs_str + " +")
		else:
			pres = xmpp.Presence(show='dnd')
			pres.setStatus(kurs_str + " -")
		cnx.send(pres)
	else:
		pres.setStatus(kurs_str + " =")
                cnx.send(pres)		
	
#	cnx.send( xmpp.Message( 'jo@joip.de' , repr(kurs_str) ) )
	print("updated: %s" %(kurs_str))
	time.sleep(int(pause))

cnx.disconnect()


