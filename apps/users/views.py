from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

# Create your views here.


def index(request):
    return render(request, 'users/index.html')


def success(request):
    return render(request, 'users/success.html')


def register(request):
    errors = User.objects.basic_validation(request.POST)
    if request.POST:
        if errors:
            for error in errors:
                messages.error(request, error)
                request.session['first_name'] = request.POST['first_name']
                request.session['last_name'] = request.POST['last_name']
                request.session['email'] = request.POST['email']
            return redirect('users:index')
    user = User.objects.user_create(request.POST)
    request.session['user_id'] = user.id
    request.session['first_name'] = user.first_name
    messages.success(request, "You have been registered successfully.")
    return redirect('jobs:dashboard')


def login(request):
    if request.POST:
        # send information to model to check the errors
        valid, result = User.objects.login(request.POST)
        # if error
        if not valid:
            messages.error(request, result)
            return redirect('users:index')
        # log user in
        else:
            request.session['user_id'] = result
            messages.success(
                request, "You have been logged in successfully.")
        return redirect('jobs:dashboard')


def logout(request):
    request.session.clear()
    messages.success(request, "You have been logged out successfully.")
    return redirect('users:index')
