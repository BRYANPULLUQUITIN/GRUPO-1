from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.profile_view, name='profile'),
    path('perfil/actualizar/', views.profile_update, name='profile_update'),
    path('configuracion/', views.settings_view, name='settings'),
    # Usuarios
    path('usuarios/', views.usuarios_view, name='usuarios'),
    path('usuarios/crear/', views.usuario_crear, name='usuario_crear'),
    path('usuarios/<int:user_id>/editar/', views.usuario_editar, name='usuario_editar'),   # ← agregar esta línea
    path('usuarios/<int:user_id>/eliminar/', views.usuario_eliminar, name='usuario_eliminar'),
    path('usuarios/<int:user_id>/toggle/', views.usuario_toggle, name='usuario_toggle'),
    # Calendario
    path('calendario/', views.calendario_view, name='calendario'),
    path('calendario/crear/', views.evento_crear, name='evento_crear'),
    path('calendario/<int:evento_id>/eliminar/', views.evento_eliminar, name='evento_eliminar'),
    path('calendario/json/', views.eventos_json, name='eventos_json'),
    # Pedidos
    path('pedidos/', views.pedidos_view, name='pedidos'),
    path('pedidos/crear/', views.pedido_crear, name='pedido_crear'),
    path('pedidos/<int:pedido_id>/editar/', views.pedido_editar, name='pedido_editar'),
    path('pedidos/<int:pedido_id>/eliminar/', views.pedido_eliminar, name='pedido_eliminar'),
    # Clientes
    path('clientes/crear/', views.cliente_crear, name='cliente_crear'),
    path('clientes/json/', views.clientes_json, name='clientes_json'),
]