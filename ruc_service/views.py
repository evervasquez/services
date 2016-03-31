import urllib.request
import urllib.parse
import re
import json
import time
import requests
import random
from django.http import HttpResponse
from django.views.generic import ListView
from timeit import timeit
from .models import Proxy,Personas
from django.db import connection
class Ruc_service(ListView):
	def randomip():
		user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36'
		#url ="http://www.google-proxy.net/"
		url ="https://www.us-proxy.org/"
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
		ip=(datafin[num][0]+':'+datafin[num][1])
		print(ip)
		proxy = {"http": "http://"+ip+""}
		try:
			r = requests.get('http://google.com',proxies=proxy,timeout=3)
		except requests.HTTPError as e:
			print("Checking internet connection failed, status code.".format(e.response.status_code))
			Ruc_service.randomip()
		except requests.ConnectionError:
			print("No internet connection available.")
			Ruc_service.randomip()
		else:
			print ("All was fine")
			return ip
	def _data_Get(ruc):
		ruc2=ruc
		datos=Ruc_service.connected(ruc2)
		data=datos
		n_c= '(.*)'
		pattern1 = re.compile(n_c)
		data1 = re.findall(pattern1,data)#data1[0] es todo la data de la empresa 9 es el formato
		print((data1[0]))
		print(str(data1[4]))
		if((data1[6]=='status_msg=RUC 20531588118 no existe')or(len(str(data1[4]))==13)or(len(str(data1[4]))==2)):
			return HttpResponse(str("RUC "+ruc+" no existe"), content_type="text/plain")

		if (data1[0]=="Formato XML"):
			print(data1[0])
			ali={0:'n1_ruc',1:'n1_alias',2:'n1_estado',3:'n1_condicion',4:'n1_ubigeo',5:'n1_ubigeo_dep',6:'n1_ubigeo_pro',7:'n1_ubigeo_dis',8:'n1_direccion'}
			cont=0
			data={}
			#print(data1[4:20])
			for val in data1[4:21]:
				if(val!=''):
					borrartdf=val.replace("<"+ali[cont]+">","")
					borrartdi=borrartdf.replace("</"+ali[cont]+">","")
					data[cont]=borrartdi
					cont=cont+1
				data[0]=data[0].replace("<root>","")
			return HttpResponse(str(data), content_type="text/plain")
		else:
			if(data1[0]=='Formato JSON'):
				print(data1[0])
				borrartdf=data1[4].replace("[","")
				borrartdi=borrartdf.replace("]","")
				borrartdf2=borrartdi.replace("{","")
				borrartdi2=borrartdf2.replace("}","")
				borrartdi3=borrartdi2.replace('"',"")
				borrartdi3=borrartdi2.replace('"',"")
				borrartdi4=borrartdi3.split(',')
				data={}
				cont=0
				#print(borrartdi4)
				for val in borrartdi4:
					valor=val.split(':')
					data[cont]=valor[1]
					cont=cont+1
				return HttpResponse(str(data), content_type="text/plain")
			else:
				#print(data1)
				data={}
				cont=0
				for val in data1[8:36]:
					if(val!=''):
						values=val.split("=")
						data[cont]=values[1]
						cont=cont+1
				return HttpResponse(str(data), content_type="text/plain")


	def get(self,request):
		ruc=request.GET['ruc']
		try:
			val = int(ruc)
		except ValueError:
			print("That's not an int!")
		else:
			if(len(ruc)==11):
				return (Ruc_service._data_Get(ruc))
			else:
				return HttpResponse(str("EL ruc tiene que tener 11 digitos"), content_type="text/plain")

	def connected(ruc):
		try:
			ip=Ruc_service.randomip()
			proxy = {"http": "http://"+ip+""}
			user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
			headers={'User-Agent':user_agent,'Host':'ws.insite.pe','Upgrade-Insecure-Requests':'1','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Encoding':'gzip, deflate, sdch','Accept-Language':'es-ES,es;q=0.8','Cache-Control':'no-cache','Connection':'keep-alive','Content-type':'text/html; charset=ISO-8859-1','Cookie':'PHPSESSID=2ldrbf60pv5vh7hvg0eua17sr2'}
			data = {'ruc':ruc}
			print(data)
			dat1=urllib.parse.urlencode(data)
			filterProxy=Proxy.objects.filter(proxy=ip)
			r =requests.post('http://ws.insite.pe/sunat/test_ruc.php?ruc='+ruc,proxies=proxy,headers=headers,timeout=10)
			if(len(filterProxy.values("proxy"))==0):
				newProxy = Proxy(proxy=ip,fecha=time.strftime("%Y-%m-%d %H:%M:%S"),cantidad=1)
				newProxy.save()
			else:
				filterProxy.update(fecha=time.strftime("%Y-%m-%d %H:%M:%S"),cantidad=int(filterProxy.values("cantidad")[0]["cantidad"])+1)
			return r.text
		except requests.HTTPError as e:
			print("Checking internet connection failed, status code.".format(e.response.status_code))
			return False
		except requests.ConnectionError:
			print("No internet connection available.")
			return False

class Dni(ListView):
	def get(self,request):
		cont=0
		ip='212.82.126.32:80'
		proxy = {"http": "http://"+ip+""}
		user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'		
		while(cont<=30000000):
			headers={'User-Agent':user_agent,'Host':'consultamiembrodemesa.onpe.gob.pe','Upgrade-Insecure-Requests':'1','Accept':'application/json, text/javascript, */*; q=0.01','Accept-Encoding':'gzip, deflate, sdc','Accept-Language':'es-ES,es;q=0.8','Cache-Control':'no-cache','Connection':'keep-alive','Content-type':'text/html; charset=utf-8','X-Requested-With':'XMLHttpRequest'}
			dni=Dni.numdni()
			r = requests.get('http://consultamiembrodemesa.onpe.gob.pe/consultalv_eg_2016/default/index/consulta?documento='+dni+'&key=as12swerdserdfer4$fsdwesdfwerdswedsde',headers=headers,proxies=proxy)
			data=r.text
			json_obj = json.loads(data)
			data2=json_obj["page"]
			n_c= '<p class="nombre-dni">(.*)</p>'
			n_c2='<div class="span24 resultado-de r-ubigeo l-votacion">(.*)</div>'
			pattern1 = re.compile(n_c)
			data1 = re.findall(pattern1,data2)
			pattern2 = re.compile(n_c2)
			lugar = re.findall(pattern2,data2)
			if(len(data1)>0):
				persona=data1[0]+" "+data1[1]
				newPersona = Personas(persona=persona,dni=dni,lugar=lugar[0])
				newPersona.save()
				cont=cont+1
				print(cont)
			else:
				print("No participa")
		return HttpResponse("fin", content_type="text/plain")

	def numdni():
		num1=str(random.randrange(0,10,))
		num2=str(random.randrange(0,10,))
		num3=str(random.randrange(0,10,))
		num4=str(random.randrange(0,10,))
		num5=str(random.randrange(0,10,))
		num6=str(random.randrange(0,10,))
		num7=str(random.randrange(0,10,))
		num8=str(random.randrange(0,10,))
		num=str(num1+""+num2+""+num3+""+num4+""+num5+""+num6+""+num7+""+num8)
		print(num)
		return num
class Numpersonas(ListView):
	def get(self,request):
		numPersona = Personas.objects.all()
		print(len(numPersona.values("dni")))
		return HttpResponse(len(numPersona.values("dni")), content_type="text/plain")

		
