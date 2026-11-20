"""
URL configuration for django_cheems_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hello_api import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('user', views.save_user),
    path('animal', views.save_animal),

    # Videojuegos (CRUD)
    path('videojuego/', views.videojuego),
    path('save_videojuego/', views.save_videojuego),
    path('get_videojuegos/', views.get_videojuegos),
    path('get_videojuego/<int:id_videojuego>/', views.get_videojuego),
    path('update_videojuego/<int:id_videojuego>/', views.update_videojuego),
    path('delete_videojuego/<int:id_videojuego>/', views.delete_videojuego),
]