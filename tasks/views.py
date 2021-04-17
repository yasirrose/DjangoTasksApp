from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from tasks.models import *
from django.http import HttpResponse, JsonResponse
# Create your views here.
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from tasks.utils import validate_password, duration, is_date_valid,is_date_future_date
from django.contrib.auth.models import User
from django.conf import settings
import re
import os
from django.db import connection

@login_required
def index(request):
    cursor = connection.cursor()
    cursor.execute("""SELECT id,title,description,status,DATE(creation_date) as display_creation_date,DATE(due_date) as display_due_date,created_by_id  FROM tasks_task WHERE id IN (SELECT task_id from tasks_taskuser WHERE user_id = %s) ORDER BY creation_date DESC""", [request.user.id])
    results = cursor.fetchall()
    tasks=[]
    if results is not None:
            columns = [name[0] for name in cursor.description]
            for r in results:
                print(r)
                l = dict(zip(columns, r))
                cl = TaskUser.objects.filter(task_id=r[0]).exclude(user_id=request.user.id).select_related('user')
                l['user'] = cl
                tasks.append(l)
    return render(request, 'index.html', { "tasks": tasks })

def login_view(request):
    if not request.user.is_authenticated:
        return render(request, 'auth/login.html')
    else:
        return redirect('index')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                return HttpResponseRedirect('/')
            else:
                messages.warning(request, 'Your account is inactive.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid Login details given.')
            return redirect('login')
    else:
        messages.error(request, 'Request Failed. Please try again.')
        return redirect('login')

def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            birthday = request.POST.get('birthday')
            context = {"first_name": first_name, "last_name": last_name, "email": email, "username": username, "birthday": birthday}
            if password == confirm_password and password != "":
                if not validate_password(password):
                    messages.error(request, 'Passwords must contain letters and numbers')
                    return render(request, "auth/register.html", context)
                if not all(x.isalpha() or x.isspace() for x in first_name):
                    messages.error(request, 'First name must contain only letters')
                    return render(request, "auth/register.html", context)
                if not all(x.isalpha() or x.isspace() for x in last_name):
                    messages.error(request, 'Last name must contain only letters')
                    return render(request, "auth/register.html", context)

                if not is_date_valid(birthday):
                    messages.error(request, 'Enter a valid date you should be 18 years old to signup')
                    return render(request, "auth/register.html", context)

                try:
                    User.objects.get(username=username)
                    messages.error(request, 'Username is already taken')
                    return render(request, "auth/register.html", context)

                except User.DoesNotExist:
                    user = User.objects.create_user(username, password=password, email=email, first_name=first_name,
                                                    last_name=last_name)
                    Profile.objects.create(date_of_birth=birthday, user_id=user.id)
                    login(request, user)
                    return HttpResponseRedirect('/')
            else:
                messages.error(request, 'Passwords dont match')
                return render(request, "auth/register.html", context)
        else:
            return render(request, "auth/register.html")
    else:
        #
        return redirect('index')

def signout(request):
    logout(request)
    messages.success(request, 'Log Out successfully.')
    return redirect('login')


@login_required
def addtask(request):
    users = User.objects.exclude(id=request.user.id).values()
    view_data = []
    for user in users:
        view_data.append({"id": user['id'], "username": user['username']})

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        usr = request.POST.getlist('user[]')
        status = request.POST.get('status')
        context = {"title": title, "description": description, "due_date": due_date,
                   "user": [int(x) for x in usr], "status": status}
        valid = True
        if not all(x.isalpha() or x.isspace() for x in title):
            messages.error(request, 'Title must contain only letters')
            valid =False
        if not all(x.isalpha() or x.isspace() for x in description):
            messages.error(request, 'Description must contain only letters')
            valid = False

        if not is_date_future_date(due_date):
            messages.error(request, 'Due date cannot be older than today')
            valid = False

        if not valid:
            return render(request, 'addtask.html', {"users": view_data, "data": context})
        else:
            usr.append(request.user.id)
            task = Task.objects.create(title = title, description = description, status = 1 if status == "1" else 0, due_date = due_date,created_by=request.user)
            for u in usr:
                TaskUser.objects.create(task_id=task.id, user_id=u)

            messages.success(request, "Task Created Successfully")
            return HttpResponseRedirect('/')
    else:
        return render(request, 'addtask.html', {"users": view_data})

