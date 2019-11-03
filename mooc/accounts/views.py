# Create your views here.
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (PasswordChangeForm, SetPasswordForm)
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegisterForm, EditAccountForm, PasswordResetForm
from .models import PasswordReset

User = get_user_model()


@login_required
def dashboard(request):
	template_name = 'accounts/dashboard.html'
	context = {}
	return render(request, template_name, context)


def register(request):
	template_name = 'accounts/register.html'
	form = RegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save()
		messages.success(
			request, 'Seja bem-vindo, seu cadastro foi realizado com sucesso')
		user = authenticate(
			username=user.username,
			password=form.cleaned_data['password1']
			)
		login(request, user)
		return redirect(settings.LOGIN_REDIRECT_URL)
	context = {
		'form': form
	}
	return render(request, template_name, context)


def password_reset(request):
	template_name = 'accounts/password_reset.html'
	context = {}
	form = PasswordResetForm(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(
			request, 'Foi enviado um e-mail para redefinição da sua senha')
		return redirect('accounts:login')
		# context['success'] = True
	context['form'] = form
	return render(request, template_name, context)


def password_reset_confirm(request, key):
	template_name = 'accounts/password_reset_confirm.html'
	context = {}
	reset = get_object_or_404(PasswordReset, key=key)
	form = SetPasswordForm(user=reset.user, data=request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(
			request, 'Sua senha foi alterada com sucesso com sucesso')
		return redirect('accounts:dashboard')
		# context['success'] = True
	context['form'] = form
	return render(request, template_name, context)


@login_required
def edit(request):
	template_name = 'accounts/edit.html'
	context = {}
	form = EditAccountForm(request.POST or None, instance=request.user)
	if form.is_valid():
		form.save()
		messages.success(
			request, 'Seus dados foram alterados com sucesso')
		return redirect('accounts:dashboard')
		# form = EditAccountForm(instance=request.user)
		# context['success'] = True
	context['form'] = form
	return render(request, template_name, context)


@login_required
def edit_password(request):
	template_name = 'accounts/edit_password.html'
	context = {}
	form = PasswordChangeForm(
		data=request.POST or None,
		user=request.user)
	if form.is_valid():
		user = form.save()
		messages.success(
			request, 'Sua senha foi alterada com sucesso')
		return redirect('accounts:dashboard')
		# context['success'] = True
		"""	user = authenticate(
				username=user.username,
				password=form.cleaned_data['password1']
				)
			return redirect(settings.LOGIN_REDIRECT_URL)"""
	context['form'] = form
	return render(request, template_name, context)
