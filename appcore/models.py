from django.db import models

# Create your models here.

class Articulo(models.Model):
	titulo = models.CharField(max_length = 100)
	abstract = models.TextField()
	autor = models.CharField(max_length = 100)
	fecha = models.DateField()
	editorial = models.CharField(max_length = 50)
	revista = models.CharField(max_length = 50)
	paginas = models.CharField(max_length = 20)
	doi = models.CharField(max_length = 100)
	url = models.CharField(max_length = 200)
	palabras_clave = models.CharField(max_length = 100)

class Archivo(models.Model):
	archivo = models.FileField()