"""dp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import include, path
from charts import views
from django.shortcuts import redirect


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")), #accounts/
    path('proflvls/', views.proflvls, name='proflvls'),#, name='charts') #include('charts.urls'))
    path('directions/', views.directions),#, name='charts') #include('charts.urls'))
    path('foreigns/', views.foreigns),#, name='charts') #include('charts.urls'))
    path('forms/', views.forms),#, name='charts') #include('charts.urls'))
    path('registrations/', views.registrations),#, name='charts') #include('charts.urls'))
    path('basics/', views.basics),#, name='charts') #include('charts.urls'))
    path('', lambda request: redirect('accounts/login', permanent=True)),
]