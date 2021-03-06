from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
#User Auth Stuff
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

#Model
from rango.models import Category, Page, userProfile
from rango.forms import CategoryForms, PageForms, UserForms, UserProfileForms
from rango.bing_search import run_query

#Other
from datetime import datetime

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

    #Define merge fields in a dictionary
    category_list = Category.objects.order_by('-likes')[:5]
    most_viewed = Category.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list,'most_viewed': most_viewed}

    visits = request.session.get("visits")
    if not visits:
        visits = 1

    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:

        #cast value to date time
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).days > 0:
            visits = visits + 1
            reset_last_visit_time = True

    else:

        #Last visit doesn't exist so set it
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits

    context_dict['visits'] = visits
    response = render(request, 'rango/index.html', context_dict)
    #Pass all the data into the render.
    return response

def about(request):
	link = '<a href="/rango">Home</a>'
	
	if request.session.get('visits'):
		visits = request.session.get('visits')
	else:
		visits = 0

	context_dict = {'visits': visits}

	return render(request, 'rango/about.html', context_dict)


def category(request, category_name_slug):

    #Create a blank dict for the rendering engine
	context_dict = {}

	if request.method == 'POST':
		query = request.POST['query'].strip()

		if query:

			#run the bing search function
			result_list = run_query(query)

		return render(request, 'rango/search.html', {'result_list': result_list})

	else:

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





@login_required
def restricted(request):

	return HttpResponse("Since you're logged in, you can see this text")



# Process the search request
def search(request):

	result_list = []

	if request.method == 'POST':
		query = request.POST['query'].strip()

		if query:

			#run the bing search function
			result_list = run_query(query)

	return render(request, 'rango/search.html', {'result_list': result_list})


# Perform click tracking

def track_url(request):

	if request.method == "GET":
		if 'pageid' in request.GET:
			page_id = request.GET['pageid']

			page = Page.objects.get(id=page_id)
			print "object"	
			print page
			currentCount = page.views
			url = page.url
			print url
			newCount = currentCount + 1

			page.views = newCount

			page.save()




	return redirect(url)

@login_required
def register_profile(request):

	context = {}

	if request.method == "POST":

		userID = request.user.id
		user = User.objects.get(id=userID)

		print user
		form = UserProfileForms(request.POST)

		if form.is_valid():

			profile = form.save(commit=False)

			profile.user = user

			profile.save()

			return redirect('/rango')
			


		print "test"

	else:

		if request.user.is_authenticated:

			form = UserProfileForms()
			context['form'] = form

	return render( request, 'rango/profile_registration.html', context)

@login_required
def profile(request):

	user = request.user
	if user.is_authenticated:

		
		context = {}

		if request.method == "GET":
			getUser = userProfile.objects.get(user=user)
		

			getUser = userProfile.objects.get(user=user)

			form = UserProfileForms(instance=getUser)
			context['form'] = form

		elif request.method == "POST":


			# Update the user profile
			instance = userProfile.objects.get(user=user)
			form = UserProfileForms(request.POST, instance = instance)

			if form.is_valid():
				print "is Valid"
				
				profile = form.save(commit=False)

				profile.user = user

				profile.save()

				context['form'] = form				
			else:

				print "Is Not Valid"

	else:

		context = {}

	return render( request, 'rango/profile.html', context)

@login_required
def like_category(request):

	cat_id = None
	if request.method == "GET":
		print "GET"
		categoryid = request.GET['category_id']

	likes = 0
	if categoryid:
		print "catid"
		cat = Category.objects.get(id=int(categoryid))
		if cat:
			likes = cat.likes + 1
			cat.likes = likes
			cat.save()

	return HttpResponse(likes)