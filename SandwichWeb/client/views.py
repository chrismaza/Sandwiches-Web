from django.shortcuts import render
from django.views import View
from .models import Ingredients, Size, Order,Sandwich

class Index (View):
    def get(self, request, *args, **kwargs):
        return render(request,'client/index.html')

class Index_Admin (View):
    def get(self, request, *args, **kwargs):
        return render(request,'client/admin.html')

class makeOrder (View):
    def get(self, request, *args, **kwargs):
        ingredients = Ingredients.objects.order_by('name')
        sizes = Size.objects.order_by('name')

        context = {
            'ingredients' : ingredients,
            'sizes' : sizes,
        }
        return render(request,'client/order.html',context)
    
    def post(self, request, *args, **kwargs):
        order_items = {
            'items':[]
        }

        items_sizes = request.POST.getlist('items_sizes[]')
        items_ing = request.POST.getlist('items_ing[]')

        for size in items_sizes:
            size_item = Size.objects.get(pk__contains=int(size))
            data_size = {
                'id':size_item.pk,
                'name':size_item.name,
                'price':size_item.price
            }

        order_items['items'].append(data_size)

        for item in items_ing:
            ing_item = Ingredients.objects.get(pk__contains=int(item))
            data_ing = {
                'id': ing_item.pk,
                'name': ing_item.name,
                'price': ing_item.price
            }

            order_items['items'].append(data_ing)
            price = 0
            items_id = []

        for item in order_items['items']:
            price += float(item['price'])
            items_id.append(item['id'])
        
        context = {
            'items': order_items['items'],
            'price': price
        }

        return render(request,'client/order_confirmation.html',context)
            