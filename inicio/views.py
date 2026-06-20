from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages          
from django.contrib.auth.decorators import login_required

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

def login_view(request):
    # Si ya está autenticado, ir al dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        action = request.POST.get('action')

        # ══ LOGIN ══════════════════════════════════════════
        if action == 'login':
            email    = request.POST.get('email', '').strip()
            password = request.POST.get('password', '')

            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, 'No existe una cuenta con ese correo electrónico.')
                return render(request, 'login.html')

            user = authenticate(request, username=user_obj.username, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('splash')   # ← pasa por splash antes del dashboard
            else:
                messages.error(request, 'Contraseña incorrecta. Inténtalo de nuevo.')
                return render(request, 'login.html')

        # ══ REGISTRO ═══════════════════════════════════════
        elif action == 'register':
            full_name        = request.POST.get('full_name', '').strip()
            email            = request.POST.get('email', '').strip()
            password         = request.POST.get('password', '')
            confirm_password = request.POST.get('confirm_password', '')

            if password != confirm_password:
                messages.error(request, 'Las contraseñas no coinciden.')
                return render(request, 'login.html')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Ya existe una cuenta con ese correo. Inicia sesión.')
                return render(request, 'login.html')

            # Crear usuario
            parts    = full_name.split(' ', 1)
            username = email.split('@')[0]

            # username único
            base = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f'{base}{counter}'
                counter += 1

            user = User.objects.create_user(
                username   = username,
                email      = email,
                password   = password,
                first_name = parts[0],
                last_name  = parts[1] if len(parts) > 1 else '',
            )
            # El Profile se crea solo por la señal post_save
            messages.success(request, f'¡Bienvenido {parts[0]}! Cuenta creada correctamente.')
            return redirect('login')

    return render(request, 'login.html')

def splash_view(request):
    return render(request, 'splash.html')

def dashboard(request):
    return render(request, 'dashboard.html')



