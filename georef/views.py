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
            if cd.get("compra_reciente")!='0':
                listado=listado.filter(compra_reciente=cd.get("compra_reciente"))
            if cd.get("compra_otc")!='0':
                listado=listado.filter(compra_otc=cd.get("compra_otc"))
            if cd.get("compra_blanqueador")!='0':
                listado=listado.filter(compra_blanqueador=cd.get("compra_blanqueador"))
            if cd.get("compra_aditivo")!='0':
                listado=listado.filter(compra_aditivo=cd.get("compra_aditivo"))



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
        feat=Feature(geometry=punto,properties={"codigo":t.codigo,
                                                "vendedor":t.vendedor.codigo,
                                                "color":t.vendedor.color})
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
    opciones_compra_otc=[("SI","SI"),("NO","NO"),(0,"Todos")]
    #opciones_compra_otc=list(Tienda.objects.values_list("compra_otc","compra_otc").distinct())
    opciones_compra_blanqueador=[("BOT BL","BOT BL"),("CAJA BL","CAJA BL"),("NO COMPRA","NO COMPRA"),(0,"Todos")]
    #opciones_compra_blanqueador=list(Tienda.objects.values_list("compra_blanqueador","compra_blanqueador").distinct())
    opciones_compra_aditivo=[("BOT AD","BOT AD"),("CAJA AD","CAJA AD"),("NO COMPRA","NO COMPRA"),(0,"Todos")]
    #opciones_compra_aditivo=list(Tienda.objects.values_list("compra_aditivo","compra_aditivo").distinct())
    opciones_compra_reciente=[("SI","SI"),("NO","NO"),(0,"Todos")]
    #opciones_compra_reciente=list(Tienda.objects.values_list("compra_reciente","compra_reciente").distinct())
    #opciones.compra_reciente.append((0,"Todos"))


    opciones_localidad.append((0,"Todas"))
    print(f"opciones... {opciones_vendedor}")
    #opciones_programa=((3, "TAT CALI"),(5,"TAT PEREIRA"))
    #opciones_vendedor=((1300,"VENDEDOR 1"),(1302,"VENDEDOR 2"))
    #opciones_localidad=((1,"santa rosa"),(2,"la virginia"))
    programa=forms.ChoiceField(choices=opciones_programa,required=False,initial=cod_programa_default,help_text="Programa")
    vendedor=forms.ChoiceField(choices=opciones_vendedor,required=False,initial=0,help_text="Vendedor ")
    localidad=forms.ChoiceField(choices=opciones_localidad,required=False,initial=0,help_text="Localidad ")
    compra_otc=forms.ChoiceField(choices=opciones_compra_otc,required=False,initial=0,help_text="Compra OTC ")
    compra_reciente=forms.ChoiceField(choices=opciones_compra_reciente,required=False,initial=0,help_text="Compra Ult meses")
    compra_aditivo=forms.ChoiceField(choices=opciones_compra_aditivo,required=False,initial=0,help_text="Compra Aditivo")
    compra_blanqueador=forms.ChoiceField(choices=opciones_compra_blanqueador,required=False,initial=0,help_text="Compra Blanqueador")


    #    largo=Tienda._meta.get_field("nombre").max_length
    #    largourl=Page._meta.get_field("url").max_length

    #    title=forms.CharField(max_length=largo,help_text="Plearecienteenter title of the page")
    #    urRLField(max_length=largourl,help_text="Please enter the URL of the page")
    #    codigo=forms.IntegerField()
    #    nombre=forms.Charfield(max_length=largo,help_text="Nombre")

    #class Meta:
        #Association between ModelForm and Model
        #model=Tienda
        #exclude=("Category",)
        #could be including the other fields
        #fields=("programa","vendedor","localidad")
    #    pass
