from django.shortcuts import redirect, render

# Create your views here.
def listar_productos(request):
    return render(request, 'productos/listar_productos.html')

def crear_producto(request):
    if request.method == 'POST':
        nombre_producto = request.POST.get('')
        precio = request.POST.get('')
        precio_producto = request.POST.get('')
        stock = request.POST.get('')
        estado_producto = request.POST.get('')

        Producto.objects.create(
            nombre_producto=nombre_producto,
            precio=precio,
            precio_producto=precio_producto,
            stock=stock,
            estado_producto=estado_producto
        )
        return redirect('listar_productos')
