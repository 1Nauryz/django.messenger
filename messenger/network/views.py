from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from .models import *

def index(request):
    message = Message.objects.all()
    context = {
        'message': message,
        'title': 'Main Page',
    }
    return render(request, 'network/index.html', context=context)


def about(request):
    message = Message.objects.all()
    context = {
        'message': message,
        'title': 'About Page',
    }
    return render(request, 'network/about.html', context=context)


def login(request):
    return HttpResponse("LOGIN PAGE")


def contact(request):
    message = Message.objects.all()
    context = {
        'message': message,
        'title': 'Contact Page',
    }
    return render(request, 'network/contact.html', context=context)


def writeMessage(request):
    return HttpResponse("Write Message PAGE")


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h2>PAGE NOT FOUND</h2>")