# Create your models here.
from django.dispatch.dispatcher import receiver
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings
from django.db import models

from mooc.core.mail import send_mail_template


class CourseManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(
            models.Q(id__icontains=query) | \
            models.Q(name__icontains=query) | \
            models.Q(description__icontains=query) | \
            models.Q(slug__icontains=query)
        )


class Course(models.Model):
    name = models.CharField(
        'Nome',
        max_length=100
    )
    slug = models.SlugField(
        'Atalho'
    )
    description = models.TextField(
        'Enunciado',
        blank=True
    )
    about = models.TextField(
        'Ementa do curso',
        blank=True
    )
    start_date = models.DateField(
        'Data de Início',
        null=True,
        blank=True
    )
    image = models.ImageField(
        upload_to='courses/images',
        verbose_name='Imagem',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        'Criado em',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        'Atualizado em',
        auto_now=True
    )
    objects = CourseManager()

    def __str__(self):
        return self.name

    def release_lessons(self):
        today = timezone.now().date()
        return self.lessons.filter(release_date__gte=today)

    def get_absolute_url(self):
        return '/cursos/' + str(self.slug)

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['name']


class LessonManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(
            models.Q(course__icontains=query) | \
            models.Q(name__icontains=query) | \
            models.Q(description__icontains=query) | \
            models.Q(number__icontains=query)
        )


class Lesson(models.Model):
    # Conecta a aula a um curso específico pelo ForeignKey
    course = models.ForeignKey(
        Course,
        verbose_name='Curso',
        related_name='lessons',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        'Name',
        max_length=100
    )
    description = models.TextField(
        'Descrição',
        blank=True
    )
    number = models.IntegerField(
        'Número (ordem)',
        blank=True,
        default=0
    )
    release_date = models.DateTimeField(
        'Data de Liberção',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        'Criado em',
        auto_now_add=True
    )
    update_at = models.DateTimeField(
        'Atualizado em',
        auto_now=True
    )
    objects = LessonManager()

    def __str__(self):
        return self.name

    def is_available(self):
        if self.release_date:
            today = timezone.now().date()
            return self.release_date >= today
        return False

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['number']


class MaterialManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains=query) | models.Q(course__icontains=query) |models.Q(lesson__icontains=query) | models.Q(file__icontains=query)
        )


class Material(models.Model):
    # Conecta o material a uma aula específica pelo ForeignKey
    course = models.ForeignKey(
        Course,
        verbose_name='Curso',
        related_name='material',
        on_delete=models.CASCADE
    )
    # Conecta o material a uma aula específica pelo ForeignKey
    lesson = models.ForeignKey(
        Lesson,
        verbose_name='Aula',
        related_name='material',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        'Nome',
        max_length=100,
    )
    embedded = models.TextField(
        'Vídeo embedded',
        blank=True
    )

    objects = MaterialManager()

    def is_embedded(self):
        return bool(self.embedded)

    file = models.FileField(
        upload_to='lessons/material',
        blank=True,
        null=True
    )

    def __str__(self):
        material_curso = self.course.name + ' / ' + self.lesson.name + ' / ' + self.name
        return material_curso

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiais'


class EnrollmentManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(
            models.Q(user__icontains=query) | models.Q(course__icontains=query) | models.Q(slug__icontains=query)
        )


class Enrollment(models.Model):
    # Conecta a inscrição a um usuário específico pelo ForeignKey
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Usuário',
        related_name='enrollments',
        on_delete=models.CASCADE
    )
    # Conecta a inscrição a um curso específico pelo ForeignKey
    course = models.ForeignKey(
        Course,
        verbose_name='Curso',
        related_name='enrollments',
        on_delete=models.CASCADE
    )
    STATUS_CHOICES = (
        (0, 'Pendente'),
        (1, 'Aprovado'),
        (2, 'Cancelado'),
    )
    status = models.IntegerField(
        'Situação',
        choices=STATUS_CHOICES,
        default=1,
        blank=True
    )
    created_at = models.DateTimeField(
        'Criado em',
        auto_now_add=True
    )
    update_at = models.DateTimeField(
        'Atualizado em',
        auto_now=True
    )

    objects = EnrollmentManager()

    def active(self):
        self.status = 1
        self.save()

    def is_approved(self):
        return self.status == 1

    def __str__(self):
        inscrito = self.course.name + ' / ' + self.user.name
        return inscrito

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = (('user', 'course'),)


class AnnouncementManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(
            models.Q(user__icontains=query) | models.Q(course__icontains=query) | models.Q(tilte__icontains=query)
        )


class Announcement(models.Model):
    # Conecta o anúncio a um usuário específico pelo ForeignKey
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Usuário',
        related_name='announcements',
        on_delete=models.CASCADE
    )
    # Conecta o anúncio a um curso específico pelo ForeignKey
    course = models.ForeignKey(
        Course,
        verbose_name='Curso',
        related_name='announcements',
        on_delete=models.CASCADE
    )
    title = models.CharField(
        'Título',
        max_length=100
    )
    content = models.TextField(
        'Conteúdo'
    )
    created_at = models.DateTimeField(
        'Criado em',
        auto_now_add=True
    )
    update_at = models.DateTimeField(
        'Atualizado em',
        auto_now=True
    )

    objects = AnnouncementManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'
        ordering = ['-created_at']


@receiver(models.signals.post_save, sender=Announcement)
def post_save_announcement(instance, created, **kwargs):
    if created:
        subject = instance.title
        context = {
            'announcement': instance
        }
        template_name = 'courses/announcement_mail.html'
        enrollments = Enrollment.objects.filter(
            course=instance.course,
            status=1
        )
        for enrollment in enrollments:
            recipient_list = [enrollment.user.email]
            send_mail_template(subject, template_name, context, recipient_list)


models.signals.post_save.connect(
    post_save_announcement,
    sender=Announcement,
    dispatch_uid='post_save_announcement'
)


class CommentManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(
            models.Q(course__icontains=query) | \
            models.Q(announcement__icontains=query) | \
            models.Q(comment__icontains=query)
        )


class Comment(models.Model):
    # Conecta o comentário a um usuário específico pelo ForeignKey
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Usuário',
        related_name='comments',
        on_delete=models.CASCADE
    )
    # Conecta o comentário a um anúncio específico pelo ForeignKey
    announcement = models.ForeignKey(
        Announcement,
        verbose_name='Anúncio',
        related_name='comments',
        on_delete=models.CASCADE
    )
    comment = models.TextField(
        'Comentário'
    )
    created_at = models.DateTimeField(
        'Criado em',
        auto_now_add=True
    )
    update_at = models.DateTimeField(
        'Atualizado em',
        auto_now=True
    )

    objects = CommentManager()

    def __str__(self):
        comentado = self.announcement.course.name + ' / ' + self.announcement.title + ' / ' + self.user.name
        return comentado

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['created_at']
