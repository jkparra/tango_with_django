"""tango_with_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
#se incluyen las siguientes direcciones para dar portabilidad
from django.conf.urls import include
from rango import views
from django.conf import settings
from django.conf.urls.static import static
from registration.backends.simple.views import RegistrationView

urlpatterns = [
    #url(r'^$',views.about,name='about'),
    url(r'^$',views.index,name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^rango/',include('rango.urls')),
    #url(r'^accounts/register/$',MyRegistrationView.as_view(),name='registration_register'),
    url(r'^accounts/',include('registration.backends.simple.urls')),
    #above maps any urls mapping /rango to be manage by rango apps
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
#la linea anterior aplicaria si las media dinamicas estuvieran llegando
#a rango/media/  por lo que esta linea debe adicionarse al urls.py de
#proyecto completo

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


#create a new class that redirects user to the index page
class MyRegistrationView(RegistrationView):
    def get_success_url(self,user):
        return '/rango/'
