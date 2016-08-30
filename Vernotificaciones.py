#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2,json
from cookie import cookieexpresssid
import re 
import ssl

def _getnotificaciones():

	
	context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

	url="https://exo.do/api/notifications"
	req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0','Cookie':'express.sid='+cookieexpresssid})
	f = urllib2.urlopen(req, context=context)
	array = f.read()
	#print "_getnotificaciones: Array=", array
	f.close()
	data=json.loads(array)

	arrayestadisticas=[]
	for l in data["notifications"]:
		#print l
		if l["bodyShort"].find("notifications:user_mentioned_you_in")>0 and l["read"]==False:
			print "_getnotificaciones*******"
			print l["bodyLong"]
			usuario=l["user"]["userslug"]
			
			m = re.search('@botmensajes\s*(\d*)',l["bodyLong"])
			m2 = re.search('@botmensajes\s{0,3}http[s]?:\/\/exo\.do\/topic\/(\d*)\/',l["bodyLong"])

			hilosolicitado=""
			if m2 is not None:
				hilosolicitado= m2.group(1)
			elif m is not None:
				hilosolicitado= m.group(1)
			if hilosolicitado!="":
				resptid=l["tid"]
				#print "hilo solicitado y resptid", int(hilosolicitado), int(resptid)
				arrayestadisticas.append([hilosolicitado, resptid,usuario])
	print "_getnotificaciones*******"
	print "arrayestadisticas=", arrayestadisticas
	return arrayestadisticas
	
_getnotificaciones()