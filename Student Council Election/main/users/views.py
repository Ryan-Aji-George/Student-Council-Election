from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('login')
