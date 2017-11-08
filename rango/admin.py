from django.contrib import admin
from rango.models import UserProfile
# Register your models here.
from rango.models import Category, Page
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}
class PageDetails(admin.ModelAdmin):
    list_display=("title","category","url","views")
admin.site.register(Category,CategoryAdmin)
admin.site.register(Page,PageDetails)
admin.site.register(UserProfile)
