from django.contrib import admin

from .models import Thread, Reply


# Register your models here.

class ThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'update_at']
    search_fields = ['title', 'author__email', 'body']


class ReplyAdmin(admin.ModelAdmin):
    list_display = ['thread', 'author', 'created_at', 'update_at']
    search_fields = ['thread__author', 'author__email', 'reply']


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Reply, ReplyAdmin)
