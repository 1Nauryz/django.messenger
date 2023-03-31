from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from .models import *

def index(request):
    message = Message.objects.all()
    return render(request, 'network/index.html', {'message': message, 'title': 'Main Page'})


def about(request):
    message = Message.objects.all()
    return render(request, 'network/about.html', {'message': message, 'title': 'About Page'})


def login(request):
    return HttpResponse("LOGIN PAGE")


def contact(request):
    return HttpResponse("CONTACT PAGE")


def writeMessage(request):
    return HttpResponse("Write Message PAGE")


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h2>PAGE NOT FOUND</h2>")