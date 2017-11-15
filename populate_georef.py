import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',"tango_with_django.settings")
import pandas as pd
import django
django.setup()
from georef.models import Vendedor, Tienda, Programa, ApiKeys

def populate():
    df=pd.read_excel('datos_georef.xlsx',sheet_name="programa")
    add_programa(df)
    chequear_programa()
    df=pd.read_excel('datos_georef.xlsx',sheet_name="vendedor")
    add_vendedor(df)
    chequear_vendedor()
    df=pd.read_excel('datos_georef.xlsx',sheet_name="tienda")
    add_tienda(df)
    chequear_tienda()
    add_key()
    chequear_key()



def add_programa(df):
    for i in df.index:
        p=Programa.objects.get_or_create(codigo=df['codigo'][i],nombre=df['nombre'][i])[0]
        p.latitud=df['coordenadas'][i].split(',')[0]
        p.longitud=df['coordenadas'][i].split(',')[1]
        p.save()

def add_vendedor(df):
    for i in df.index:
        p=Programa.objects.get_or_create(codigo=df['programa'][i])[0]
        v=Vendedor.objects.get_or_create(codigo=df['codigo'][i],nombre=df['nombre'][i],programa=p)[0]
        v.save()

def add_tienda(df):
    for i in df.index:
        print(f"i {i} {df['programa'][i]}")

        p=Programa.objects.get(codigo=df['programa'][i])
        print(f"p {p}")
        v=Vendedor.objects.get(codigo=df['vendedor'][i])
        print(f"v {v}")
        lat=df['coordenadas'][i].split(",")[0]
        lng=df['coordenadas'][i].split(",")[1]
        #print(f"latitud {lat} longitud {lng}")
        t=Tienda.objects.get_or_create(codigo=df['codigo'][i],programa=p,vendedor=v)[0]

        t.nombre=df['nombre'][i]
        t.direccion=df['direccion'][i]
        t.localidad=df['localidad'][i]
        t.coordenadas=df['coordenadas'][i]
        t.programa=p
        t.vendedor=v
        lat=t.coordenadas.split(",")[0]
        lng=t.coordenadas.split(",")[1]
        t.latitud=lat
        t.longitud=lng
        print("listo para salvar")
        t.save()

def add_key():
    k=ApiKeys.objects.get_or_create(clave="AIzaSyCSPV519NeRA9AHLfWLyCrtEva5MbUL_LI",tipo="geocode")[0]
    k=ApiKeys.objects.get_or_create(clave="AIzaSyCsYv-KEH6WNq4JtsSWTTMOdPzPHeuHJP8",tipo="geocode")[0]
    k=ApiKeys.objects.get_or_create(clave="AIzaSyBckQmYAj27KJOcRLaXEWnhgrliapEFh14",tipo="maps")[0]
    #k=ApiKeys.objects.get_or_create(clave="AIzaSyA3lvXJ8XK06TnblkKADofy6wZe6HEF_xI",tipo="maps")[0]

def chequear_programa():
    p=Programa.objects.all()
    for x in p:
        print(x)
def chequear_vendedor():
    v=Vendedor.objects.all()
    for x in v:
        print(x)
def chequear_tienda():
    t=Tienda.objects.all()
    for x in t:
        print(x)
def chequear_key():
    k=ApiKeys.objects.all()
    for x in k:
        print (x)


def completar_coordenadas():
    t=Tienda.objects.all()
    for x in t:
        lat=x.coordenadas.split(",")[0]
        lng=x.coordenadas.split(",")[1]
        #print(f"latitud {lat} longitud {lng}")
        x.latitud=lat
        x.longitud=lng
        x.save()
#start execution here!
populate()
#completar_coordenadas()
#df=pd.read_excel('datos_georef.xlsx',sheet_name="programa")
#add_programa(df)
