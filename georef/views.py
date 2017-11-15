from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from geojson import Point,Feature,GeometryCollection,FeatureCollection

cod_programa_default=5
from georef.models import Programa, Vendedor, Tienda, ApiKeys
# Create your views here.
def indice (request):
    #A HTTP POST
    lista_tiendas=[]
    prog=Programa.objects.get(codigo=cod_programa_default)
    lat_mapa=prog.latitud
    lng_mapa=prog.longitud

    print(f"request method {request.method}")
    if request.method=="POST":
        forma= FiltrarTiendasForm(request.POST)
        print(forma.errors)
        if forma.is_valid():
            cd=forma.cleaned_data
            prog=Programa.objects.get(codigo=cd.get("programa"))

            listado=Tienda.objects.filter(programa=prog).all()
            print("valor forma vendedor {}".format(cd.get('vendedor')=='0'))
            if cd.get("vendedor")!='0':
                vend=Vendedor.objects.get(codigo=cd.get("vendedor"))
                listado=listado.filter(vendedor=vend)
            if cd.get("localidad")!='0':
                listado=listado.filter(localidad=cd.get("localidad"))
            #lista_tiendas=Tienda.objects.filter(localidad=cd.get("localidad"),programa=prog,vendedor=vend).all()[:]
            lista_tiendas=listado[:]
            lat_mapa=prog.latitud
            lng_mapa=prog.longitud
    else:
        forma=FiltrarTiendasForm()

    clave=ApiKeys.objects.filter(tipo="maps").values('clave')[0]["clave"]
    url_script="https://maps.googleapis.com/maps/api/js?key=" + clave + "&callback=initMap"

    lista_puntos=[]
    for t in lista_tiendas[:]:
        punto=Point((float(t.longitud),float(t.latitud)))
        feat=Feature(geometry=punto,properties={"codigo":t.codigo,"vendedor":t.vendedor.codigo})
        lista_puntos.append(feat)
    gc=FeatureCollection(lista_puntos)
    gc["type"]="FeatureCollection"
    geojson_tiendas="eqfeed_callback(" + str(gc) +")"
    return render(request,'georef/indice.html',context={"lat":lat_mapa,
                                                        "lng":lng_mapa,
                                                        "url_script":url_script,
                                                        "geojson_tiendas":geojson_tiendas,
                                                        "forma":forma,})


class FiltrarTiendasForm(forms.Form):

    opciones_programa=list(Programa.objects.values_list("codigo","nombre").distinct())
    opciones_vendedor=list(Vendedor.objects.values_list("codigo","nombre").distinct())
    opciones_vendedor.append((0,"Todos"))
    opciones_localidad=list(Tienda.objects.values_list("localidad","localidad").distinct())
    opciones_localidad.append((0,"Todas"))
    print(f"opciones... {opciones_vendedor}")
    #opciones_programa=((3, "TAT CALI"),(5,"TAT PEREIRA"))
    #opciones_vendedor=((1300,"VENDEDOR 1"),(1302,"VENDEDOR 2"))
    #opciones_localidad=((1,"santa rosa"),(2,"la virginia"))
    programa=forms.ChoiceField(choices=opciones_programa,required=False,initial=cod_programa_default)
    vendedor=forms.ChoiceField(choices=opciones_vendedor,required=False,initial=0)
    localidad=forms.ChoiceField(choices=opciones_localidad,required=False,initial=0)
    #    largo=Tienda._meta.get_field("nombre").max_length
    #    largourl=Page._meta.get_field("url").max_length

    #    title=forms.CharField(max_length=largo,help_text="Please enter title of the page")
    #    url=forms.URLField(max_length=largourl,help_text="Please enter the URL of the page")
    #    codigo=forms.IntegerField()
    #    nombre=forms.Charfield(max_length=largo,help_text="Nombre")

    #class Meta:
        #Association between ModelForm and Model
        #model=Tienda
        #exclude=("Category",)
        #could be including the other fields
        #fields=("programa","vendedor","localidad")
    #    pass
