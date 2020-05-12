from django.contrib import admin
from .models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'username', 'email', 'last_login', 'date_joined']
    search_fields = ['username', 'email']
    prepopulated_fields = {'username': ('name',)}


# Register your models here.
admin.site.register(User, UserAdmin)
