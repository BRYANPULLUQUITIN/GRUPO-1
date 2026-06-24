from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.profile_view, name='profile'),          
    path('perfil/actualizar/', views.profile_update, name='profile_update'),
    path('configuracion/', views.settings_view, name='settings'),
    # ── Usuarios ──────────────────────────────────────────────
    path('usuarios/', views.usuarios_view, name='usuarios'),
    path('usuarios/crear/', views.usuario_crear, name='usuario_crear'),
    path('usuarios/<int:user_id>/eliminar/', views.usuario_eliminar, name='usuario_eliminar'),
    path('usuarios/<int:user_id>/toggle/', views.usuario_toggle, name='usuario_toggle'),
    path('calendario/', views.calendario, name='calendario'),
    path('usuarios/<int:user_id>/editar/', views.usuario_editar, name='usuario_editar'),

    path('calendario/', views.calendario_view, name='calendario'),
    path('calendario/crear/', views.evento_crear, name='evento_crear'),
    path('calendario/<int:evento_id>/eliminar/', views.evento_eliminar, name='evento_eliminar'),
    path('calendario/json/', views.eventos_json, name='eventos_json'),
]