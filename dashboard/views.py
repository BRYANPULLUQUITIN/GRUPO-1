from django.shortcuts               import render, redirect
from django.contrib.auth            import logout, update_session_auth_hash
from django.contrib.auth.forms      import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib                 import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from dashboard.models import Profile, Evento, Cliente, Pedido


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


# ── Pedidos ───────────────────────────────────────────────────
@login_required
def pedidos_view(request):
    pedidos  = Pedido.objects.select_related('cliente', 'usuario').all()
    clientes = Cliente.objects.all().order_by('nombres')
    usuarios = User.objects.filter(is_active=True).order_by('first_name')
    return render(request, 'private/pedidos.html', {
        'pedidos':  pedidos,
        'clientes': clientes,
        'usuarios': usuarios,
        'pendientes_count':  pedidos.filter(estado='pendiente').count(),
        'completados_count': pedidos.filter(estado='completado').count(),
        'cancelados_count':  pedidos.filter(estado='cancelado').count(),
    })


@login_required
def pedido_crear(request):
    if request.method == 'POST':
        try:
            Pedido.objects.create(
                cliente_id  = request.POST.get('cliente'),
                usuario_id  = request.POST.get('usuario') or request.user.pk,
                fecha       = request.POST.get('fecha'),
                estado      = request.POST.get('estado', 'pendiente'),
                total       = request.POST.get('total', 0) or 0,
            )
            messages.success(request, 'Pedido creado correctamente.')
        except Exception as e:
            messages.error(request, f'Error al crear pedido: {e}')
    return redirect('pedidos')


@login_required
def pedido_editar(request, pedido_id):
    if request.method == 'POST':
        try:
            pedido            = Pedido.objects.get(pk=pedido_id)
            pedido.cliente_id   = request.POST.get('cliente')
            pedido.usuario_id   = request.POST.get('usuario') or request.user.pk
            pedido.fecha        = request.POST.get('fecha')
            pedido.estado       = request.POST.get('estado', 'pendiente')
            pedido.total        = request.POST.get('total', 0) or 0
            pedido.save()
            messages.success(request, f'Pedido #{pedido_id} actualizado.')
        except Pedido.DoesNotExist:
            messages.error(request, 'Pedido no encontrado.')
    return redirect('pedidos')


@login_required
def pedido_eliminar(request, pedido_id):
    if request.method == 'POST':
        try:
            Pedido.objects.get(pk=pedido_id).delete()
            messages.success(request, f'Pedido #{pedido_id} eliminado.')
        except Pedido.DoesNotExist:
            messages.error(request, 'Pedido no encontrado.')
    return redirect('pedidos')


@login_required
def cliente_crear(request):
    if request.method == 'POST':
        nombres  = request.POST.get('nombres', '').strip()
        if nombres:
            Cliente.objects.create(
                nombres   = nombres,
                apellidos = request.POST.get('apellidos', ''),
                telefono  = request.POST.get('telefono', ''),
                direccion = request.POST.get('direccion', ''),
                correo    = request.POST.get('correo', ''),
            )
            messages.success(request, 'Cliente creado correctamente.')
        else:
            messages.error(request, 'El nombre es obligatorio.')
    return redirect('pedidos')


@login_required
def clientes_json(request):
    clientes = Cliente.objects.all().order_by('nombres')
    return JsonResponse(
        [{'id': c.pk, 'nombre': c.get_full_name()} for c in clientes],
        safe=False
    )

# ═══════════════════════════════════════════════════════════════
# AGREGAR ESTE BLOQUE A dashboard/views.py
# (usa los mismos imports que ya tienes: render, redirect, messages,
#  login_required, User, JsonResponse — solo agrega los modelos)
# ═══════════════════════════════════════════════════════════════
from dashboard.models import Galpon, Ave, Alimento, Alimentacion  # sumar a tu import existente


# ── Galpones ──────────────────────────────────────────────────
@login_required
def galpones_view(request):
    galpones = Galpon.objects.all().order_by('nombre')
    return render(request, 'private/galpones.html', {'galpones': galpones})


