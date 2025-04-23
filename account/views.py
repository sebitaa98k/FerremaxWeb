from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm, LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user) 
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = RegisterForm()

    return render(request, 'account/register.html', {'form': form})