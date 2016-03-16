from django.db import models
from django.utils import timezone
class Proxy(models.Model):
	proxy = models.CharField(max_length=30)
	fecha = models.DateTimeField()
	cantidad = models.IntegerField()

class Personas(models.Model):
	persona=models.CharField(max_length=250)
	dni=models.CharField(max_length=10)
	lugar=models.CharField(max_length=250)
		
