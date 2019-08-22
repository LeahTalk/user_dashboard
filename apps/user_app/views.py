from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt
import re
import datetime


def new_user(request):
    if 'curUser' not in request.session:
        return redirect('/') 
    if Users.objects.get(id = request.session['curUser']).user_level != 9:
        return redirect('/dashboard')
    return render(request, "user_app/add.html")

def edit_user(request, user_id):
    if 'curUser' not in request.session:
        return redirect('/') 
    if Users.objects.get(id = request.session['curUser']).user_level != 9:
        return redirect('/dashboard')
    if len(Users.objects.filter(id = user_id)) == 0:
        return redirect('/dashboard/admin')
    context = {
        'user' : Users.objects.get(id = user_id)
    }
    return render(request, "user_app/edit_user.html", context)

def process_user_edits(request, user_id, form_type):
    if 'curUser' not in request.session:
        return redirect('/') 
    errors = Users.objects.user_validator(request.POST)
    #Make sure we don't compare against the user's original email if they keep it the same
    users = Users.objects.exclude(id = user_id)
    for user in users:
        if user.email == request.POST['email']:
            errors['exists'] = "A user with this email already exists!"
            break
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        if form_type == 'admin': 
            return redirect('/users/edit/' + str(user_id))
        return redirect('/users/edit')
    user = Users.objects.get(id = user_id)
    user.email = request.POST['email']
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    #Check if this is coming from profile edit, or the admin edit
    if form_type == 'admin':
        user_level = 0
        if request.POST['user_level'] == 'admin':
            user_level = 9
        user.user_level = user_level
    user.save()
    return redirect('/users/show/' + str(user_id))

def process_password_edits(request, user_id, form_type):
    if 'curUser' not in request.session:
        return redirect('/') 
    errors = Users.objects.user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        if form_type == 'admin': 
            return redirect('/users/edit/' + str(user_id))
        return redirect('/users/edit')
    print('hi again')
    password = request.POST['regPassword']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()) 
    user = Users.objects.get(id = user_id)
    user.pw_hash = pw_hash
    user.save()
    return redirect('/users/show/' + str(user_id))

def edit_profile(request):
    if 'curUser' not in request.session:
        return redirect('/')
    context = {
        'user' : Users.objects.get(id = request.session['curUser'])
    }
    return render(request, "user_app/edit_profile.html", context)

def edit_description(request):
    if 'curUser' not in request.session:
        return redirect('/') 
    user = Users.objects.get(id = request.session['curUser'])
    user.desc = request.POST['desc']
    user.save()
    return redirect('/users/show/' + str(user.id))

def message_board(request, user_id):
    if 'curUser' not in request.session:
        return redirect('/')
    if len(Users.objects.filter(id = user_id)) == 0:
        return redirect('/dashboard')
    user = Users.objects.get(id = user_id)
    user.created_at = user.created_at.date()
    all_messages = user.received_messages.all()
    for message in all_messages:
        created = message.created_at
        date_string = created.strftime('%B %d{suffix} %Y')
        day = created.day
        if 3 < day < 21 or 23 < day < 31:
            the_suffix = 'th'
        else:
            the_suffix = {1: 'st', 2: 'nd', 3: 'rd'}[day % 10]
        message.created_at = date_string.format(suffix=the_suffix)
    reversed_messages = all_messages[::-1]
    context = {
        'user' : user,
        'user_messages' : reversed_messages
    }
    return render(request, "user_app/messages.html", context)

def create_message(request, user_id):
    if 'curUser' not in request.session:
        return redirect('/') 
    errors = Messages.objects.message_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/users/show/' + str(user_id))
    Messages.objects.create(content = request.POST['content'], message_receiver = Users.objects.get(id = user_id),
                            message_owner = Users.objects.get(id = request.session['curUser']))
    return redirect('/users/show/' + str(user_id))

def create_comment(request, user_id):
    if 'curUser' not in request.session:
        return redirect('/') 
    errors = Comments.objects.comment_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/users/show/' + str(user_id))
    Comments.objects.create(content = request.POST['content'], related_message = Messages.objects.get(id = request.POST['message_id']),
                             comment_owner = Users.objects.get(id = request.session['curUser']))
    return redirect('/users/show/' + str(user_id))

def delete_message(request, user_id):
    if 'curUser' not in request.session:
        return redirect('/') 
    message = Messages.objects.get(id = request.POST['message_id'])
    message.delete()
    return redirect('/users/show/' + str(user_id))

def delete_comment(request, user_id):
    if 'curUser' not in request.session:
        return redirect('/') 
    comment = Comments.objects.get(id = request.POST['comment_id'])
    comment.delete()
    return redirect('/users/show/' + str(user_id))

def process_new_user(request):
    if 'curUser' not in request.session:
        return redirect('/') 
    errors = Users.objects.user_validator(request.POST)
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if not EMAIL_REGEX.match(request.POST['email']):        
        errors['email'] = ("Invalid email address!")
    if Users.objects.filter(email=request.POST['email']).exists():
        errors['exists'] = "A user with this email already exists!"
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/users/new')
    password = request.POST['regPassword']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()) 
    Users.objects.create(first_name=request.POST['first_name'], last_name = request.POST['last_name'],
            email = request.POST['email'], pw_hash=pw_hash, user_level = 0)
    user = Users.objects.get(id = request.session['curUser'])
    return redirect('/dashboard/admin')