@login_required
def galpon_crear(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        if nombre:
            Galpon.objects.create(
                nombre=nombre,
                capacidad=request.POST.get('capacidad') or 0,
                ubicacion=request.POST.get('ubicacion', ''),
                descripcion=request.POST.get('descripcion', ''),
            )
            messages.success(request, f'Galpón "{nombre}" creado correctamente.')
        else:
            messages.error(request, 'El nombre es obligatorio.')
    return redirect('galpones')


@login_required
def galpon_editar(request, galpon_id):
    try:
        galpon = Galpon.objects.get(pk=galpon_id)
    except Galpon.DoesNotExist:
        messages.error(request, 'Galpón no encontrado.')
        return redirect('galpones')

    if request.method == 'POST':
        galpon.nombre = request.POST.get('nombre', '').strip()
        galpon.capacidad = request.POST.get('capacidad') or 0
        galpon.ubicacion = request.POST.get('ubicacion', '')
        galpon.descripcion = request.POST.get('descripcion', '')
        galpon.save()
        messages.success(request, f'Galpón "{galpon.nombre}" actualizado.')
    return redirect('galpones')


@login_required
def galpon_eliminar(request, galpon_id):
    if request.method == 'POST':
        try:
            galpon = Galpon.objects.get(pk=galpon_id)
            nombre = galpon.nombre
            galpon.delete()
            messages.success(request, f'Galpón "{nombre}" eliminado.')
        except Galpon.DoesNotExist:
            messages.error(request, 'Galpón no encontrado.')
    return redirect('galpones')


# ── Aves ──────────────────────────────────────────────────────
@login_required
def aves_view(request):
    aves = Ave.objects.select_related('galpon').all().order_by('-fecha_ingreso')
    galpones = Galpon.objects.all().order_by('nombre')
    return render(request, 'private/aves.html', {
        'aves': aves,
        'galpones': galpones,
    })


@login_required
def ave_crear(request):
    if request.method == 'POST':
        raza = request.POST.get('raza', '').strip()
        if raza:
            Ave.objects.create(
                raza=raza,
                cantidad=request.POST.get('cantidad') or 0,
                fecha_ingreso=request.POST.get('fecha_ingreso'),
                estado=request.POST.get('estado', 'activo'),
                galpon_id=request.POST.get('galpon') or None,
            )
            messages.success(request, f'Registro de aves "{raza}" creado correctamente.')
        else:
            messages.error(request, 'La raza es obligatoria.')
    return redirect('aves')


@login_required
def ave_editar(request, ave_id):
    try:
        ave = Ave.objects.get(pk=ave_id)
    except Ave.DoesNotExist:
        messages.error(request, 'Registro de aves no encontrado.')
        return redirect('aves')

    if request.method == 'POST':
        ave.raza = request.POST.get('raza', '').strip()
        ave.cantidad = request.POST.get('cantidad') or 0
        ave.fecha_ingreso = request.POST.get('fecha_ingreso')
        ave.estado = request.POST.get('estado', 'activo')
        ave.galpon_id = request.POST.get('galpon') or None
        ave.save()
        messages.success(request, f'Registro de aves "{ave.raza}" actualizado.')
    return redirect('aves')


@login_required
def ave_eliminar(request, ave_id):
    if request.method == 'POST':
        try:
            ave = Ave.objects.get(pk=ave_id)
            raza = ave.raza
            ave.delete()
            messages.success(request, f'Registro de aves "{raza}" eliminado.')
        except Ave.DoesNotExist:
            messages.error(request, 'Registro de aves no encontrado.')
    return redirect('aves')


# ── Alimentos ─────────────────────────────────────────────────
@login_required
def alimentos_view(request):
    alimentos = Alimento.objects.all().order_by('nombre')
    return render(request, 'private/alimentos.html', {'alimentos': alimentos})


@login_required
def alimento_crear(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        if nombre:
            Alimento.objects.create(
                nombre=nombre,
                tipo=request.POST.get('tipo', 'otro'),
                unidad_medida=request.POST.get('unidad_medida', 'kg'),
                stock=request.POST.get('stock') or 0,
                descripcion=request.POST.get('descripcion', ''),
            )
            messages.success(request, f'Alimento "{nombre}" creado correctamente.')
        else:
            messages.error(request, 'El nombre es obligatorio.')
    return redirect('alimentos')


@login_required
def alimento_editar(request, alimento_id):
    try:
        alimento = Alimento.objects.get(pk=alimento_id)
    except Alimento.DoesNotExist:
        messages.error(request, 'Alimento no encontrado.')
        return redirect('alimentos')

    if request.method == 'POST':
        alimento.nombre = request.POST.get('nombre', '').strip()
        alimento.tipo = request.POST.get('tipo', 'otro')
        alimento.unidad_medida = request.POST.get('unidad_medida', 'kg')
        alimento.stock = request.POST.get('stock') or 0
        alimento.descripcion = request.POST.get('descripcion', '')
        alimento.save()
        messages.success(request, f'Alimento "{alimento.nombre}" actualizado.')
    return redirect('alimentos')


@login_required
def alimento_eliminar(request, alimento_id):
    if request.method == 'POST':
        try:
            alimento = Alimento.objects.get(pk=alimento_id)
            nombre = alimento.nombre
            alimento.delete()
            messages.success(request, f'Alimento "{nombre}" eliminado.')
        except Alimento.DoesNotExist:
            messages.error(request, 'Alimento no encontrado.')
    return redirect('alimentos')


# ── Alimentación (registro de porciones) ───────────────────────
@login_required
def alimentacion_view(request):
    registros = Alimentacion.objects.select_related('alimento', 'galpon', 'usuario').order_by('-fecha')
    alimentos = Alimento.objects.all().order_by('nombre')
    galpones = Galpon.objects.all().order_by('nombre')
    usuarios = User.objects.filter(is_active=True).order_by('first_name')
    return render(request, 'private/alimentacion.html', {
        'registros': registros,
        'alimentos': alimentos,
        'galpones': galpones,
        'usuarios': usuarios,
    })


@login_required
def alimentacion_crear(request):
    if request.method == 'POST':
        try:
            Alimentacion.objects.create(
                fecha=request.POST.get('fecha'),
                porcion=request.POST.get('porcion') or 0,
                observacion=request.POST.get('observacion', ''),
                alimento_id=request.POST.get('alimento') or None,
                galpon_id=request.POST.get('galpon') or None,
                usuario_id=request.POST.get('usuario') or request.user.pk,
            )
            messages.success(request, 'Registro de alimentación creado correctamente.')
        except Exception as e:
            messages.error(request, f'Error al crear el registro: {e}')
    return redirect('alimentacion')


@login_required
def alimentacion_editar(request, registro_id):
    try:
        registro = Alimentacion.objects.get(pk=registro_id)
    except Alimentacion.DoesNotExist:
        messages.error(request, 'Registro no encontrado.')
        return redirect('alimentacion')

    if request.method == 'POST':
        registro.fecha = request.POST.get('fecha')
        registro.porcion = request.POST.get('porcion') or 0
        registro.observacion = request.POST.get('observacion', '')
        registro.alimento_id = request.POST.get('alimento') or None
        registro.galpon_id = request.POST.get('galpon') or None
        registro.usuario_id = request.POST.get('usuario') or request.user.pk
        registro.save()
        messages.success(request, 'Registro de alimentación actualizado.')
    return redirect('alimentacion')


@login_required
def alimentacion_eliminar(request, registro_id):
    if request.method == 'POST':
        try:
            Alimentacion.objects.get(pk=registro_id).delete()
            messages.success(request, 'Registro de alimentación eliminado.')
        except Alimentacion.DoesNotExist:
            messages.error(request, 'Registro no encontrado.')
    return redirect('alimentacion')