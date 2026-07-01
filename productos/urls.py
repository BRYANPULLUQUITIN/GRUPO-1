from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# ══ Gestión de Productos (Requieren Login) ═════════════════════

@login_required
def listar_productos(request):
    """
    Vista para listar todos los productos en el sistema.
    """
    # Por ahora renderiza la plantilla estática, en el futuro traerá los objetos desde la BD.
    return render(request, 'productos/listar_productos.html')


@login_required
def crear_producto(request):
    """
    Vista para el formulario de creación de un nuevo producto.
    """
    if request.method == 'POST':
        # Aquí procesarás el formulario cuando lo implementemos en el HTML
        messages.success(request, "¡Producto creado con éxito (Simulado)!")
        return redirect('listar_productos')
        
    return render(request, 'productos/crear_producto.html')