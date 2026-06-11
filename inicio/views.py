from django.http import HttpResponse
from django.shortcuts import redirect, render
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

def login_view(request):  # Cambié el nombre para no confundir con la función login de Django
    if request.method == 'POST':
        username = request.POST.get('username')  # Usa .get() para evitar errores
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')  
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
    
    return render(request, 'login.html')


def dashboard(request):
    return render(request, 'dashboard.html')


