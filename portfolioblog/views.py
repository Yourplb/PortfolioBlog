from django.shortcuts import render
from django.contrib.auth.decorators import login_required



def contacts(request):
    return render(request, 'blog/contacts.html')


def index(request):
    return render(request, 'blog/index.html')
