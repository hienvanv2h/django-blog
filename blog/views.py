from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)
from django.contrib.auth.models import User
from .models import Post

# def home(request):
#   context = {
#     "posts": Post.objects.all()
#   }
#   return render(request, "blog/home.html", context)

class PostListView(ListView):
  model = Post
  template_name = "blog/home.html"    # Default value: <app>/<model>_<viewtype>.html
  context_object_name = "posts"   # change object list name that will be reference from template
  ordering = ["-date_posted"]   # latest posts show first
  paginate_by = 5


class UserPostListView(ListView):
  model = Post
  template_name = "blog/user_posts.html"    # Default value: <app>/<model>_<viewtype>.html
  context_object_name = "posts"   # change object list name that will be reference from template
  # ordering = ["-date_posted"]
  paginate_by = 5

  # Override
  def get_queryset(self) -> QuerySet[Any]:
    user = get_object_or_404(User, username=self.kwargs.get("username"))
    return Post.objects.filter(author=user).order_by("-date_posted")


class PostDetailView(DetailView):
  model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
  model = Post
  fields = ["title", "content"]
  # Override method
  def form_valid(self, form: BaseModelForm) -> HttpResponse:
    # set instance has author prop to current login user
    form.instance.author = self.request.user
    return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Post
  fields = ["title", "content"]
  # Override method
  def form_valid(self, form: BaseModelForm) -> HttpResponse:
    # set instance has author prop to current login user
    form.instance.author = self.request.user
    return super().form_valid(form)

  def test_func(self) -> bool | None:
    post = self.get_object()    # get current post
    if(self.request.user == post.author):
      return True
    return False
  

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Post
  success_url = "/"
  def test_func(self) -> bool | None:
    post = self.get_object()    # get current post
    if(self.request.user == post.author):
      return True
    return False

def about(request):
  return render(request, "blog/about.html", {"title": "About"})