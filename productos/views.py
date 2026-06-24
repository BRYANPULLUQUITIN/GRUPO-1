from django.shortcuts import redirect, render
from .models import Producto

# Create your views here.
def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/listar_productos.html', {'productos': productos})

def crear_producto(request):
    if request.method == 'POST':
        nombre_producto = request.POST.get('nombre_producto')
        precio = request.POST.get('precio')
        precio_producto = request.POST.get('precio_producto')
        stock = request.POST.get('stock')
        estado_producto = request.POST.get('estado_producto')

        Producto.objects.create(
            nombre_producto=nombre_producto,
            precio=precio,
            precio_producto=precio_producto,
            stock=stock,
            estado_producto=estado_producto
        )
        return redirect('listar_productos')
