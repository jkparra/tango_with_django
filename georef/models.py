
from django.db import models
# Create your models here.
class Programa (models.Model):
    codigo=models.IntegerField (primary_key=True)
    nombre=models.CharField(max_length=25)
    latitud=models.CharField(max_length=20,default="0")
    longitud=models.CharField(max_length=20,default="0")
    def __str__(self):
        return self.nombre

class Vendedor(models.Model):
    codigo=models.IntegerField(primary_key=True)
    nombre=models.CharField(max_length=75)
    color=models.CharField(max_length=20,default="Black")
    programa=models.ForeignKey(Programa)
    class Meta:
        verbose_name_plural="Vendedores"
    def __str__(self):
        return self.nombre
class Tienda(models.Model):
    codigo=models.IntegerField(primary_key=True)
    nombre=models.CharField(max_length=100)
    direccion=models.CharField(max_length=120)
    localidad=models.CharField(max_length=35)
    coordenadas=models.CharField(max_length=40)
    latitud=models.CharField(max_length=20,default="0")
    longitud=models.CharField(max_length=20,default="0")
    compra_otc=models.CharField(max_length=20,default="NO")
    compra_blanqueador=models.CharField(max_length=20,default="NO COMPRA")
    compra_aditivo=models.CharField(max_length=20,default="NO COMPRA")
    compra_mensual=models.FloatField(default=0)
    compra_reciente=models.CharField(max_length=20,default="NO")
    programa=models.ForeignKey(Programa)
    vendedor=models.ForeignKey(Vendedor)
    def __str__(self):
        return str(self.codigo)
class ApiKeys(models.Model):
    clave=models.CharField(max_length=50,primary_key=True)
    tipo=models.CharField(max_length=10)
    def __str__(self):
        return "{} tipo {}".format(self.clave,self.tipo)
