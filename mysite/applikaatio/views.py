from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from .forms import TeamForm
import http.client
import json


# Create your views here.


def HomePageView(request):
    context = {
        'posts': Post.objects.all()
        }
    return render(request, 'applikaatio/HomePageView.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'applikaatio/HomePageView.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def testi(request):
    search_result = {}
    if 'team' in request.GET:
        form = TeamForm(request.GET)
        if form.is_valid():
            search_result = form.search()
    else:
        form = TeamForm()
    return render(request, 'applikaatio/testi.html', {'form': form, 'search_result': search_result})
