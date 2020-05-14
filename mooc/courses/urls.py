"""courses URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from mooc.courses.views import index, details, enrollment, undo_enrollment, announcements, show_announcement, lessons, lesson, material

app_name = 'courses'
urlpatterns = [
    path(r'',
         index,
         name='index'),
    # path('<int:pk>', details, name='details'),
    re_path(r'^(?P<slug>[\w_-]+)/$',
            details,
            name='details'),
    re_path(r'^(?P<slug>[\w_-]+)/inscricao/$',
            enrollment,
            name='enrollment'),
    re_path(r'^(?P<slug>[\w_-]+)/cancelar-inscricao/$',
            undo_enrollment,
            name='undo_enrollment'),
    re_path(r'^(?P<slug>[\w_-]+)/anuncios/$',
            announcements,
            name='announcements'),
    re_path(r'^(?P<slug>[\w_-]+)/anuncios/(?P<pk>\d+)/$',
            show_announcement,
            name='show_announcement'),
    re_path(r'^(?P<slug>[\w_-]+)/aulas/$',
            lessons,
            name='lessons'),
    re_path(r'^(?P<slug>[\w_-]+)/aulas/(?P<pk>\d+)/$',
            lesson,
            name='lesson'),
    re_path(r'^(?P<slug>[\w_-]+)/materiais/(?P<pk>\d+)/$',
            material,
            name='material'),
]
