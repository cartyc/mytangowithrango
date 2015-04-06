from django.contrib import admin
from rango.models import Category, Page, userProfile

##Modified Views
class PageAdmin(admin.ModelAdmin):
	list_display = ('title','category',  'url')
	list_filter = ['category']
	search_fields = ['title']
	fields = ['category', 'title', 'url', 'views']

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(userProfile)
	