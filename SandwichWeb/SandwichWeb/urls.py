"""SandwichWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from client.views import *

urlpatterns = [

    ##################### Admin de Django ##############################
    path('admin/', admin.site.urls),

    ##################### Pagina Principal #############################
    path('', Index.as_view(),name = 'index'),

    ################## Pagina Administrativa ###########################
    path('administration/', getOrders,name = 'administration'),

    ################## Obtener una Orden por Fecha #####################
    path('getByDate/', getByDate,name = 'getByDate'),

    ################### Obtener una Orden por Tamaño ###################
    path('getBySize/', getBySize,name = 'getBySize'),

    ################### Obtener una Orden por Ingrediente ##############
    path('getByIngredient/', getByIngredient,name = 'getByIngredient'),

    #################### Obtener una Orden por Cliente #################
    path('getByClient/', getByClient,name = 'getByClient'),

    ###################### Realizar una Orden ##########################
    path('makeOrder/', makeOrder ,name = 'makeOrder'),

    ###################### Reiniciar una Orden #########################
    path('reset/', resetOrder ,name = 'resetOrder'),

    ###################### Confirmar una Orden #########################
    path('confirm/', confirmOrder ,name = 'confirmOrder'),
    
]
