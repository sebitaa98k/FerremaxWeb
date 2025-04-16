from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        
        return redirect('home')
    return render(request, 'account/login.html')