from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from mooc.accounts.models import User


# Create your tests here.
class RegisterUserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(name='Fulano Teste', email='teste@mooc.com', username='fulano-teste')

    def tearDown(self):
        self.user.delete()

    def test_register_form_error(self):
        data = {'email': '', 'username': '', 'password1': '', 'password2': ''}
        client = Client()
        path = reverse('accounts:register')
        response = client.post(path, data)
        self.assertFormError(response, 'form', 'username', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'password1', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'password2', 'Este campo é obrigatório.')
        data = {'email': 'test@mooc.com', 'username': 'fulano_teste', 'password1': 'teste@123', 'password2': 'teste@1243'}
        response = client.post(path, data)
        self.assertFormError(response, 'form', 'password2', 'As senhas não são iguais')

    def test_login_form_error(self):
        data = {'username': '', 'password': ''}
        client = Client()
        path = reverse('accounts:login')
        response = client.post(path, data)
        self.assertFormError(response, 'form', 'username', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'password', 'Este campo é obrigatório.')
