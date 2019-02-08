from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from django.shortcuts import render
from django.http import HttpResponse

	
#create new views here
def index(request):
	
	category_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by('-views')[:5]
	context_dict = {'categories': category_list, 'pages': page_list}
	
	return render(request, 'rango/index.html', context=context_dict)
	
	

	
def about(request):
	context_dict = {'boldmessage': 'Rango says about page is here'}
	return render(request, 'rango/about.html', context=context_dict)
	


	
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
	




	
	



