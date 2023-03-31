from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('writeMessage/', writeMessage, name='writeMessage'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),

]
