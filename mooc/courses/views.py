# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ContactCourse, CommentForm
from .models import Course, Enrollment, Lesson, Material
from .decorators import enrollment_required


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
    course = get_object_or_404(
        Course,
        slug=slug
    )
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


@login_required
def enrollment(request, slug):
    course = get_object_or_404(
        Course,
        slug=slug
    )
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )
    if created:
        # Opção para aprovação no curso antes de ativar, alterar o default "self.status = 0" no models
        # enrollment.active()
        messages.success(request, 'Você foi inscrito no curso com sucesso')
    else:
        messages.info(request, 'Você já está inscrito no curso')
    return redirect('accounts:dashboard')


@login_required
def undo_enrollment(request, slug):
    course = get_object_or_404(
        Course,
        slug=slug
    )
    enrollment = get_object_or_404(
        Enrollment,
        user=request.user,
        course=course
    )
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Sua inscrição foi cancelada com sucesso')
        return redirect('accounts:dashboard')
    template = 'courses/undo_enrollment.html'
    context = {
        'enrollment': enrollment,
        'course': course,
    }
    return render(request, template, context)


@login_required
@enrollment_required
def announcements(request, slug):
    course = request.course
    template = 'courses/announcements.html'
    context = {
        'course': course,
        'announcements': course.announcements.all()
    }
    return render(request, template, context)


@login_required
@enrollment_required
def show_announcement(request, slug, pk):
    course = request.course
    announcement = get_object_or_404(
        course.announcements.all(),
        pk=pk
    )
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.announcement = announcement
        comment.save()
        form = CommentForm()
        messages.success(request, 'Seu comentário foi enviado com sucesso')
    elif form.errors:
        messages.error(request, 'Ocorreu algum erro. Confirme os dados informados e tente novamente.')
    template = 'courses/show_announcement.html'
    context = {
        'course': course,
        'announcement': announcement,
        'form': form,
    }
    return render(request, template, context)


@login_required
@enrollment_required
def lessons(request, slug):
    course = request.course
    template = 'courses/lessons.html'
    lessons = course.release_lessons()
    if request.user.is_staff:
        lessons = course.lessons.all()
    context = {
        'course': course,
        'lessons': lessons
    }
    return render(request, template, context)


@login_required
@enrollment_required
def lesson(request, slug, pk):
    course = request.course
    lesson = get_object_or_404(
        Lesson,
        pk=pk,
        course=course
    )
    if not request.user.is_staff and not lesson.is_available():
        messages.error('Esta aula ainda não está disponível')
        return redirect('courses:lessons', slug=course.slug)
    template = 'courses/lesson.html'
    context = {
        'course': course,
        'lesson': lesson
    }
    return render(request, template, context)


@login_required
@enrollment_required
def material(request, slug, pk):
    course = request.course
    material = get_object_or_404(
        Material,
        pk=pk,
        lesson__course=course,
    )
    lesson = material.lesson
    if not request.user.is_staff and not lesson.is_available():
        messages.error('Este material ainda não está disponível')
        return redirect('courses:lessons', slug=course.slug, pk=lesson.pk)
    if not material.is_embedded():
        material.file.url = course.slug
        return redirect(material.file.url)
    template = 'courses/material.html'
    context = {
        'course': course,
        'lesson': lesson,
        'material': material
    }
    return render(request, template, context)
