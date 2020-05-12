from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.conf import settings

from model_mommy import mommy

from mooc.courses.models import Course


class CourseManagerTestCase(TestCase):
    def setUp(self) -> None:
        self.courses = mommy.make(
            'courses.Course',
            name='Python na WEB com Django',
            _quantity=5)
        self.courses = mommy.make(
            'courses.Course',
            name='Python para Devs',
            _quantity=10)
        self.client = Client()

    def tearDown(self) -> None:
        Course.objects.all().delete()

    def test_course_search(self):
        search = Course.objects.search('django')
        self.assertEqual(len(search), 5)
        search = Course.objects.search('devs')
        self.assertEqual(len(search), 10)
        search = Course.objects.search('Python')
        self.assertEqual(len(search), 15)