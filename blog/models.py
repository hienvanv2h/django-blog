from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
  title = models.CharField(max_length=100)
  content = models.TextField()
  date_posted = models.DateTimeField(default=timezone.now)
  # reference to User table, delete all posts of this user when user is deleted
  author = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.title
  
  # This method required to tell Django to URL of ant specific post instance
  def get_absolute_url(self):
    return reverse("post-detail", kwargs={"pk": self.pk})