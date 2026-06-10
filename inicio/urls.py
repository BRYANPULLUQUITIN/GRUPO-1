from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('menu/', views.menu, name='menu'),
    path('about/', views.about, name='about'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
]   