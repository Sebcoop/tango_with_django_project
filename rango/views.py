from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from django.shortcuts import render
from django.http import HttpResponse
from rango.forms import CategoryForm
from rango.forms import PageForm

	
#create new views here
def index(request):

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}

    # Render the response and send it back
    return render(request, 'rango/index.html', context=context_dict)
	
	

	
def about(request):
    print(request.method)
    print(request.user)
    return render(request, 'rango/about.html', {})
	


	
def show_category(request, category_name_slug):
	context_dict = {}
	
	try:
		#can we find a category name slug with given name?
		# If we can't, the .get() method raises a DoesNotExist exception.
		# So the .get() method returns one model instance or raises an exception.
		category = Category.objects.get(slug=category_name_slug)
		
		# Retrieve all of the associated pages.
		# Note that filter() will return a list of page objects or an empty list
		pages = Page.objects.filter(category=category)
		# We also add the category object from
		# the database to the context dictionary.
		# We'll use this in the template to verify that the category exists.
		context_dict['Pages'] = pages
		context_dict['Category'] = category
	except Category.DoesNotExist:
		#do nothing
		context_dict['category'] = None
		context_dict['pages'] = None
	
	return render(request, 'rango/category.html', context_dict)
	

	

def add_category(request):
	form = CategoryForm()
	
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		
		if form.is_valid():
			cat = form.save(commit=True)
			return index(request)
		else:
			print(form.errors)
	return render(request, 'rango/add_category.html', {'form': form})

	
	

def add_page(request, category_name_slug):
	try:
		category = Category.objects.egt(slug=category_name_slug)
	except:
		category = None
	
	form = PageForm()
	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if category:
				page = form.save(commit=False)
				page.category = category
				page.views = 0
				page.save()
				return show_category(request, category_name_slug)
		else:
			print(form.errors)
	context_dict = {'form':form, 'category': category}
	return render(request, 'rango/add_page.html', context_dict)
































	
	



