from django.contrib import admin
from .models import RegularPizza,SicillianPizza,Topping,Sub,Pasta,Salad,DinnerPlatter,Extra,cart
# Register your models here.

admin.site.register(RegularPizza)
admin.site.register(SicillianPizza)
admin.site.register(Topping)
admin.site.register(Sub)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(DinnerPlatter)
admin.site.register(Extra)
admin.site.register(cart)