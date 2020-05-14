from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView
from .models import Thread

# Create your views here.

# class ForumView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'forum/index.html')
#
#
# class ForumView(TemplateView):
#     template_name = 'forum/index.html'


class ForumView(ListView):
    model = Thread
    paginate_by = 10
    template_name = 'forum/index.html'


index = ForumView.as_view()
# index = TemplateView.as_view(template_name='forum/index.html')
