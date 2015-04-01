from django.shortcuts import render
from django.http import HttpResponse

from rango.models import Category, Page

# Create your views here.
def index(request):
	#Define merge fields in a dictionary
	category_list = Category.objects.order_by('-likes')[:5]
	most_viewed = Category.objects.order_by('-views')[:5]

	context_dict = {'categories': category_list,
				'most_viewed': most_viewed}

	#Pass all the data into the render.
	return render(request, 'rango/index.html', context_dict)

def about(request):
	link = '<a href="/rango">Home</a>'
	return render(request, 'rango/about.html')


def category(request, category_name_slug):

	#Create a blank dict for the rendering engine
	context_dict = {}

	try:
		#find the category that matches the slug url
		category = Category.objects.get(slug=category_name_slug)
		context_dict['category_name'] = category.name
		print category
		pages = Page.objects.filter(category=category)

		context_dict['pages'] = pages
		context_dict['category'] = category

	except Category.DoesNotExist:
		#If nothing is found
		pass

	#Render it up
	return render(request, 'rango/category.html', context_dict)
