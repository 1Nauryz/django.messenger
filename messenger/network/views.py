from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from rest_framework import generics, viewsets, routers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import *
from .models import *
from .permissions import IsOwnerOrReadOnly
from .serializers import MessageSerializer
from .utils import *


class MessageHome(DataMixin, ListView):
    paginate_by = 3
    model = Message
    template_name = 'network/index.html'
    context_object_name = 'message'
    extra_context = {'title': 'Main Page'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Main Page')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Message.objects.filter(is_published=True)


# def index(request):
#     message = Message.objects.all()
#     cats = Category.objects.all()
#     context = {
#         'message': message,
#         'cats': cats,
#         'cat_selected': 0,
#         'title': 'Main Page',
#     }
#     return render(request, 'network/index.html', context=context)

def about(request):
    message = Message.objects.all()
    paginator = Paginator(message, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/about.html', {'page_obj': page_obj, 'title': 'About Page', 'message': message})


# def login(request):
#     return HttpResponse("LOGIN PAGE")


def contact(request):
    message = Message.objects.all()
    context = {
        'message': message,
        'title': 'Contact Page',
    }
    return render(request, 'network/contact.html', context=context)


class writeMessage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'network/createPost.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Create Page')
        return dict(list(context.items()) + list(c_def.items()))


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    template_name = 'network/post_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# def writeMessage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#
#     return render(request, 'network/createPost.html', {'form': form, 'title': 'Create Post'})


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h2>PAGE NOT FOUND</h2>")


class ShowPost(DataMixin, DetailView):
    model = Message
    template_name = 'network/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Post Page')
        return dict(list(context.items()) + list(c_def.items()))


class MessageCategory(DataMixin, ListView):
    paginate_by = 3
    model = Message
    template_name = 'network/index.html'
    context_object_name = 'message'
    allow_empty = 0

    def get_queryset(self):
        return Message.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Category - ' + str(context['message'][0].cat),
            cat_selected=context['message'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'network/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *,object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Create User Page')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'network/login.html'

    def get_context_data(self, *,object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Log in')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class MessageAPIList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class MessageAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsOwnerOrReadOnly, )
    # authentication_classes = (TokenAuthentication, )


class MessageAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAdminUser, )


