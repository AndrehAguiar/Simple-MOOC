# Create your views here.
from django.shortcuts import render


def home(request):
	template_name = 'home.html'
	return render(request, template_name)


def contact(request):
	template_name = 'contact.html'
	return render(request, template_name)
