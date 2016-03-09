from django.db import models
from django.utils import timezone
class Proxy(models.Model):
	proxy = models.CharField(max_length=30)
	fecha = models.DateTimeField()
	cantidad = models.IntegerField()
