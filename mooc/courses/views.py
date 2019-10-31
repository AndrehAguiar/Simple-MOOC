from django.shortcuts import render, get_object_or_404
from .models import Course
from .forms import ContactCourse

# Create your views here.
def index(request):
	courses = Course.objects.all()
	template_name = 'courses/index.html'
	context = {
		'courses': courses
	}
	return render(request, template_name, context)

"""def details(request, pk):
	course = get_object_or_404(Course, pk=pk)
	template_name = 'courses/details.html'
	context = {
		'course': course
	}
	return render(request, template_name, context)"""

def details(request, slug):
	course = get_object_or_404(Course, slug=slug)
	context = {}

	form = ContactCourse(request.POST or None)
	if form.is_valid():
		context['is_valid'] = True
		"""
		print(form.cleaned_data['name'])
		print(form.cleaned_data['email'])
		print(form.cleaned_data['message'])
		"""
		"""
		imprimi lista de campos
		print(form.cleaned_data)
		"""
		form.send_mail(course)
		form = ContactCourse()

	context['course'] = course
	context['form'] = form	
	template_name = 'courses/details.html'
	return render(request, template_name, context)