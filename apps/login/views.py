from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
# Create your views here.
def index(request):

    return render(request, "login/index.html")
def register(request):
    if request.method!='POST':
        return redirect('/')
    response_from_model=User.objects.validate_user_r(request.POST)
    if response_from_model['status']:
        request.session['user_id']=response_from_model['id']
        return redirect('/success')
    for error, content in response_from_model['errors'].items():
        messages.error(request, content, extra_tags=error)
    return redirect('/')
def login(request):
    if request.method!='POST':
        return redirect('/')
    response_from_model=User.objects.validate_user_l(request.POST)
    if response_from_model['status']:
        request.session['user_id']=response_from_model['id']
        return redirect('/success')
    for error, content in response_from_model['errors'].items():
        messages.error(request, content, extra_tags=error)
    return redirect('/')
def success(request):
    if 'user_id' in request.session:
        return redirect('friends:index')
    return redirect('/')
