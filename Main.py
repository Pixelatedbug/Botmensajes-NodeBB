#!/usr/bin/env python
# -*- coding: utf-8 -*-

import websocket
from time import sleep, time
from Configuracion import cookieexpresssid, nickdelbot
from Listarusuarios import _tabladeusuarios
from Vernotificaciones import _getnotificaciones
import json, re

#import os #para usar nice
#os.nice(0)


from threading import Thread
import sys  

#definimos el juego de car?cteres unicode
reload(sys)  
sys.setdefaultencoding('utf8')

unmensajecadamaxsegundos=10

global ws
ws = websocket.WebSocket()

ultimoenviado=0 #Esta variable la utilizaremos para marcar cuando fue la ?ltima vez que se envi? un mensaje, para esperar los 15 segundos
arraynotificaciones=[]



class ThreadingRecv(object):
	
	
	def __init__(self, interval=0.7):
		""" Constructor
		:type interval: int
		:param interval: Check interval, in seconds
		"""
		self.interval = interval

		thread = Thread(target=self.run, args=())
		thread.daemon = True							# Daemonize thread
		thread.start()								  # Start the execution

	def recuperarconexion(self,ws):
		ws.close()
		return ws.connect("wss://exo.do/socket.io/?EIO=3&transport=websocket",	cookie="express.sid=" + cookieexpresssid)	
	
	def run(self):
		
		""" Method that runs forever """
		print "Main: ESPERANDO NOTIFICACIONES..."
		result=""
		while True:
			try:
				ws.send("2")
				result =  ws.recv()
			except:
				i=0
				print "Main: Conexi?n perdida tratando de recuperarla...."
				#@retry(urllib2.URLError, tries=20, delay=30, backoff=2)
				#self.recuperarconexion(ws)
				while True:
					try:
						sleep(4)
						ws.close()
						ws.connect("wss://exo.do/socket.io/?EIO=3&transport=websocket",	cookie="express.sid=" + cookieexpresssid)	
					except:
						print "Main: Conexi?n perdida tratando de recuperarla.... Intento %d " %i
						i+=1
						continue
					print "Main: Conexi?n recuperada"
					break
					
			
			#print result
			if result != '3' and result.find("notifications:user_mentioned_you_in")>0 and result.find(""""path":"/chats""")==0:
				#print str(i) + " -/-"
				print "Main: ", result
				m =re.search('^\d*\["event:new_notification",([\S\s]*)]',result)
				if m is not None:
					resultjson= m.group(1)
					data  = json.loads(resultjson)
					try: 
						print "Main: ", resultjson
						print "Main: ", data["bodyLong"]
					except UnicodeEncodeError:
						print u"No se puede imprimit el mensaje por tener car?cteres no unicode"
						
					m = re.search('@'+nickdelbot+'\s{1,5}([0-9]+)',data["bodyLong"])
					m2 = re.search('@'+nickdelbot+'\s{1,5}http[s]?:\/\/exo\.do\/topic\/([0-9]+)\/',data["bodyLong"])

					hilosolicitado=""
					if m2 is not None:
						hilosolicitado= m2.group(1)
					elif m is not None:
						hilosolicitado= m.group(1)
					
					print "Main: hilo solicitado", hilosolicitado
					if hilosolicitado!="":
						resptid=data["tid"]
						#usuario=data["user"]["userslug"]
						print "Main: ", resptid
						arraynotificaciones.append([hilosolicitado,resptid,''])
					print "Main: Esperando..."
						
			sleep(self.interval)

#Creamos el objeto websockets

print "Main: Comprobando notificaciones"
arraynotificaciones=_getnotificaciones()
print "Main: Notificaciones a enviar:"
print arraynotificaciones
print "Main: ************"


#ABRIMOS LA CONEXI?N 
ws.connect(	"wss://exo.do/socket.io/?EIO=3&transport=websocket",cookie="express.sid=" + cookieexpresssid)
ws.send("""4290["notifications.markAllRead"]""")
threadping = ThreadingRecv()


#result =  ws.recv()
#print "Main: Received '%s'" % result
print "Main: INICIANDO"
#ws.send("""421["posts.reply",{"tid":24417,"content":"asdf\nasdf\nasdf\ndf","lock":"false"}]""")
#ws.send("""421["posts.reply",{"tid":'24417',"content":'Usuario | Nº Post en hilo \r\n|-----|----| \r\n asdf',"lock":"false"}]""")


while True:
	try:
		segundosrestantes= time()-ultimoenviado
		if len(arraynotificaciones)>0: print "Main: Segundos restantes " + str(int(segundosrestantes)) + ". Arraynotificaciones: ", arraynotificaciones
		if len(arraynotificaciones)>0 and segundosrestantes>unmensajecadamaxsegundos:
		
			hilosolicitado,resptid,usuario = arraynotificaciones.pop(0)
			
			respcont=_tabladeusuarios(hilosolicitado)
			comillas = '"'
			if respcont != -1:	
				#if time()-ultimoenviado<8: sleep(8-time()+ultimoenviado)
								
				print "Main: " +"""421["posts.reply",{"tid":"""+comillas+str(resptid)+comillas+""","content":""" +comillas+respcont +comillas + ""","lock":"false"}]"""
				if usuario=="":
					ws.send("""425["posts.reply",{"tid":"""+comillas+str(resptid)+comillas+""","content":""" +comillas+respcont +comillas + ""","lock":"false"}]""")
				else:
					ws.send("""425["posts.reply",{"tid":"""+comillas+str(resptid)+comillas+""","content":"""+comillas+r"@"+usuario+" "+respcont +comillas + ""","lock":"false"}]""")
				ultimoenviado=time()
				print "Main: ***FIN del loop, mensaje enviado."
				continue
			else:
				ws.send("""425["posts.reply",{"tid":"""+comillas+str(resptid)+comillas+""","content": "No puedo conseguir el hilo ["""+ str(hilosolicitado) + r"]("+ r"//exo.do/topic/"+str(hilosolicitado)+")"+ comillas+ ""","lock":"false"}]""")
				print "Main: ***FIN. Reseteamos el loop porque el error era -1."
				continue
		sleep(1)
	except KeyboardInterrupt:
		ws.close()
		break

#11446 Received '42["event:new_notification",{"bodyShort":"[[notifications:user_mentioned_you_in, kNN, eaeaea]]","bodyLong":"@pixel te menciono","nid":"tid:24417:pid:770097:uid:5919:user","pid":770097,"tid":24417,"from":5919,"path":"/post/770097","importance":6,"datetime":1471963895463}]'