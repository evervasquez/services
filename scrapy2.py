import requests
import urllib.parse
import re
import json
import random
import psycopg2
import itertools
cont=0
conn = psycopg2.connect(dbname='proxys2' ,user='denys', host='localhost' ,password='123456')
ip='50.201.223.217:80'
proxy = {"http": "http://"+ip+""}
code = '0123456789'
codigos = itertools.permutations(code,8)
inicio=0
fin=30000000
x = list(itertools.islice(codigos,inicio,fin,1))
for i in x:
      user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
      headers={'User-Agent':user_agent,'Host':'consultamiembrodemesa.onpe.gob.pe','Upgrade-Insecure-Requests':'1','Accept':'application/json, text/javascript, */*; q=0.01','Accept-Encoding':'gzip, deflate, sdc','Accept-Language':'es-ES,es;q=0.8','Cache-Control':'no-cache','Connection':'keep-alive','Content-type':'text/html; charset=utf-8','X-Requested-With':'XMLHttpRequest','Cookie':'__cfduid=d12d7eb5e962469337b827edf2afdf7091458311785; _gat=1; _ga=GA1.3.2046105002.1458311788; PHPSESSID=aalhvb2p63ke6bntdu0nhb2le0; ARRAffinity=ceef22ab0852dd7d38577ef3ab3694ae36f68c272effd14941448f1914a17e68'}
      dni=i[0]+i[1]+i[2]+i[3]+i[4]+i[5]+i[6]+i[7]
      print(dni)
      r = requests.get('http://consultamiembrodemesa.onpe.gob.pe/consultalv_eg_2016/default/index/consulta?documento='+dni+'&key=as12swerdserdfer4$fsdwesdfwerdswedsde',headers=headers,proxies=proxy)
      data=r.text
      json_obj = json.loads(data)
      data2=json_obj["page"]
      #print(data2)
      n_c= '<p class="nombre-dni">(.*)</p>'
      n_c2='<div class="span24 resultado-de r-ubigeo l-votacion">(.*)</div>'
      pattern1 = re.compile(n_c)
      data1 = re.findall(pattern1,data2)
      pattern2 = re.compile(n_c2)
      lugar = re.findall(pattern2,data2)
      if(len(data1)>0):
            persona=data1[0]+" "+data1[1]
            sql="INSERT INTO dni (persona,dni,lugar) VALUES ('"+persona+"','"+dni+"','"+lugar[0]+"');"
            #print(sql)
            cur = conn.cursor()
            cur.execute(sql)
            cur.close()
            conn.commit()
            #print ("Records created successfully")
            #print(data1)
            #print(sql)
            cont=cont+1
            print(cont)
      print("No")
conn.close()
print("fin")
