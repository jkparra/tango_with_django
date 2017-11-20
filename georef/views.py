from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from georef.models import Programa, Vendedor, Tienda, ApiKeys

#para generar datos geograficos
from geojson import Point,Feature,GeometryCollection,FeatureCollection

#librarias para generar el tag no necesarias aqui sino en templatetag js
from django.utils.safestring import mark_safe
from django.template import Library
import json

#para ensayo pdf
from django.template.loader import render_to_string
from weasyprint import HTML
from reportlab.pdfgen import canvas

#para ensayopdf2
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile





register=Library()
cod_programa_default=5


# Create your views here.
def indice (request):  #forma de tener un dropdown dinamico manejado por java script muy complejo y dificil de manejar
    #A HTTP POST
    lista_tiendas=[]
    lista_vendedores=[]
    opciones_vendedores={cod_programa_default:[{"codigo":cod_programa_default,
                                                "nombre":"Todos",
                                                "color":"White",
                                              }]
                        }
    prog=Programa.objects.get(codigo=cod_programa_default)
    lat_mapa=prog.latitud
    lng_mapa=prog.longitud
    if request.method=="POST":
        forma= FiltrarTiendasForm(request.POST,codigo_programa=request.POST['programa'][0])
        print(forma.errors)
        if forma.is_valid():
            cd=forma.cleaned_data
            prog=Programa.objects.get(codigo=cd.get("programa"))
            listado=Tienda.objects.filter(programa=prog).all()
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
            lista_tiendas=listado[:]
            lat_mapa=prog.latitud
            lng_mapa=prog.longitud
            list_vend=Vendedor.objects.filter(programa=prog).values('codigo','color')
            lista_vendedores=list(list_vend)
            opciones_vendedores={}
            programas=Programa.objects.all()
            for prog in programas:
                list_vend=Vendedor.objects.filter(programa=prog).values('codigo','nombre','color')

                opciones_vendedores[prog.codigo]=[{"codigo":0,
                                                            "nombre":"Todos",
                                                                "color":"White",
                                                          }]+list(list_vend)
                #opciones_vendedores[prog.codigo].append(list(list_vend)[:])
                opciones_vendedores[prog.codigo]
            #json_lista_vendedores=js|0(lista_vendedores)

    else:
        forma=FiltrarTiendasForm(codigo_programa=cod_programa_default)

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
    print("opciones vendedores {}".format(opciones_vendedores))
    return render(request,'georef/indice.html',context={"lat":lat_mapa,
                                                        "lng":lng_mapa,
                                                        "url_script":url_script,
                                                        "geojson_tiendas":geojson_tiendas,
                                                        "forma":forma,
                                                        "lista_vendedores":lista_vendedores,
                                                        "opciones_vendedores":opciones_vendedores})



class FiltrarTiendasForm2(forms.Form):

    opciones_programa=list(Programa.objects.values_list("codigo","nombre").distinct())
    opciones_vendedor=list(Vendedor.objects.values_list("codigo","nombre").distinct())
    opciones_vendedor.append((0,"Todos"))
    opciones_localidad=list(Tienda.objects.values_list("localidad","localidad").distinct())
    opciones_compra_otc=[("SI","SI"),("NO","NO"),(0,"Todos")]
    opciones_compra_blanqueador=[("BOT BL","BOT BL"),("CAJA BL","CAJA BL"),("NO COMPRA","NO COMPRA"),(0,"Todos")]
    opciones_compra_aditivo=[("BOT AD","BOT AD"),("CAJA AD","CAJA AD"),("NO COMPRA","NO COMPRA"),(0,"Todos")]
    opciones_compra_reciente=[("SI","SI"),("NO","NO"),(0,"Todos")]
    opciones_localidad.append((0,"Todas"))
    programa=forms.ChoiceField(choices=opciones_programa,required=False,initial=cod_programa_default,help_text="Programa")
    vendedor=forms.ChoiceField(choices=opciones_vendedor,required=False,initial=0,help_text="Vendedor ")
    localidad=forms.ChoiceField(choices=opciones_localidad,required=False,initial=0,help_text="Localidad ")
    compra_otc=forms.ChoiceField(choices=opciones_compra_otc,required=False,initial=0,help_text="Compra OTC ")
    compra_reciente=forms.ChoiceField(choices=opciones_compra_reciente,required=False,initial=0,help_text="Compra Ult meses")
    compra_aditivo=forms.ChoiceField(choices=opciones_compra_aditivo,required=False,initial=0,help_text="Compra Aditivo")
    compra_blanqueador=forms.ChoiceField(choices=opciones_compra_blanqueador,required=False,initial=0,help_text="Compra Blanqueador")


