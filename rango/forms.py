from django import forms
from rango.models import Page, Category, UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    #esta es la forma de acceder a las definiciones de campo
    largo=Category._meta.get_field("name").max_length
    name=forms.CharField(max_length=largo, help_text="Please enter the Category Name")
    views=forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    likes=forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    slug=forms.CharField(widget=forms.HiddenInput(),required=False)
    #An inline class to provide additional information to the form.
    class Meta:
        #Provide association between ModelForm and Model
        model=Category
        fields=('name',)


class PageForm(forms.ModelForm):
    largo=Page._meta.get_field("title").max_length
    largourl=Page._meta.get_field("url").max_length

    title=forms.CharField(max_length=largo,help_text="Please enter title of the page")
    url=forms.URLField(max_length=largourl,help_text="Please enter the URL of the page")
    views=forms.IntegerField(widget=forms.HiddenInput(),initial=0)

    class Meta:
        #Association between ModelForm and Model
        model=Page
        #exclude=("Category",)
        #could be including the other fields
        fields=("title","url","views")
#class UserForm(forms.ModelForm):
#    password=forms.CharField(widget=forms.PasswordInput())
#    class Meta:
#        model=User
#        fields=("username","email","password")

#class UserProfileForm(forms.ModelForm):
#    class Meta:
#        model=UserProfile
#        fields=("website","picture")
