#!/usr/bin/python2
import xmpp,sys,time,os,re
from urllib import urlopen
import urllib, json, time
from difflib import context_diff,ndiff
from itertools import chain

# Variablen:

greeting="The diff-bot on joip.de is reporting changes!"
pause=60
kurs=7
waitcounter=1

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

	#only ask for daily averages every thrity minutes
	waitcounter-=1
	if (waitcounter==0):
		try:
			f2= urllib.urlopen('http://bitcoincharts.com/t/weighted_prices.json')
			bitcoincharts=f2.read();
			f2.close()
			bitcoincharts=bitcoincharts.decode('utf-8')
			bitcoincharts = json.loads(bitcoincharts)
		except:
			bitcoincharts = dict({'USD': {'24h' : 'NaN'}, 'EUR': {'24h' : 'NaN'}})
			print('error loading bitcoincharts data')
		waitcounter=30

	# Read from the object, storing the page's contents in 's'.
	try:
		mtgox=f.read();
		mtgox=mtgox.decode('utf-8');
		mtgox = json.loads(mtgox)
		oldkurs=kurs
		kurs=mtgox['ticker']['last']
	except:
		print('error loading mtgox data')
		kurs='NaN'			
	kurs_str=str(kurs)
	kurs_str += ' USD'

	kurs_str +=' | 24h: ' + bitcoincharts['USD']['24h'] + ' USD, ' + bitcoincharts['EUR']['24h'] + ' EUR'
	
	
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
	print("%f: updated: %s" %(time.time(), kurs_str))
	time.sleep(int(pause))

cnx.disconnect()


