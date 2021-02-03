from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Ingredients, Size, Order,Sandwich

from datetime import datetime

##################################### Lista de Sandwiches de la Orden ##################################

lista_sand = []
lista_view_sand = []

############################################ Clases #####################################################
class Index (View):
    def get(self, request, *args, **kwargs):
        return render(request,'client/index.html')

############################################## Funciones ################################################

######################################## Realizar una Orden###############################################

def makeOrder(request, *args, **kwargs):

    global data_size
    global data_ing
    global data_id_sizes
    global data_id_ing

    ingredients = Ingredients.objects.order_by('name') # Obtenemos los Ingredientes de la BD
    sizes = Size.objects.order_by('name')              # Obtenemos los tamaños de la BD

    context = {
        'ingredients' : ingredients,                   # Pasamos los Ingredientes y Tamaños 
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

        client_name= str(request.POST.get("client_name")).capitalize() # Obtenemos el nombre del cliente desde la vista
        items_sizes = request.POST.getlist('items_sizes[]')            # Obtenemos el tamaño seleccionado desde la vista
        items_ing = request.POST.getlist('items_ing[]')                # Obtenemos los ingredientes seleccionados desde la vista

        for size in items_sizes:
            size_item = Size.objects.get(pk__contains=int(size))       # Obtenemos el objeto Tamaño de la BD
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
            ing_item = Ingredients.objects.get(pk__contains=int(item)) # Obtenemos el objeto Ingrediente de la BD
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

        for item in sandwich['sizes']:                     # Calculamos el Subtotal del Sandwich
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
            'client_name': client_name,
            'sizes': sandwich['sizes'],
            'ingredients': sandwich['ingredients'],
            'price': price,
        }

        lista_view_sand.append(context)

        return render(request,'client/order_confirmation.html',context)

    return render(request,'client/order.html',context)

##############################################################################################################

####################################### Volver a Empezar la Orden ############################################

def resetOrder (request):
    lista_sand.clear()          # Limpiamos la lista que tenia los sandwiches que se habian ordenado
    lista_view_sand.clear()
    return render(request,'client/index.html')

#############################################################################################################

####################################### Confirmar la Orden #################################################

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

        p = Order.objects.create(client_name = name,total = total_order) # Creamos una orden en la BD

        for items in lista_sand:
            for m in items['sizes']:
                size = Size.objects.get(id_size=m['id'])
            sandwich = Sandwich.objects.create(order = p, size = size,total = items['price']) # Creamos un sandwich en la BD
            for b in items['ingredients']:
                ingredient = Ingredients.objects.get(id_ingredients=b['id'])
                sandwich.ingredients.add(ingredient)                            # Le agregamos al sandwich los ingredientes

        lista_sand.clear()      # Limpiamos las listas
        lista_view_sand.clear()

        return render(request,'client/index.html')

    return render(request,'client/order_view.html',context)

###############################################################################################################

####################################### Obtener todas las Ordenes ############################################

def getOrders (request):
    orders = Order.objects.order_by('created_on') # Obtenemos las Ordenes por orden de fecha
    list_ord = []
    for m in orders:
        numero_sand = 0
        sand = Sandwich.objects.filter(order=m)   # Filtramos los sandwiches de la orden en especifico
        for x in sand:
            numero_sand += 1                     # Calculamos el nro de sandwiches que tiene la orden

        general = {
            'fecha': m.created_on,
            'sand': numero_sand,
            'price': m.total,
            'client': m.client_name  
        }
        list_ord.append(general)

    context = {
        'list_ord_total' : list_ord
    }

    return render(request,'client/admin.html',context)

##############################################################################################################

############################## Obtener Ordenes por Fecha ####################################################

def getByDate (request):

    context = {}

    if request.method == "POST":
        date= request.POST.get("date")                      # Obtenemos la fecha por la cual se desea buscar
        date_format = datetime.strptime(date, '%Y-%m-%d')
        orders = Order.objects.filter(created_on=date_format) # Obtenemos las ordenes de esa fecha en especifico
        list_ord = []
        for m in orders:
            numero_sand = 0
            sand = Sandwich.objects.filter(order=m)
            for x in sand:
                numero_sand += 1

            general = {
                'fecha': m.created_on,
                'sand': numero_sand,
                'price': m.total,
                'client': m.client_name  
            }
            list_ord.append(general)

        context = {
            'list_ord_total' : list_ord
        }

    return render(request,'client/order_list_date.html',context)
##############################################################################################################

############################## Obtener Ordenes por Tamaño ####################################################

def getBySize (request):

    list_ord = []
    context = {}
    sizes_list = Size.objects.order_by('name')

    if request.method == "POST":
        size_name = request.POST.get("size")
        size = Size.objects.get(name=size_name) 
        orders = Order.objects.order_by('created_on')

        for m in orders:
            sand = Sandwich.objects.filter(order=m,size=size) # Obtenemos los sandwiches de ese tamaño en especifico
            for x in sand:

                general = {
                    'fecha': m.created_on,
                    'size': x.size,
                    'total_sand': x.total,
                    'client': m.client_name, 
                    'id_order': m.id_order, 
                    'total_order': m.total,
                }

                list_ord.append(general)

    context = {
        'list_ord_total' : list_ord,
        'sizes':sizes_list
    }

    return render(request,'client/order_list_size.html',context)
##############################################################################################################

############################## Obtener Ordenes por Cliente ####################################################

def getByClient (request):

    context = {}

    if request.method == "POST":
        client = str(request.POST.get("client")).capitalize()
        orders = Order.objects.filter(client_name=client)  # Obtenemos las ordenes de ese cliente en especifico
        list_ord = []
        for m in orders:
            numero_sand = 0
            sand = Sandwich.objects.filter(order=m)
            for x in sand:
                numero_sand += 1

            general = {
                'fecha': m.created_on,
                'sand': numero_sand,
                'price': m.total,
                'client': m.client_name  
            }
            list_ord.append(general)

        context = {
            'list_ord_total' : list_ord
        }

    return render(request,'client/order_list_client.html',context)
##############################################################################################################

############################## Obtener Ordenes por Ingrediente ####################################################

def getByIngredient (request):

    context = {}
    list_ord = []
    list_ing = Ingredients.objects.order_by('name')

    if request.method == "POST":
        ingredient = request.POST.get("ingredient")
        ing = Ingredients.objects.get(name=ingredient)
        orders = Order.objects.order_by('created_on')
        
        for m in orders:
            sand = Sandwich.objects.filter(order=m,ingredients=ing) # Obtenemos los sandwiches de esa orden y ingrediente en especifico
            for x in sand:
                general = {
                    'fecha': m.created_on,
                    'ing': ing,
                    'total_sand': x.total,
                    'client': m.client_name, 
                    'id_order': m.id_order, 
                    'total_order': m.total,
                }
                list_ord.append(general)

    context = {
        'ingredient': list_ing,
        'list_ord_total' : list_ord
    }

    return render(request,'client/order_list_ing.html',context)
