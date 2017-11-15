from sys import argv
from os.path import exists
import requests
#import webbrowsser
#otra api key AIzaSyCSPV519NeRA9AHLfWLyCrtEva5MbUL_LI
#PETICION PARA DIRECCIONES EN COLOMBIA USANDO BOUNDS
#https://maps.googleapis.com/maps/api/geocode/json?address=Calle+12+a+31+217+cali,+colombia&bounds=3.2,-76.6|3.6,-76.4&key=AIzaSyCSPV519NeRA9AHLfWLyCrtEva5MbUL_LI
#PARA HACER GEOPOSICIONAMIENTO INVERSO, SE DAN LAS COORDENADAS Y ENTREGA LA DIRECCIONES
#https://maps.googleapis.com/maps/api/geocode/json?latlng=3.45,-76.53&key=AIzaSyCSPV519NeRA9AHLfWLyCrtEva5MbUL_LI
def primer_ensayo():
    api_key="&key=AIzaSyCsYv-KEH6WNq4JtsSWTTMOdPzPHeuHJP8"
    target=open("ciudadesReferenciadas2.xml","w")
    indata=open("ciudades.txt")
    target.write('<?xml version="1.0" encoding="iso-8859-1"?>\n')
    target.write("<inicio>\n")
    for line in indata:

        res=requests.get("https://maps.googleapis.com/maps/api/geocode/xml?address={}{}".format(line,api_key))
        target.write("<registroCiudad>\n")
        target.write("<ciudadBuscada>{}</ciudadBuscada>\n".format(line))
        target.write(res.text[39:])
        target.write("</registroCiudad>\n")
        print("Procesada ciudad {}".format(line))
    print ("termine!")
    target.write("</inicio>")
    target.close()
    indata.close()

primer_ensayo()
