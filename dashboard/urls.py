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
    path('usuarios/<int:user_id>/editar/', views.usuario_editar, name='usuario_editar'),   
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

    # ═══════════════════════════════════════════════════════════════
# AGREGAR ESTE BLOQUE A dashboard/urls.py, dentro de urlpatterns
# (reemplaza el comentario "# Calendario" o ponlo justo antes)
# ═══════════════════════════════════════════════════════════════

    # Galpones
    path('galpones/', views.galpones_view, name='galpones'),
    path('galpones/crear/', views.galpon_crear, name='galpon_crear'),
    path('galpones/<int:galpon_id>/editar/', views.galpon_editar, name='galpon_editar'),
    path('galpones/<int:galpon_id>/eliminar/', views.galpon_eliminar, name='galpon_eliminar'),

    # Aves
    path('aves/', views.aves_view, name='aves'),
    path('aves/crear/', views.ave_crear, name='ave_crear'),
    path('aves/<int:ave_id>/editar/', views.ave_editar, name='ave_editar'),
    path('aves/<int:ave_id>/eliminar/', views.ave_eliminar, name='ave_eliminar'),

    # Alimentos
    path('alimentos/', views.alimentos_view, name='alimentos'),
    path('alimentos/crear/', views.alimento_crear, name='alimento_crear'),
    path('alimentos/<int:alimento_id>/editar/', views.alimento_editar, name='alimento_editar'),
    path('alimentos/<int:alimento_id>/eliminar/', views.alimento_eliminar, name='alimento_eliminar'),

    # Alimentación
    path('alimentacion/', views.alimentacion_view, name='alimentacion'),
    path('alimentacion/crear/', views.alimentacion_crear, name='alimentacion_crear'),
    path('alimentacion/<int:registro_id>/editar/', views.alimentacion_editar, name='alimentacion_editar'),
    path('alimentacion/<int:registro_id>/eliminar/', views.alimentacion_eliminar, name='alimentacion_eliminar'),
]