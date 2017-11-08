import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',"tango_with_django.settings")

import django
django.setup()
from rango.models import Category, Page

def populate():
    #Creating list of dictionaries
    python_pages=[
        {"title":"Official Python Tutorial", "url":"http://docs.python.org/2/tutorial/","views":12},
        {"title":"How to think like a computer scientist","url":"http://www.greenteapress.com/thinkpython/","views":14},
        {"title":"Learn Python in 10 minutes","url":"http://www.korokithakis.net/tuturial/python/","views":18}
    ]
    django_pages=[
        {"title":"Official Django Tutorial", "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial101/","views":11},
        {"title":"Django Rocks", "url":"http://www.djangorocks.com/","views":17},
        {"title":"How to tango with Django", "url":"http://tangowithdjango.com/","views":19}
    ]
    other_pages=[
        {"title":"Bottle", "url":"https://bottlepy.org/docs/dev/","views":11},
        {"title":"Flask", "url":"https://flask.pocoo.org/","views":1}

    ]
    cats= {"Python":{"views":128,"likes":64,"pages":python_pages},
            "django":{"views":64,"likes":32,"pages":django_pages},
            "Other Frameworks":{"views":64,"likes":32,"pages":other_pages}
        }
    #adding categories y pages associated wiht category
    for cat, cat_data in cats.items():
        c=add_cat(cat,cat_data["views"],cat_data["likes"])
        for p in cat_data["pages"]:
            for p in cat_data["pages"]:
                add_page(c,p["title"],p["url"],p["views"])
    #print out Categories
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("-  {0} - {1}".format(str(c),str(p)))

def add_page(cat,title,url, views=0):
    p=Page.objects.get_or_create(category=cat,title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name,views,likes):
    c=Category.objects.get_or_create(name=name,views=views,likes=likes)[0]
    c.save
    return c

#start execution here!

if __name__=="__main__":
    print("Starging Rango Population Script ....")
    populate()
