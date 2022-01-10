from django.db.models import fields
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, PostView, Like, Comment

class PostListView(ListView):
    model = Post

class PostDetailView(DetailView):
    model = Post

class PostCreateView(CreateView):
    model = Post
    fields = (
        'title',
        'content',
        'thumbnail',
        'author',
        'slug',
    )

class PostUpdateView(UpdateView):
    model = Post
    fields = (
        'title',
        'content',
        'thumbnail',
        'author',
        'slug',
    )

class PostDeletView(DeleteView):
    model = Post
    success_url = '/'
    