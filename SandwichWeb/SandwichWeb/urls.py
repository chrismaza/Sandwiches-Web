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
    path('admin/', admin.site.urls),
    path('', Index.as_view(),name = 'index'),
    path('administration/', Index_Admin.as_view(),name = 'administration'),
    path('order/', makeOrder,name = 'order'),
    path('administration/order_list/', listOrder.as_view(),name = 'order_list'),
    path('administration/order_list_date/', listOrderDate.as_view(),name = 'order_list_date'),
    path('makeOrder/', makeOrder ,name = 'makeOrder'),
    path('reset/', resetOrder ,name = 'resetOrder'),
    path('confirm/', confirmOrder ,name = 'confirmOrder'),
]
