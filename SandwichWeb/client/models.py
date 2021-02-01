from django.db import models

class Size (models.Model):
    id_size = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5,decimal_places=2)

    def __str__(self):
        return self.name

class Ingredients (models.Model):
    id_ingredients = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5,decimal_places=2)

    def __str__(self):
        return self.name

class Order (models.Model):
    id_order = models.AutoField(primary_key=True)
    created_on = models.DateTimeField(auto_now_add=True)
    client_name = models.CharField(max_length=100)
    total = models.FloatField()

    def __str__(self):
        return f'Orden: {self.created_on.strftime("%a, %d %b %y %H:%M:%S")}'

class Sandwich (models.Model):
    id_sandwich = models.AutoField(primary_key=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,blank=True)
    ingredients = models.ManyToManyField(Ingredients,blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=5,decimal_places=2)

    def __str__(self):
        return f'Sandwich {self.id_sandwich}'

