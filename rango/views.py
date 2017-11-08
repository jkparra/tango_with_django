from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
#from rango.forms import UserProfileForm
#from rango.forms import UserForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    category_list=Category.objects.order_by('-likes')[:5]
    pages_list=Page.objects.order_by('-views')[:5]
    context_dict={"categories":category_list,"pages_most_viewed":pages_list}
    return render(request,'rango/index.html',context=context_dict)

def about(request):
    print (request.method)
    print (request.user)
    return render(request,'rango/about.html',context={})

def show_category(request, category_name_slug):
    context_dict={}
    try:
        category=Category.objects.get(slug=category_name_slug)
        pages=Page.objects.filter(category=category)
        context_dict['pages']=pages
        context_dict['category']=category
    except Category.DoesNotExist:
        context_dict['category']=None
        context_dict['pages']=None
    return render(request,'rango/category.html',context_dict)

@login_required
def add_category(request):
    form=CategoryForm()
    #A HTTP POST
    if request.method=="POST":
        form= CategoryForm(request.POST)

        #FORM IS VALID?
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)

    print("****** resultado *****{}".format(form))

    return render(request,'rango/add_category.html',{'form':form})

@login_required
def add_page(request,category_name_slug):
    print(" ****   category_name_slug {}".format(category_name_slug))
    try:
        category=Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category=None
    print("***request method {}".format(request.method))
    form=PageForm()
    if request.method=="POST":
        form=PageForm(request.POST)
        if form.is_valid():
            if category:
                page=form.save(commit=False)
                page.category=category
                page.views=0
                page.save()
                #print("Dentro de add_page page.category {} y page name {}".format(page.category, page.name))
                return show_category(request,category_name_slug)
        else:
            print(form.errors)
    context_dict={'form':form,"category":category}
    return render (request,"rango/add_page.html",context_dict)


#def register(request):
    #A boolean values for telling teh template
    #wheter teh resgitration was succesful
    #Set to fals initially. Code changes value to True
    #when regisgration succeeds.
#    registered=False

    #If it is POST were interesting in processing form Data
#    if request.method=="POST":
        #Attempt to grab informaation from the raw form information.
        #Note that we make use of both userform and userprofile form.
#        user_form=UserForm(data=request.POST)
#        profile_form=UserProfileForm(data=request.POST)
#        if user_form.is_valid() and profile_form.is_valid():
#            user=user_form.save()
            #now we hash password with set_password method.
            #once hashed, we can update user objects
#            user.set_password(user.password)
#            user.save()

            #Now sort_out the UserProfile instance.
            #Since we need to set the user attribute ourselves.
            #We set commit=false.  This delays saving the model  until
            #until we are ready to avoid integrity problems.
#            profile=profile_form.save(commit=False)
#            profile.user=user

            #Did the user  provide a profile picture.
            #if so, we need to get it from the input form and puit it in
            #int he userprofile models
#            if "picture" in request.FILES:
#                profile.picture=request.FILES["picture"]
            #Now we save the UserProfile model instance.
#            profile.save()

            #Update our variable to indicate that the template registration was successful
#            registered=True
#        else:
#            print(user_form.errors,profile_form.errors)
#    else:
        #not a http PoST  so we render our fom using tow model form instances.
#        user_form=UserForm()
#        profile_form=UserProfileForm()

    #render template depending on the conxtext
#    return render(request,"rango/register.html",{"user_form":user_form,"profile_form":profile_form, "registered":registered})

#def user_login(request):
    #If the rquest is HTTP POST, try to pull out the relevant information
#    if request.method=='POST':
        #Gather Username and password provided by user.
        #This information comes from login form
        #we used request.POST.get['<variable>'] returns None if value not exists
        #as opposed as request.POST['<variable>'] that raises an Keyerror exception
#        username=request.POST.get('username')
#        password=request.POST.get('password')
        #using django machinery if the combination is valid  a User object is returned
#        user=authenticate(username=username,password=password)
        #if we have a user object,combination is valid.
#        if user:
#            if user.is_active:
#                login(request,user)
#                return HttpResponseRedirect(reverse('index'))
#            else:
#                return HttpResponse("Your rango account is disabled")
#        else:
#            print("Invalid login details: {0},{1}".format(username,password))
            #return HttpResponse("<a href =\"/rango/login\">Invalid data supplied for user {}</a>".format(username))
#            return render(request,'rango/login.html',{"mensaje":"Datos incorrectos"})
        #The request is not an HTTP POST, so display login form.
#    else:
#        return render(request,'rango/login.html',{})


@login_required
def restricted (request):
    return HttpResponse("Since you're logged in, you can see this text")


#@login_required
#def user_logout (request):
##SINCE WE KNOW THE USER IS LOGGED IN, WE CAN JUST LOG THEM OUT
#    logout(request)
#    return HttpResponseRedirect(reverse('index'))
