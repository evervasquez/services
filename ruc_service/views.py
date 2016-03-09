import urllib.request
import urllib.parse
import re
import json
import requests
import random
from django.http import HttpResponse
from django.views.generic import ListView

class Ruc_service(ListView):
	def randomip():
		user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36'
		url = "http://www.google-proxy.net/"
		headers={'User-Agent':user_agent,} 
		request=urllib.request.Request(url,None,headers) 
		response = urllib.request.urlopen(request)
		data = response.read().decode('utf-8')
		n_c= '</thead>\s*<tbody><tr>([^´]*)</tbody>\s*<tfoot>\s*<tr>'
		pattern1 = re.compile(n_c)
		data1 = re.findall(pattern1,data)
		#print(data1[0])
		n_c2= '<td>(.*)</td>'
		pattern2= re.compile(n_c2)
		data2 = re.findall(pattern2,data1[0])
		datafin={}
		cont=0
		for val in data2:
			borrartdi=val.replace("<td>"," ")
			borrartdf=borrartdi.replace("</td>"," ")
			datafinal=borrartdf.split("  ")
			datafin[cont]=datafinal
			cont=cont+1 
		num=random.randint(1,len(datafin))
		return HttpResponse(datafin[num][0]+':'+datafin[num][1])
	def _data_Get():
	    #ip=Ruc_service.randomip()
	    ip="107.151.136.220:80"
	    print (ip)
	    proxy = {"http": "http://"+ip+""}
	    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
	    headers={'User-Agent':user_agent,
	            'Host':'webservice.miasoftware.net',
	            'Upgrade-Insecure-Requests':'1',
	            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	            'Accept-Encoding':'gzip,deflate,sdch',
	            'Accept-Language':'es-ES,es;q=0.8',
	            'Cache-Control':'no-cache',
	            'Connection':'keep-alive',
	            'Content-type':'text/html; charset=ISO-8859-1'
	            }
	    data = {'ruc':'20600629922'}
	    dat1=urllib.parse.urlencode(data)
	    #print(dat1)
	    r = requests.get('http://webservice.miasoftware.net/service/sunat/test_ruc.php?ruc=20523477006',proxies=proxy,headers=headers)
	    data=r.text
	    #print(len(data))
	    #print(r.text)
	    n_c= '(.*)'
	    pattern1 = re.compile(n_c)
	    data1 = re.findall(pattern1,data)
	    #data1[0] es todo la data de la empresa
	    # 9 es el formato
	    #print (data1[9])
	    if (data1[9]=="Formato XML"):
	    	ali={0:'n1_ruc',1:'n1_alias',2:'n1_estado',3:'n1_condicion',4:'n1_ubigeo',5:'n1_ubigeo_dep',6:'n1_ubigeo_pro',7:'n1_ubigeo_dis'}
	    	cont=0
	    	data={}
	    	for val in data1[13:28]:
	        	if(val!=''):
	        		borrartdf=val.replace("<"+ali[cont]+">","")
	        		borrartdi=borrartdf.replace("</"+ali[cont]+">","")
	        		data[cont]=borrartdi
	        		cont=cont+1                
	    	data[0]=data[0].replace("<root>","")
	    	return HttpResponse(str(data), content_type="text/plain")
	    else:
	    	if(data1[9]=='Formato JSON'): 
	        	borrartdf=data1[13:21][0].replace("[","")
	        	borrartdi=borrartdf.replace("]","")
	        	borrartdf2=borrartdi.replace("{","")
	        	borrartdi2=borrartdf2.replace("}","")
	        	borrartdi3=borrartdi2.replace('"',"")
	        	borrartdi3=borrartdi2.replace('"',"")
	        	borrartdi4=borrartdi3.split(',')
	        	data={}
	        	cont=0
	        	for val in borrartdi4:
	        		valor=val.split(':')
	        		data[cont]=valor[1]
	        		cont=cont+1
	        	return HttpResponse(str(data), content_type="text/plain")
	    	else:
	        	data={}
	        	cont=0
	        	for val in data1[13:36]:
	        		if(val!=''):
	        			values=val.split("=")
	        			data[cont]=values[1]
	        			cont=cont+1
	        	#print (data)
	        	return HttpResponse(str(data), content_type="text/plain")

	def get(self,request):
	 	return (Ruc_service._data_Get())

		
