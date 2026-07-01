from django.urls import path
from . import views

urlpatterns = [
    # ── Páginas Públicas Estáticas ─────────────────────────────────
    path('', views.inicio, name='index'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('menu/', views.menu, name='menu'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),

    # ── Autenticación y Cuentas ────────────────────────────────────
    path('login/', views.login_view, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('logout/', views.logout_view, name='logout'),
    
    # ── Vistas Protegidas intermedias ──────────────────────────────
    path('splash/', views.splash_view, name='splash'),
]