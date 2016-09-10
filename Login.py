#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, re, json

def _getexpresssid(url,username,password):
	with requests.Session() as s:
		r= s.get(url,headers={'User-Agent': 'Mozilla/5.0'})
		m = re.search('\"csrf\_token\":\"([^"]+)\"',r.content)
		s.headers.update({'x-csrf-token': m.group(1)})
		form_data = {'username': username, 'password': password}
		r= s.post(url,data=form_data)
		encabezado= r.headers
		mm = re.search("express\.sid=([^;]+);", encabezado["set-cookie"])
