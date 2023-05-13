from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from .forms import UserRegistrationForm
# Create your tests here.


class UserRegistrationTestCase(TestCase):

    def setUp(self):
        self.url = reverse('register')
        self.valid_data = {
            'username': 'testuser',
            'first_name': 'testuser',
            'email': 'test@mail.ru',
            'password': 'TestPassword123',
            'password2': 'TestPassword123'
        }
        self.invalid_data = {
            'username': 'testuser',
            'first_name': 'testuser',
            'email': 'test@mail.ru',
            'password': 'TestPassword123',
            'password2': 'TestPassword111'
        }

    def test_registration_view_success_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_registration_view_contains_form(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], UserRegistrationForm)

    def test_registration_valid_form_submission(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(User.objects.count(), 1)

    def test_registration_invalid_form_submission(self):
        response = self.client.post(self.url, data=self.invalid_data)
        self.assertEquals(response.status_code, 200)

        form = UserRegistrationForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Пароли не совпадают', str(form.errors))

    def test_password_validation(self):
        form = UserRegistrationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_password_validation_fail(self):
        form = UserRegistrationForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())

    def test_register_unavailable_mail(self):
        user = User.objects.create_user(username='testuser', email='test@mail.ru', password='testpassword')
        user.save()

        form_data = {
            'username': 'newuser',
            'first_name': 'firstname',
            'email': 'test@mail.ru',
            'password': 'testpassword',
            'password2': 'testpassword'
        }

        form = UserRegistrationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('Пользователь с такой почтой уже зарегистрирован', str(form.errors))


class UserLoginTestCase(TestCase):

    def setUp(self):
        self.username = 'test'
        self.email = 'test@mail.ru'
        self.password = 'TestPass123'
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
        )

        self.url = reverse('login')
        self.valid_data = {
            'username': self.username,
            'password': self.password,
        }
        self.invalid_data = {
            'username': self.username,
            'password': 'IncorrectPass456',
        }

    def test_login_view_success_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_login_view_contains_form(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], AuthenticationForm)

    def test_valid_login(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertRedirects(response, reverse('index'))

    def test_invalid_login(self):
        response = self.client.post(self.url, data=self.invalid_data)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Пожалуйста, введите правильные имя пользователя и пароль.')
