from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

# ══ Vistas del Catálogo de Productos ═══════════════════════════

def productos_list(request):
    """
    Vista para mostrar todos los productos disponibles.
    """
    # Por ahora renderiza una plantilla estática, luego traeremos los datos de la Base de Datos.
    return render(request, 'productos/productos_list.html')


def producto_detail(request, pk):
    """
    Vista para ver el detalle en profundidad de un único producto.
    """
    context = {
        'producto_id': pk
    }
    return render(request, 'productos/producto_detail.html', context)