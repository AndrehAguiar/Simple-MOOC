# Create your models here.
import re

from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, UserManager)
from django.core import validators
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        'Nome de Usuário',
        max_length=30,
        unique=True,
        validators=[
            validators.RegexValidator(
                re.compile(r'^[\w.@+-]+$'),
                'O nome de usuário só pode conter letras, números e @/./+/-/_',
                'invalid'
            )
        ]
    )
    email = models.EmailField(
        'E-mail',
        unique=True
    )
    name = models.CharField(
        'Nome',
        max_length=100,
        blank=True
    )
    is_active = models.BooleanField(
        'Está ativo?',
        blank=True,
        default=True
    )
    is_staff = models.BooleanField(
        'É da equipe?',
        blank=True,
        default=False
    )
    date_joined = models.DateTimeField(
        'Data de Entrada',
        auto_now_add=True
    )
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.name or self.username

    def get_shot_name(self):
        return self.username

    def get_full_name(self):
        return str(self)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


class PasswordResetManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(
            models.Q(user__icontains=query)
        )


class PasswordReset(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Usuário',
        on_delete=models.CASCADE,
        related_name='resets'
    )
    key = models.CharField(
        'Chave',
        max_length=100,
        unique=True)
    created_at = models.DateTimeField(
        'Criado em',
        auto_now_add=True)
    confirmed = models.BooleanField(
        'Confirmado?',
        default=False,
        blank=True)

    objects = PasswordResetManager()

    def __str__(self):
        return '{0} em {1}'.format(
            self.user,
            self.created_at
        )

    class Meta:
        verbose_name = 'Nova Senha'
        verbose_name_plural = 'Novas Senhas'
        ordering = ['-created_at']
