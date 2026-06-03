from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login

# Create your views here.
def inicio(request):
  return render(request, 'index.html')

def blog(request):
  return render(request, 'blog.html')

def contact(request):
  return render(request, 'contact.html')

def menu(request):
  return render(request, 'menu.html') 

def about(request):
  return render(request, 'about.html')  

def home(request):
  return render(request, 'home.html')

