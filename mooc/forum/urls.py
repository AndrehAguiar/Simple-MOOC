from django.urls import path, re_path
from mooc.forum.views import index

app_name = 'forum'
urlpatterns = [
    path(r'',
         index,
         name='index')
    ]