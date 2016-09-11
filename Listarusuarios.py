#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2,json
from collections import defaultdict # para convertir a array
import collections 
import operator # para ordenar la lista
from Configuracion import cookieexpresssid
import sys 
import math

from collections import Counter

from Concurrentget import _getsimultaneo

def _generarlista(hilo,pagina=30): #Esta funcion genera una array con las url de exo.do
	print "INICIO _generarlista"
	arrurl=[]
	for i in range(1,pagina+1):
		arrurl.append('https://exo.do/api/topic/' + str(hilo) +"/?page="+ str(i))
		
	return arrurl
	print "****FIN _generarlista"
	
	


def _listarusuarios(hilo): #Esta función solicita todas las páginas del hilo y cuenta los usuarios
	print "INICIO _listarusuarios"
	
	listausuario=[]
		
	#En primer lugar vamos a ver cuantas páginas hay:
	url = 'https://exo.do/api/topic/' + str(hilo) +"/?page=1"
	print url 
	req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0','Cookie':'express.sid='+cookieexpresssid})
	try:
		f = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print e.code
		print e.msg
		return -1, -1
	array = f.read()

	#print array 
	data  = json.loads(array)
	#print array 
	if data["template"]["name"]=="topic-error": return -1, -1 
	if data["loggedIn"]==False: #Si no estaos logueados se avisa y se devuelve error (-1)
		print "Error, no te has logueado"
		return -1, -1
	
	postcount=data["postcount"] #contamos los post en total
	totalpost=len(data["posts"])-1 #contamos cuantos post estamos viendo
	paginas=int(math.ceil(float(postcount)/int(totalpost))) #calculamos las páginas dividiendo y redondeando hacia arriba
	
	titulopost=data["title"] #Aprovechamos para sacar el título del hilo
	
	print "_listarusuarios: Numero de paginas calculadas: ", paginas 
	arrurl2 = _generarlista(hilo,paginas) #Generamos la lista con todas las páginas que vamos a solicitar
	
	#print "_listarusuarios: Hay %d paginas" %len(arrurl2)
	if paginas+1>8: #Si hay más de 8 páginas utilizamos 8 hilos, si hay menos pues una por hilo
		concurrencia=8
	else: 
		concurrencia=paginas+1
	#concurrencia=2
	array= _getsimultaneo(arrurl2,concurrencia) #Llamamos a la función que solicitará todas las páginas, calculara los subtotales de usuarios y nos devolverá una array de diccionarios con todos los usuarios.
	
	print "_listarusuarios: Fin del cálculo por partes. Inicio de unir diccionarios"
		
	Resultcounter= sum((Counter(dict(x)) for x in array), Counter())
	#print Resultcounter
	Resultarray=list(collections.Counter(Resultcounter).items())
	
	print "_listarusuarios: Diccionarios unidos, convirtiendo a array "
	unsorted_list_usuarios = []
	for key in sorted(Resultcounter.iterkeys(), reverse=True):
		unsorted_list_usuarios.append([key, Resultcounter[key]])
	
	list_usuarios=sorted(unsorted_list_usuarios, key=operator.itemgetter(1),reverse=True)
	
	print "_listarusuarios:" , list_usuarios
	"""
	d = defaultdict(int)
	a = listausuario
	for i in a:
		d[i] += 1
	#print d
	
	"""
	print "****FIN _listarusuarios"
	return list_usuarios, titulopost

def _tabladeusuarios(hilo):
	print "inicio _tabladeusuario"
	reload(sys)  
	sys.setdefaultencoding('utf8')

	list_usuarios, titulo = _listarusuarios(hilo)
	total=0
	if list_usuarios==-1: return -1 
	for u in list_usuarios:
		total = total + u[1]
	titulo= titulo.encode('utf8')
	string=  r"\n# ["+ titulo + r"]("+ r"//exo.do/topic/"+str(hilo)+ r""")\n:::\n Puesto | Usuario | Nº Post en hilo\n|---|---|---|\n"""
	
	
	for i, line in enumerate(list_usuarios):
		i+=1
		string= string + str(i) + r"|" +  line[0] + r"|" + str(line[1])+r"""\n"""
	string= string + r"""|TOTAL| | """ + str(total) + r"""|\n:::"""
	return string 
	print "****FIN _tabladeusuario"
		
#print _tabladeusuarios(15076)