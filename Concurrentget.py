#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread
import sys
from Queue import Queue
from time import sleep, time
from collections import defaultdict # para convertir a array
import urllib2,json
from Configuracion import cookieexpresssid

global ws

def _contarunapagina(String):
	#print data
	listausuario=[]
	data  = json.loads(String)
	for l in data["posts"]:
		#print l 
		if l["user"]["userslug"]=="": l["user"]["userslug"]="Invitado"
		listausuario.append(l["user"]["userslug"].encode('utf8'))
	
	d = defaultdict(int)
	a = listausuario
	for i in a:
		d[i] += 1
	return d

def doWork():
	while True:
		url = q.get()

		req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0','Cookie':'express.sid='+cookieexpresssid})
		while True:
			try:
				#print "Solicitando la url"
				f= urllib2.urlopen(req,timeout=4)
				break
			except:
				#print "No se ha podido solicitar"
				#sleep(0)
				continue
			
			
		result= _contarunapagina(f.read())
		#print url, result
		String.append(result)
		f.close()
		#return f.read()
		q.task_done()

def _getsimultaneo(arrurl,concurrent = 200):
	print "_getsimultaneo: INICIO"
	results = [{} for x in arrurl]
	global results
	#print arrurl
	#print "_getsimultaneo: Concurrencia",concurrent
	global q
	String =[]
	global String
	q = Queue(concurrent * 2)
	for i in range(concurrent):
		t = Thread(target=doWork)
		t.daemon = True
		t.start()
	
	timeout=60
	try:
		print "_getsimultaneo: Haciendo el put"
		for url in arrurl:
			q.put(url.strip())
		
		stop = time() + timeout
		print "_getsimultaneo: Put hecho. Esperando a que las tareas terminen"
		while q.unfinished_tasks>0 and time()<stop:
			print "_getsimultaneo: Tiempo restante %d. Tareas restantes %d" %(stop-time(), q.unfinished_tasks)
			sleep(1)
	except KeyboardInterrupt:
		sys.exit(1)
	
	#try:
	#	for url in arrurl:
			#q.put(url.strip())
		#print "y ahora el qjoin"
		#q.join()
	#except KeyboardInterrupt:
		#sys.exit(1)
	
	#print String
	#with open("Output.txt", "w") as text_file:
	#	for element in String:
	#		text_file.write("%s\n" % element)
	
	print "_getsimultaneo: FIN _getsimultaneo"
	return String