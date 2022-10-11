from django.shortcuts import render, redirect
from django.contrib.auth.views import * 
from django.views.generic import CreateView, TemplateView

from .models import Profile
from .forms import *


class SignUpView(CreateView):
    model = Profile
    template_name = 'registration/profile_form.html'
    form_class = SignUpForm

    def form_valid(self, form):
        form.save()
        return redirect('users:login')


class SignInView(LoginView):
    template_name = 'registration/login.html'


class SignOutView(LogoutView):
    pass