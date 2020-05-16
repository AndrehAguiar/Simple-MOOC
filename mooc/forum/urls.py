from django.urls import path, re_path
from mooc.forum.views import index, thread, reply_correct, reply_incorrect

app_name = 'forum'
urlpatterns = [
    path(r'',
         index,
         name='index'),
    re_path(r'^tag/(?P<tag>[\w_-]+)/$',
            index,
            name='index_tagged'),
    re_path(r'^respostas/(?P<pk>\d+)/correta/$',
            reply_correct,
            name='reply_correct'),
    re_path(r'^respostas/(?P<pk>\d+)/incorreta/$',
            reply_incorrect,
            name='reply_incorrect'),
    re_path(r'^(?P<slug>[\w_-]+)/$',
            thread,
            name='thread'),
]
