from django.contrib import admin
from .models import Size, Ingredients, Sandwich, Order

admin.site.register(Size)
admin.site.register(Ingredients)
admin.site.register(Sandwich)
admin.site.register(Order)
