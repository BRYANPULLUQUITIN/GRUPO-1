from django.urls import path
from . import views


# Create your urls here.

urlpatterns = [
    path('', views.listar_productos, name='listar_productos'),
    path('crear_producto/', views.crear_producto, name='crear_producto'),
]