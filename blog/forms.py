from django import forms
from .models import Post, Comment
from django.forms import TextInput, Textarea


class EmailPostForm(forms.Form):
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['to'].widget.attrs.update({'placeholder': 'Укажите на какую почту отправить'})
        self.fields['comments'].widget.attrs.update({'placeholder': 'Введите ваш комментарий'})
        self.fields['to'].label = ''
        self.fields['comments'].label = ''


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'comment__input',
                'placeholder': 'Введите комментарий',
                'rows': 2
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label = ''


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'preview', 'body', 'tags', 'status']

        labels = {
            'title': False,
            'preview': 'Загрузить превью',
            'body': False,
            'tags': False,
            'status': False
        }

        widgets = {
            'title': TextInput(attrs={
                'placeholder': 'Название статьи',
                'class': 'create__post-title'
            }),
            'body': Textarea(attrs={
                'placeholder': 'Введите текст статьи...',
                'class': 'create__post-text',
                'rows': 6
            }),
            'preview': forms.FileInput(attrs={
                'type': 'file',
                'class': 'create__post-preview',
                'onchange': 'showPreview(event);'
            }),
            'tags': TextInput(attrs={
                'placeholder': 'Список тегов через запятую',
                'class': 'create__post-tags'
            }),
            'status': forms.Select(attrs={
                'class': 'create__post-status'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].help_text = None


class PostChangeForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'preview', 'body', 'status']

        labels = {
            'title': False,
            'preview': 'Превью',
            'body': False,
            'status': False
        }

        widgets = {
            'title': TextInput(attrs={
                'placeholder': 'Название статьи',
                'class': 'create__post-title'
            }),
            'body': Textarea(attrs={
                'placeholder': 'Введите текст статьи...',
                'class': 'create__post-text',
                'rows': 6
            }),
            'preview': forms.FileInput(attrs={
                'type': 'file',
                'class': 'create__post-preview'
            }),
            'status': forms.Select(attrs={
                'class': 'create__post-status'
            })
        }
