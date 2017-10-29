from django.shortcuts import render, redirect, HttpResponse
from ..login.models import User
def index(request):
    if not 'user_id' in request.session:
        return redirect("login:index")
    logged_user=User.objects.get(id=request.session['user_id'])
    context={
    'friends':User.objects.filter(mapping=logged_user),
    'notfriends':User.objects.exclude(mapping=logged_user).exclude(id=request.session['user_id'])
        }
    return render(request, 'friends/index.html', context)
def show(request, id):
    if not 'user_id' in request.session:
        return redirect("login:index")
    context={
        'alias':User.objects.get(id=id).alias,
        'name':User.objects.get(id=id).name,
        'email':User.objects.get(id=id).email,
        }
    return render(request, 'friends/show.html', context)
def add(request, id):
    if not 'user_id' in request.session:
        return redirect("login:index")
    User.objects.get(id=request.session['user_id']).mapping.add(User.objects.get(id=id))
    return redirect('friends:index')
def remove(request, id):
    if not 'user_id' in request.session:
        return redirect("login:index")
    User.objects.get(id=request.session['user_id']).mapping.remove(User.objects.get(id=id))
    return redirect('friends:index')
