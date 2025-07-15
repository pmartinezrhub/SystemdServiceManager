"""SystemdServiceManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
# ✅ este es el archivo SystemdServiceManager/SystemdServiceManager/urls.py
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),     
    path('home/', views.home, name='home2'),  
    path('start/', views.start_service, name='start_service'),
    path('stop/', views.stop_service, name='stop_service'),
    path('restart/', views.restart_service, name='restart_service'),
    path('enable/', views.enable_service, name='enable_service'),
    path('disable/', views.enable_service, name='disable_service'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
