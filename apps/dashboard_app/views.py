from django.shortcuts import render, HttpResponse, redirect
from .models import *
import datetime

def index(request):
    if 'curUser' not in request.session:
        return redirect('/')
    if Users.objects.get(id = request.session['curUser']).user_level == 9:
        return redirect('/dashboard/admin')
    users = Users.objects.all()
    for user in users:
        user.created_at = user.created_at.date()
        if user.user_level == 9:
            user.user_level = 'admin'
        else:
            user.user_level = 'normal'
    context = {
        'users' : users
    }
    return render(request, 'dashboard_app/index.html', context)

def index_admin(request):
    if 'curUser' not in request.session:
        return redirect('/') 
    if Users.objects.get(id = request.session['curUser']).user_level != 9:
        return redirect('/dashboard')
    users = Users.objects.all()
    for user in users:
        user.created_at = user.created_at.date()
        if user.user_level == 9:
            user.user_level = 'admin'
        else:
            user.user_level = 'normal'
    context = {
        'users' : users
    }
    return render(request, 'dashboard_app/index_admin.html', context)

def delete_user(request, user_id):
    if Users.objects.get(id = request.session['curUser']).user_level != 9:
        return redirect('/dashboard')
    if user_id == request.session['curUser']:
        return redirect('/dashboard/admin')
    user = Users.objects.get(id = user_id)
    user.delete()
    return redirect('/dashboard/admin')
