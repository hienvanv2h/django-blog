from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Profile

def register(request):
  if request.method == "POST":
    form = UserRegisterForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get("username")
      messages.success(request, f"Account created for {username}! You are now able to log in.")
      # Redirect user
      return redirect("login")
  else:
    form = UserRegisterForm()
  return render(request, "users/register.html", {"form": form})

@login_required
def profile(request):
  if request.method == "POST":
    user_form = UserUpdateForm(data=request.POST, instance=request.user)
    prof_form = ProfileUpdateForm(data=request.POST, 
                                  files=request.FILES, 
                                  instance=request.user.profile)
    if user_form.is_valid() and prof_form.is_valid():
      user_form.save()
      prof_form.save()
      messages.success(request, f"Profile updated!")
      return redirect("profile")
  else:
    user_form = UserUpdateForm(instance=request.user)
    prof_form = ProfileUpdateForm(instance=request.user.profile)

  context = {
    "user_form": user_form,
    "prof_form": prof_form
  }
  return render(request, "users/profile.html", context)