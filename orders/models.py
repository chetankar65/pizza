from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_comma_separated_integer_list

# Create your models here.

size = (
    ('1','Small'),
    ('2','Large'),
)

class RegularPizza(models.Model):
    name = models.CharField(max_length=64)
    size = models.CharField( max_length = 20,choices = size,default = '1') 
    price = models.DecimalField(decimal_places=2,max_digits=5)
    toppings = models.IntegerField()

    def __str__(self):
        return f"{self.name},{self.size},{self.price},{self.toppings}"

class SicillianPizza(models.Model):
    name = models.CharField(max_length=64)
    size = models.CharField( max_length = 20,choices = size,default = '1') 
    price = models.DecimalField(decimal_places=2,max_digits=5)
    toppings = models.IntegerField()

    def __str__(self):
        return f"{self.name},{self.size},{self.price},{self.toppings}"

class Topping(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'Topping : {self.name}'


class Sub(models.Model):
    name = models.CharField(max_length = 64)
    small = models.DecimalField(decimal_places=2,max_digits=5)
    large = models.DecimalField(decimal_places=2,max_digits=5)

    def __str__(self):
        return f'SubType:{self.name},{self.small},{self.large}'


class Pasta(models.Model):
    name = models.CharField(max_length = 64)
    price = models.DecimalField(decimal_places=2,max_digits=5)

    def __str__(self):
        return f'Name:{self.name},price:{self.price}'


class Salad(models.Model):
    name = models.CharField(max_length = 64)
    price = models.DecimalField(decimal_places=2,max_digits=5)

    def __str__(self):
        return f'Name:{self.name},price:{self.price}'

class DinnerPlatter(models.Model):
    name = models.CharField(max_length = 64)
    small = models.DecimalField(decimal_places=2,max_digits=5)
    large = models.DecimalField(decimal_places=2,max_digits=5)

    def __str__(self):
        return f'SubType:{self.name},{self.small},{self.large}'


class Extra(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(decimal_places=2,max_digits=5)

    def __str__(self):
        return f'{self.name},{self.price}'

items = (('1','RP'),('2','SP'),('3','S'),('4','Pa'),('5','Sa'),('6','DP'))
sizes = (('0',0),('1',1),('2',2))
orders = (('1','Pending'),('2','Complete'))
class cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length = 20,choices = items,default = '1') 
    quantity = models.IntegerField()
    product_id = models.IntegerField()
    extras = models.CharField(max_length = 20,validators=[validate_comma_separated_integer_list],default='')
    size = models.IntegerField(choices = sizes,default='1')
    status = models.CharField(max_length = 20,choices=orders,default='1')

    def __str__(self):
        return f'{self.user_id},{self.product_name},{self.quantity},{self.product_id},{self.extras},{self.status}'

