from django.db.models import fields
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import View
from .models import Post, PostView, Like, Comment, User
from .forms import PostForm, CommentForm

class PostListView(ListView):
    model = Post

class PostDetailView(DetailView):
    model = Post

    def post(self, *args, **kwargs):
        form = CommentForm(self.request.POST)
        if form.is_valid():
            post = self.get_object()
            comment = form.instance
            comment.user = self.request.user
            comment.post = post
            comment.save()
            return redirect("detail", slug=post.slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form' : CommentForm()
        })
        return context

    def get_object(self, **kwagrs):
        object = super().get_object(**kwagrs)
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(user=self.request.user, post=object)
        return object

class PostCreateView(CreateView):
    form_class = PostForm
    model = Post
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type' : 'create'
        })
        return context
    

class PostUpdateView(UpdateView):
    form_class = PostForm
    model = Post
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type' : 'update'
        })
        return context

class PostDeletView(DeleteView):
    model = Post
    success_url = '/'
    

def like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like_qs = Like.objects.filter(user=request.user, post=post)
    if like_qs.exists():
        #unlike the post
        like_qs[0].delete()
        return redirect ('detail', slug=slug)
    Like.objects.create(user=request.user, post=post)
    return redirect ('detail', slug=slug)