class FiltrarTiendasForm(forms.Form):
    def __init__(self,*args,**kwargs):
        codigo_programa=kwargs.pop("codigo_programa")
        super(FiltrarTiendasForm,self).__init__(*args,**kwargs)



        opciones_programa=list(Programa.objects.values_list("codigo","nombre").distinct())
        self.fields["programa"]=forms.ChoiceField(choices=opciones_programa,required=False,initial=cod_programa_default,help_text="Programa")

        if not codigo_programa:
            codigo_programa=cod_programa_default
        prog=Programa.objects.get(codigo=codigo_programa)
        opciones_vendedor=list(Vendedor.objects.filter(programa=prog).values_list("codigo","nombre").distinct())
        opciones_vendedor.append((0,"Todos"))
        self.fields["vendedor"]=forms.ChoiceField(choices=opciones_vendedor,required=False,initial=0,help_text="Vendedor ")

        opciones_localidad=list(Tienda.objects.values_list("localidad","localidad").distinct())
        opciones_localidad.append((0,"Todas"))
        self.fields["localidad"]=forms.ChoiceField(choices=opciones_localidad,required=False,initial=0,help_text="Localidad ")

        opciones_compra_otc=[("SI","SI"),("NO","NO"),(0,"Todos")]
        self.fields["compra_otc"]=forms.ChoiceField(choices=opciones_compra_otc,required=False,initial=0,help_text="Compra OTC ")

        opciones_compra_blanqueador=[("BOT BL","BOT BL"),("CAJA BL","CAJA BL"),("NO COMPRA","NO COMPRA"),(0,"Todos")]
        self.fields["compra_blanqueador"]=forms.ChoiceField(choices=opciones_compra_blanqueador,required=False,initial=0,help_text="Compra Blanqueador")

        opciones_compra_aditivo=[("BOT AD","BOT AD"),("CAJA AD","CAJA AD"),("NO COMPRA","NO COMPRA"),(0,"Todos")]
        self.fields["compra_aditivo"]=forms.ChoiceField(choices=opciones_compra_aditivo,required=False,initial=0,help_text="Compra Aditivo")

        opciones_compra_reciente=[("SI","SI"),("NO","NO"),(0,"Todos")]
        self.fields["compra_reciente"]=forms.ChoiceField(choices=opciones_compra_reciente,required=False,initial=0,help_text="Compra Ult meses")



def ensayopdf(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response

def ensayopdf2(request):
    #MODEL Data
    vendedor=Vendedor.objects.values('programa','codigo','nombre','color').order_by('codigo')
    #rendered
    html_string=render_to_string('georef/generate_pdf.html',{'vendedor':vendedor})
    print(html_string)
    html=HTML(string=html_string,base_url=request.build_absolute_uri())
    result=html.write_pdf()
    #creating http response
    response=HttpResponse(content_type='application/pdf;')
    response['Content-Disposition']='inline; filename=lista_vendedores.pdf'
    response['Content-Transfer-Encoding']='binary'
    with tempfile.NamedTemporaryFile(delete=False) as output:
        output.write(result)
        output.flush()
        output=open(output.name,'rb')
        response.write(output.read())
    return response
def ensayopdf21(request):
    vendedor=Vendedor.objects.values('programa','codigo','nombre','color').order_by('codigo')
    print(vendedor)
    return render(request,'georef/generate_pdf.html',context={'vendedor':vendedor})
