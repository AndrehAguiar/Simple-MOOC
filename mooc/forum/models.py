from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager


# Create your models here.


class ThreadManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(
            models.Q(title__icontains=query) | \
            models.Q(body__icontains=query) | \
            models.Q(author__icontains=query)
        )


class Thread(models.Model):
    title = models.CharField(
        'Título',
        max_length=100
    )
    body = models.TextField(
        'Mensagem'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Autor',
        related_name='threads',
        on_delete=models.CASCADE
    )
    views = models.IntegerField(
        'Visualizações',
        blank=True,
        default=0
    )
    answers = models.IntegerField(
        'Respostas',
        blank=True,
        default=0
    )
    tags = TaggableManager()

    created_at = models.DateTimeField(
        'Criado em',
        auto_now_add=True
    )
    update_at = models.DateTimeField(
        'Modificado em',
        auto_now=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['-update_at']


class ReplyManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(
            models.Q(author__icontains=query) | \
            models.Q(reply__icontains=query) | \
            models.Q(correct__icontains=query)
        )


class Reply(models.Model):
    thread = models.ForeignKey(
        Thread,
        verbose_name='Tópico',
        related_name='replies',
        on_delete=models.CASCADE
    )
    reply = models.TextField(
        'Resposta'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Autor',
        related_name='replies',
        on_delete=models.CASCADE
    )
    correct = models.BooleanField(
        'Correta?',
        blank=True,
        default=False
    )
    created_at = models.DateTimeField(
        'Criado em',
        auto_now_add=True
    )

    update_at = models.DateTimeField(
        'Modificado em',
        auto_now=True
    )

    def __str__(self):
        return self.reply[:100]

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        ordering = ['-correct', 'created_at']
