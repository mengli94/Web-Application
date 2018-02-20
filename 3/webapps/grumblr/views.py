# -*- coding: utf-8 -*-
# Create your views here.
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from grumblr.models import *

@login_required
def home(request):
	posts = Post.objects.all().order_by("-time")
	context = {'posts' : posts, 'user' : request.user}
	return render(request, 'grumblr/global stream.html', context)

@login_required
def add_post(request):
	errors = []

	if not 'post' in request.POST or not request.POST['post']:
		errors.append('You must enter a post to add')
	else:
		new_post = Post(text=request.POST['post'], user=request.user)
		new_post.save()

	posts = Post.objects.all().order_by("-time")
	context = {'posts':posts, 'errors':errors, 'user':request.user}
	return render(request, 'grumblr/global stream.html', context)

@login_required
def profile(request, username):
    errors = []
    
    if len(User.objects.filter(username = username)) <= 0:
        errors.append('User does not exist.')
    
    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user).order_by("-time")

    context = {'posts' : posts, 'errors' : errors, 'user' : user}
    return render(request, 'grumblr/my profile.html', context)

def register(request):
    context = {}

    if request.method == 'GET':
        return render(request, 'grumblr/register.html', context)

    errors = []
    context['errors'] = errors
           
    if not 'username' in request.POST or not request.POST['username']:
		errors.append('Username is required.')
    else:
		context['username'] = request.POST['username']

    if not 'firstname' in request.POST or not request.POST['firstname']:
		errors.append('User Firstname is required.')
    else:
		context['firstname'] = request.POST['firstname']

    if not 'lastname' in request.POST or not request.POST['lastname']:
		errors.append('User Lastname is required.')
    else:
		context['lastname'] = request.POST['lastname']

    if not 'password1' in request.POST or not request.POST['password1']:
        errors.append('Password is required.')
    if not 'password2' in request.POST or not request.POST['password2']:
        errors.append('Confirm password is required.')

    if 'password1' in request.POST and 'password2' in request.POST \
       and request.POST['password1'] and request.POST['password2'] \
       and request.POST['password1'] != request.POST['password2']:
        errors.append('Passwords did not match.')

    if len(User.objects.filter(username = request.POST['username'])) > 0:
        errors.append('Username is already taken.')

    if errors:
        return render(request, 'grumblr/register.html', context)

    new_user = User.objects.create_user(username=request.POST['username'], \
                                        first_name=request.POST['firstname'], \
                                        last_name=request.POST['lastname'], \
                                        password=request.POST['password1'])
    new_user.save()

    new_user = authenticate(username=request.POST['username'], \
                            password=request.POST['password1'])
    login(request, new_user)

    return redirect('/grumblr')

