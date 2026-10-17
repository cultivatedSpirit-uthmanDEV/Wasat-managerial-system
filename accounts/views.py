from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from django.contrib.auth import  login as auth_login, logout as auth_logout


# Create your views here.

def welcome(request):
    return render(request, "accounts/welcome.html")

def register(request):

    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('dashboard.html/')

    context = {
        'form' : form
    }

    return render(request, 'accounts/register.html', context )

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data= request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('/wasatasoke/dashboard/')
    else:
        form = AuthenticationForm()

    context = {
       "form" : form,
      }
    
    return render(request, 'accounts/login.html',context)

def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('/login/')
    return render(request, "accounts/logout.hmtl")




