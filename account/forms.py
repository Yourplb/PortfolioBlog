from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': 'Введите пароль', 'class': 'input'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': 'Повторите пароль', 'class': 'input'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

        labels = {
            'username': False,
            'first_name': False,
            'email': False,
        }

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Введите логин',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Введите имя',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input',
                'placeholder': 'Введите почту',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None

    def clean(self):
        cleaned_data = super().clean()
        self.password_validation()
        self.email_validation()
        return cleaned_data

    def password_validation(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')

    def email_validation(self):
        cd = self.cleaned_data
        email = cd.get('email')
        if not email:
            raise forms.ValidationError('Обязательное поле')
        elif User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с такой почтой уже зарегистрирован')
        return email


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

        labels = {
            'first_name': False,
            'last_name': False,
            'email': False
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'account__edit-first-name',
                'placeholder': 'Ваше имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'account__edit-last-name',
                'placeholder': 'Ваша фамилия'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'account__edit-email',
                'placeholder': 'Ваша почта'
            }),
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['about_user', 'date_of_birth', 'photo']

        labels = {
            'about_user': False,
            'date_of_birth': False,
            'photo': 'Фотография профиля'
        }

        widgets = {
            'about_user': forms.Textarea(attrs={
                'class': 'account__edit-about',
                'placeholder': 'О вас'
            }),
            'date_of_birth': forms.TextInput(attrs={
                'class': 'account__edit-date-of-birth',
                'placeholder': 'Дата вашего рождения'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'account__edit-photo',
                'type': 'file',
                'onchange': 'showPhotoProfile(event);'
            }),
        }
