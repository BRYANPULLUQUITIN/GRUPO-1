from django.shortcuts               import render, redirect
from django.contrib.auth            import logout, update_session_auth_hash
from django.contrib.auth.forms      import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib                 import messages
from django.contrib.auth.models import User
from dashboard.models import Profile


def dashboard(request):
    return render(request, 'private/dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ── Perfil (vista de lectura) ─────────────────────────────────
@login_required
def profile_view(request):
    departamentos = [
        'Tecnología', 'Recursos Humanos', 'Finanzas',
        'Marketing', 'Operaciones', 'Ventas', 'Legal',
    ]
    return render(request, 'private/perfil.html', {
        'departamentos': departamentos,
    })


# ── Perfil (actualización) ────────────────────────────────────
@login_required
def profile_update(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_profile':
            request.user.first_name = request.POST.get('first_name', '')
            request.user.last_name  = request.POST.get('last_name', '')
            request.user.email      = request.POST.get('email', '')
            request.user.save()

            profile = request.user.profile
            profile.telefono          = request.POST.get('telefono', '')
            profile.cargo             = request.POST.get('cargo', '')
            profile.departamento      = request.POST.get('departamento', '')
            profile.bio               = request.POST.get('bio', '')
            fecha = request.POST.get('fecha_nacimiento', '')
            if fecha:
                profile.fecha_nacimiento = fecha
            if 'foto' in request.FILES:
                profile.foto = request.FILES['foto']
            profile.save()
            messages.success(request, 'Perfil actualizado correctamente.')

        elif action == 'change_password':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                update_session_auth_hash(request, form.save())
                messages.success(request, 'Contraseña actualizada correctamente.')
            else:
                for error in form.errors.values():
                    messages.error(request, error[0])

    return redirect('profile')


# ── Configuración ─────────────────────────────────────────────
@login_required
def settings_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            update_session_auth_hash(request, form.save())
            messages.success(request, 'Contraseña actualizada correctamente.')
            return redirect('settings')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'private/settings.html', {'form': form})


# ── Usuarios ──────────────────────────────────────────────────
@login_required
def usuarios_view(request):
    usuarios = User.objects.all().order_by('-date_joined')
    departamentos = [
        'Tecnología', 'Recursos Humanos', 'Finanzas',
        'Marketing', 'Operaciones', 'Ventas', 'Legal',
    ]
    return render(request, 'private/usuarios.html', {
        'usuarios': usuarios,
        'departamentos': departamentos,
    })

@login_required
def usuario_crear(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        email      = request.POST.get('email', '').strip()
        password   = request.POST.get('password', '')
        cargo      = request.POST.get('cargo', '')
        departamento = request.POST.get('departamento', '')
        is_staff   = request.POST.get('is_staff') == 'on'

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Ya existe un usuario con ese correo.')
            return redirect('usuarios')

        username = email.split('@')[0]
        base = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f'{base}{counter}'
            counter += 1

        user = User.objects.create_user(
            username=username, email=email,
            password=password,
            first_name=first_name, last_name=last_name,
            is_staff=is_staff,
        )
        # El perfil se crea por señal, solo actualizamos campos extra
        profile = user.profile
        profile.cargo        = cargo
        profile.departamento = departamento
        if 'foto' in request.FILES:
            profile.foto = request.FILES['foto']
        profile.save()

        messages.success(request, f'Usuario {user.get_full_name()} creado correctamente.')
    return redirect('usuarios')

@login_required
def usuario_eliminar(request, user_id):
    if request.method == 'POST':
        try:
            user = User.objects.get(pk=user_id)
            if user == request.user:
                messages.error(request, 'No puedes eliminar tu propia cuenta.')
            else:
                nombre = user.get_full_name()
                user.delete()
                messages.success(request, f'Usuario {nombre} eliminado.')
        except User.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')
    return redirect('usuarios')

@login_required
def usuario_toggle(request, user_id):
    if request.method == 'POST':
        try:
            user = User.objects.get(pk=user_id)
            if user != request.user:
                user.is_active = not user.is_active
                user.save()
                estado = 'activado' if user.is_active else 'desactivado'
                messages.success(request, f'Usuario {user.get_full_name()} {estado}.')
        except User.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')
    return redirect('usuarios')

def calendario(request):
    return render(request, 'private/calendario.html')

def usuario_editar(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Usuario no encontrado.')
        return redirect('usuarios')

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name  = request.POST.get('last_name', '').strip()
        user.email      = request.POST.get('email', '').strip()
        user.is_staff   = request.POST.get('is_staff') == 'on'
        user.save()

        profile = user.profile
        profile.cargo        = request.POST.get('cargo', '')
        profile.departamento = request.POST.get('departamento', '')
        if 'foto' in request.FILES:
            profile.foto = request.FILES['foto']
        profile.save()

        messages.success(request, f'Usuario {user.get_full_name()} actualizado correctamente.')
        return redirect('usuarios')

    departamentos = [
        'Tecnología', 'Recursos Humanos', 'Finanzas',
        'Marketing', 'Operaciones', 'Ventas', 'Legal',
    ]
    return render(request, 'private/usuario_editar.html', {
        'usuario': user,
        'departamentos': departamentos,
    })

import json
from django.http import JsonResponse
from dashboard.models import Evento

# ── Calendario ────────────────────────────────────────────────
@login_required
def calendario_view(request):
    eventos = Evento.objects.all()
    return render(request, 'private/calendario.html', {
        'eventos': eventos,
    })

@login_required
def evento_crear(request):
    if request.method == 'POST':
        titulo      = request.POST.get('titulo', '').strip()
        tipo        = request.POST.get('tipo', 'otro')
        descripcion = request.POST.get('descripcion', '')
        fecha       = request.POST.get('fecha', '')
        hora        = request.POST.get('hora') or None
        cantidad    = request.POST.get('cantidad') or None
        unidad      = request.POST.get('unidad', '')

        if titulo and fecha:
            Evento.objects.create(
                titulo=titulo, tipo=tipo,
                descripcion=descripcion, fecha=fecha,
                hora=hora, cantidad=cantidad,
                unidad=unidad, creado_por=request.user,
            )
            messages.success(request, f'Evento "{titulo}" creado correctamente.')
        else:
            messages.error(request, 'El título y la fecha son obligatorios.')

    return redirect('calendario')

@login_required
def evento_eliminar(request, evento_id):
    if request.method == 'POST':
        try:
            evento = Evento.objects.get(pk=evento_id)
            titulo = evento.titulo
            evento.delete()
            messages.success(request, f'Evento "{titulo}" eliminado.')
        except Evento.DoesNotExist:
            messages.error(request, 'Evento no encontrado.')
    return redirect('calendario')

@login_required
def eventos_json(request):
    eventos = Evento.objects.all()
    data = []
    colores = {
        'vacuna':      '#7c3aed',
        'veterinario': '#2563eb',
        'entrada':     '#059669',
        'salida':      '#dc2626',
        'observacion': '#d97706',
        'otro':        '#64748b',
    }
    for e in eventos:
        data.append({
            'id':    e.pk,
            'title': e.titulo,
            'start': str(e.fecha),
            'color': colores.get(e.tipo, '#64748b'),
            'extendedProps': {
                'tipo':        e.tipo,
                'descripcion': e.descripcion or '',
                'hora':        str(e.hora) if e.hora else '',
                'cantidad':    str(e.cantidad) if e.cantidad else '',
                'unidad':      e.unidad or '',
                'creado_por':  e.creado_por.get_full_name() if e.creado_por else '',
            }
        })
    return JsonResponse(data, safe=False)