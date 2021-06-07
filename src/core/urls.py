"""core URL Configuration

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
from django.contrib import admin
from django.urls import path
from .views import memory, disk, memory_percentage, network, cpu, cpu_percentage, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('memory/', memory, name='memory'),
    path('memory_percentage/', memory_percentage, name='memory_percentage'),
    path('disk/', disk, name='disk'),
    path('network/', network, name='network'),
    path('cpu/', cpu, name='cpu'),
    path('cpu_percentage/', cpu_percentage, name='cpu_percentage'),
    path('', index, name='index'),
]
