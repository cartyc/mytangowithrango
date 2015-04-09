from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
#User Auth Stuff
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

#Model
from rango.models import Category, Page, userProfile
from rango.forms import CategoryForms, PageForms, UserForms, UserProfileForms

#Category Form

def add_category(request):

	# Is it a post?
	if request.method == 'POST':
		form = CategoryForms(request.POST)

		#Check form validity
		if form.is_valid():
			#save
			form.save(commit=True)

			#Return to index
			return index(request)

		else:
			#print errors if any
			print form.errors

	else:
		form = CategoryForms()

	return render(request, 'rango/add_category.html', {'form':form})

# Page Form

def add_page(request, category_name_slug):

	try:
		cat = Category.objects.get(slug=category_name_slug)
		print cat.name
	except Category.DoesNotExist:
		cat = None

	if request.method == 'POST':
		form = PageForms(request.POST)

		if form.is_valid():
			if cat:
				page = form.save(commit=False)
				page.category = cat
				page.views = 0
				page.save()

				return category(request, category_name_slug)
		else:
			print "not valid"
			print form.errors

	else:

		form = PageForms()

	return render(request, 'rango/add_page.html', {'form': form, 'category': cat})

# Create your views here.
def index(request):

    request.session.set_test_cookie()

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



def register(request):

	#Make sure form starts off with an the user being unregistered. 
	#This will change upon upon registration success
    if request.session.test_cookie_worked():
        print "Cookie worked!"
        request.session.delete_test_cookie()

	registered = False

	if request.method == "POST":

		user_form = UserForms(data=request.POST)
		profile_form = UserProfileForms(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():

			#Handle the user
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			#Handle the Users Profile
			profile = profile_form.save(commit=False)
			profile.user = user

			#Is there profile pic to be handled?
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			profile.save()

			registered = True

		else:

			print user_form.errors, profile_form.errors

	else:

		user_form = UserForms()
		profile_form = UserProfileForms()

	return render(request, 'rango/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered':registered})


def user_login(request):

	#If POST
	if request.method == "POST":

		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		#If user authenticates
		if user:

			if user.is_active:

				#If user is valid and active
				login(request, user)
				return HttpResponseRedirect('/rango/')

			else:

				#if not active
				return HttpResponse('Your Rango account was disabled')

		else:

			print "Invalid Login Details: {0}, {1}".format(username, password)
			return HttpResponse("invalid login details supplied")


	else:

		#If fresh form
		return render(request, 'rango/login.html', {})


@login_required
def restricted(request):

	return HttpResponse("Since you're logged in, you can see this text")

@login_required
def user_logout(request):

	logout(request)

	return HttpResponseRedirect('/rango')
