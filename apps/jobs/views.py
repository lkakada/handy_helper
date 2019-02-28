from django.shortcuts import render, redirect
from .models import Job
from ..jobs.models import User
from django.contrib import messages

# Create your views here.


def dashboard(request):
    context = {
        'logged_in': User.objects.get(id=request.session['user_id']),
        'jobs': Job.objects.all().exclude(users_add=request.session['user_id']),
        'myJobs': Job.objects.filter(users_add=request.session['user_id'])
    }
    print(Job.objects.filter(users_add=request.session['user_id']))
    return render(request, 'jobs/dashboard.html', context)


def add(request):
    return render(request, 'jobs/add.html')


def add_job(request):
    errors = Job.objects.jobValidation(request.POST)
    this_user = User.objects.get(id=request.session['user_id'])
    if request.POST:
        if errors:
            for error in errors:
                messages.error(request, error)
                request.session['title'] = request.POST['title']
                request.session['description'] = request.POST['description']
                request.session['location'] = request.POST['location']
            return redirect('jobs:add')
    Job.objects.create(
        title=request.POST['title'], description=request.POST['description'], location=request.POST['location'], creator=this_user)
    return redirect('jobs:dashboard')


def move(request, id):
    this_user = User.objects.get(id=request.session['user_id'])
    this_job = Job.objects.get(id=id)
    this_user.add_jobs.add(this_job)
    return redirect('jobs:dashboard')


def view(request, id):
    context = {
        'job': Job.objects.get(id=id)
    }
    return render(request, 'jobs/view.html', context)


def edit(request, id):
    context = {
        'job': Job.objects.get(id=id)
    }

    return render(request, 'jobs/edit.html', context)


def update(request):
    errors = Job.objects.jobValidation(request.POST)
    if request.POST:
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('jobs:edit', id=request.POST['id'])
        Job.objects.get(id=request.POST['job_id']).updatedJob(request.POST)
        messages.success(request, "Job has been updated successfully.")
    return redirect('jobs:dashboard')


def delete(request, id):
    context = {
        'job': Job.objects.get(id=id)
    }
    return render(request, 'jobs/delete.html', context)


def destroy(request):
    if request.POST:
        Job.objects.get(id=request.POST['job_id']).delete()
        messages.error(request, "Job has been deleted successfully.")
    return redirect('jobs:dashboard')
