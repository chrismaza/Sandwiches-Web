from django.shortcuts import render
from django.views import View

class Index (View):
    def get(self, request, *args, **kwargs):
        return render(request,'client/index.html')

class Index_Admin (View):
    def get(self, request, *args, **kwargs):
        return render(request,'client/admin.html')

class Order (View):
    def get(self, request, *args, **kwargs):
        pass
