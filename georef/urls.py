from django.conf.urls import url
from georef import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
#este numeral es importate para tenerer un namespace para las url de la aplicacion
app_name= "georef"
#toda funcion se llamara por rango:name en el html
#en el html puede referenciarse esta direcion por el name o por la rango.views.about

urlpatterns=[
#url(r'^georef/$',views.about,name='about'),
url(r'^$',views.indice,name='indice'),
#url(r'^add_category/$',views.add_category,name='add_category'),
#url(r'^category/(?P<category_name_slug>[\w\-]+)/$',views.show_category,name="show_category"),
#url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$',views.add_page,name='add_page'),
#url(r'^register/$',views.register,name='register'),
#url(r'^login/$',views.user_login,name='login'),
#url(r'^restricted/$',views.restricted,name='restricted'),
#url(r'^logout/$',views.user_logout, name='logout'),

]
#registration.backends.simple.urls incluye las siguientes direcciones, autenticación en un solo paso
#+ registration /accounts/register/
#+ registration complete /accounts/register/complete/
#+ login /accounts/login/
#+ logout /accounts/logout/
#+ password change  /password/change/
#+ password reset /password/reset/

#registration.backendes.default.urls que es en dos pasos, con confirmaciónd e correo
#+ activation complete  activate/complete/
#+ activate if account fails activate/<activation_key>/

#observe estos dos casos como una parte de la direccion se pasa como parametro a la función