@login_required
def task_edit(request,id):
    task = Task.objects.filter(id=id).first()
    task.due_date = task.due_date.strftime('%Y-%m-%d')
    task_users = TaskUser.objects.filter(task_id=id).exclude(user_id=request.user.id)
    user_ids = [o.user_id for o in task_users]
    task.user_ids = user_ids
    users = User.objects.exclude(id=request.user.id)

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        usr = request.POST.getlist('user[]')
        status = request.POST.get('status')

        post_data = {"id": id, "title": title, "description": description, "due_date": due_date,
                   "user_ids": [int(x) for x in usr], "status": status}
        valid = True
        if not all(x.isalpha() or x.isspace() for x in title):
            messages.error(request, 'Title must contain only letters')
            valid = False
        if not all(x.isalpha() or x.isspace() for x in description):
            messages.error(request, 'Description must contain only letters')
            valid = False


        if not is_date_future_date(due_date):
            messages.error(request, 'Due date cannot be older than today')
            valid = False

        if not valid:
            return render(request, 'edittask.html', {"users": users, "task": post_data})
        else:
            update_task = Task.objects.get(id=id)
            update_task.title = title
            update_task.description = description
            update_task.status = 1 if status == "1" else 0
            update_task.due_date = due_date
            update_task.save()
            TaskUser.objects.filter(task_id=id).delete()
            usr.append(request.user.id)
            for u in usr:
                TaskUser.objects.create(task_id=task.id, user_id=u)
            messages.success(request, "Task Updated Successfully")
            return HttpResponseRedirect('/')
    else:
        return render(request, 'edittask.html', {"task": task, "users": users })


@login_required
def task_delete(request,id):
    try:
        Task.objects.filter(id=id).delete()
        TaskUser.objects.filter(task_id=id).delete()
        VoiceNote.objects.filter(task_id=id).delete()
        messages.success(request, "Task Deleted Successfully")
        return HttpResponseRedirect('/')
    except:
        messages.error(request, "Request failed please try agian")
        return HttpResponseRedirect('/')

@login_required
def task_details(request,id):
    task = Task.objects.filter(id=id).first()
    task.due_date = task.due_date.strftime('%Y-%m-%d')
    task.creation_date = task.creation_date.strftime('%Y-%m-%d')
    task_users = TaskUser.objects.filter(task_id=id).exclude(user_id=request.user.id)
    user_ids = [o.user_id for o in task_users]
    task.user_ids = user_ids
    users = User.objects.exclude(id=request.user.id)
    return render(request,"taskdetails.html",{"task": task, "users": users})

@csrf_exempt
def add_voice_note(request,task_id):
    if request.method == 'POST':
        customFile = request.FILES['voice_memo']
        nameFile = request.FILES['voice_memo'].name
        ext = nameFile.split(".")[-1]
        request.FILES['voice_memo'].name = request.FILES['voice_memo'].name.replace(ext, "wav")
        size = request.FILES['voice_memo'].size
        note = VoiceNote.objects.create(voice_memo=customFile, size=size,  user_id=request.user.id,task_id=task_id)
        dur = duration(os.path.join(settings.MEDIA_ROOT, str(note.voice_memo)))
        VoiceNote.objects.filter(id=note.id).update(duration=dur)
        return JsonResponse(data={'status': True, 'message': 'Uploaded File'},status=201)
    else:
        return JsonResponse({'status': False, "message": "Invalid Request"}, 400)


@login_required
def delete_voice_note(request,note_id):
    try:
        VoiceNote.objects.filter(id=note_id).delete()
        return JsonResponse(data={"success": True, "message": "note deleted successfully"})
    except:
        return JsonResponse(data={"success": False, "message": "Failed to Delete Note"})



@csrf_exempt
@login_required
def model_form_upload(request):
    if request.method == 'POST':
        customFile = request.FILES['voice_memo']
        nameFile = request.FILES['voice_memo'].name
        ext = nameFile.split(".")[-1]
        request.FILES['voice_memo'].name = request.FILES['voice_memo'].name.replace(ext, "wav")
        size = request.FILES['voice_memo'].size
        note = VoiceNote.objects.create(voice_memo=customFile, size=size,  user_id=request.user.id,task_id=1)
        dur = duration(os.path.join(settings.MEDIA_ROOT, str(note.voice_memo)))
        VoiceNote.objects.filter(id=note.id).update(duration=dur)
    return JsonResponse({'status': True, 'message': 'Uploaded File'})

@login_required
def get_recordings(request):
    recordings = VoiceNote.objects.all()
    data = [recording.to_dict_json() for recording in recordings]
    return render(request, 'view_tasks.html', {'recordings': data})

@login_required
def task_voice_notes(request,task_id):
    recordings = VoiceNote.objects.filter(task_id=task_id).order_by('creation_date')
    string_view = render_to_string('view_tasks.html', {'recordings': recordings})
    return JsonResponse({"view": string_view})
