from django.shortcuts import render, redirect
from .forms import *

from django.contrib.auth.hashers import check_password
from django.contrib import messages

from .models import *

def custom_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = CustomUser.objects.get(username = username)
            if check_password(password, user.password) or password == user.password:
                request.session['user_id'] = str(user.id)
                request.session['username'] = user.username
                request.session['is_logged_in'] = True
                messages.success(request, f"{user.username}logged in")
                return redirect('dashboard:home')
        except CustomUser.DoesNotExist:
            messages.error(request, f"invalid username or password")

    return render(request, 'accounts/login.html')

def custom_register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    form = CustomUserForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/register.html', context)

def custom_logout(request):
    request.session.flush()
    messages.success(request, f"you have logged out")
    return redirect("dashboard:home")

def user_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_logged_in'):
            messages.error(request, f"login is access this page")
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapper