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
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, re_path
from mooc.accounts.views import register, dashboard, edit, edit_password, password_reset, password_reset_confirm

app_name = 'accounts'
urlpatterns = [
    path(r'',
         dashboard,
         name='dashboard'),
    re_path(r'^entrar/$',
            LoginView.as_view(template_name='accounts/login.html'),
            name='login'),
    re_path(r'^sair/$',
            LogoutView.as_view(next_page='/'),
            name='logout'),
    re_path(r'^cadastre-se/$',
            register,
            name='register'),
    re_path(r'^editar/$',
            edit,
            name='edit'),
    re_path(r'^redefine-senha/$',
            password_reset,
            name='password_reset'),
    re_path(r'^confirma-nova-senha/(?P<key>\w+)/$',
            password_reset_confirm,
            name='password_reset_confirm'),
    re_path(r'^editar-senha/$',
            edit_password,
            name='edit_password'),
]
