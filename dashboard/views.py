from django.shortcuts               import render, redirect
from django.contrib.auth            import logout, update_session_auth_hash
from django.contrib.auth.forms      import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib                 import messages


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