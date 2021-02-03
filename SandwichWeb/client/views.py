from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Ingredients, Size, Order,Sandwich

from datetime import datetime

##### Lista de Sandwiches de la Orden ###################

lista_sand = []
lista_view_sand = []

############################################ Clases #####################################################
class Index (View):
    def get(self, request, *args, **kwargs):
        return render(request,'client/index.html')

############################################## Funciones ################################################

def makeOrder(request, *args, **kwargs):

    global data_size
    global data_ing
    global data_id_sizes
    global data_id_ing

    ingredients = Ingredients.objects.order_by('name')
    sizes = Size.objects.order_by('name')

    context = {
        'ingredients' : ingredients,
        'sizes' : sizes,
    }

    if request.method == "POST":
        sandwich = {
        'sizes':[],
        'ingredients':[]
        }

        items_id = {
            'id_sizes':[],
            'id_ingredients':[]
        }

        client_name= request.POST.get("client_name")
        items_sizes = request.POST.getlist('items_sizes[]')
        items_ing = request.POST.getlist('items_ing[]')

        for size in items_sizes:
            size_item = Size.objects.get(pk__contains=int(size))
            data_size = {
                'name':size_item.name,
                'price':size_item.price
            }

            data_id_sizes = {
                'id':size_item.pk,
            }

        sandwich['sizes'].append(data_size)
        items_id['id_sizes'].append(data_id_sizes)

        for item in items_ing:
            ing_item = Ingredients.objects.get(pk__contains=int(item))
            data_ing = {
                'name': ing_item.name,
                'price': ing_item.price
            }

            data_id_ing = {
                'id': ing_item.pk,
            }

            sandwich['ingredients'].append(data_ing)
            items_id['id_ingredients'].append(data_id_ing)
        
        price = 0

        for item in sandwich['sizes']:
            price += float(item['price'])

        for item in sandwich['ingredients']:
            price += float(item['price'])
        
        sandwich_items = {
            'client_name': client_name,
            'sizes': items_id['id_sizes'],
            'ingredients': items_id['id_ingredients'],
            'price': price
        }

        lista_sand.append(sandwich_items)

        context = {
            'sizes': sandwich['sizes'],
            'ingredients': sandwich['ingredients'],
            'price': price,
        }

        lista_view_sand.append(context)

        return render(request,'client/order_confirmation.html',context)

    return render(request,'client/order.html',context)

##############################################################################################################

def resetOrder (request):
    lista_sand.clear()
    lista_view_sand.clear()
    return render(request,'client/index.html')

#############################################################################################################

def confirmOrder (request):

    total_order = 0

    for items in lista_sand:
        name = items['client_name']
        total_order += float(items['price'])
    
    context = {
        'sandwich': lista_view_sand,
        'total': total_order
    }

    if request.method == "POST":

        p = Order.objects.create(client_name = name,total = total_order)

        for items in lista_sand:
            for m in items['sizes']:
                size = Size.objects.get(id_size=m['id'])
            sandwich = Sandwich.objects.create(order = p, size = size,total = items['price'])
            for b in items['ingredients']:
                ingredient = Ingredients.objects.get(id_ingredients=b['id'])
                sandwich.ingredients.add(ingredient)

        lista_sand.clear()
        lista_view_sand.clear()

        return render(request,'client/index.html')

    return render(request,'client/order_view.html',context)

def getOrders (request):
    orders = Order.objects.order_by('created_on')
    lista_sandw = []
    list_ord = []
    for m in orders:
        numero_sand = 0
        sand = Sandwich.objects.filter(order=m)
        for x in sand:
            numero_sand += 1
            # for n in x['ingredients']:
            #     print(n)
            # size = x['size']
            # sand = {
            #     'ing': ing,
            #     'size': size
            # }
            # lista_sandw.append(sand)

        general = {
            'fecha': m.created_on,
            'sand': numero_sand,
            'price': m.total,
            'client': m.client_name  
        }
        list_ord.append(general)
        for x in list_ord:
            print(x)

    context = {
        'list_ord_total' : list_ord
    }

    return render(request,'client/admin.html',context)

def getByDate (request):

    context = {}

    if request.method == "POST":
        date= request.POST.get("date")
        date_format = datetime.strptime(date, '%Y-%m-%d')
        orders = Order.objects.filter(created_on=date_format)
        lista_sandw = []
        list_ord = []
        for m in orders:
            numero_sand = 0
            sand = Sandwich.objects.filter(order=m)
            for x in sand:
                numero_sand += 1
                # for n in x['ingredients']:
                #     print(n)
                # size = x['size']
                # sand = {
                #     'ing': ing,
                #     'size': size
                # }
                # lista_sandw.append(sand)

            general = {
                'fecha': m.created_on,
                'sand': numero_sand,
                'price': m.total,
                'client': m.client_name  
            }
            list_ord.append(general)
            for x in list_ord:
                print(x)

        context = {
            'list_ord_total' : list_ord
        }

    return render(request,'client/order_list_date.html',context)

