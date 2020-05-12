from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from .models import RegularPizza,SicillianPizza,Topping,Sub,Pasta,Salad,DinnerPlatter,Extra,cart
from decimal import *
from ast import literal_eval
import numpy as np

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html",{'message':None})
    regulars = RegularPizza.objects.all()
    sicillians = SicillianPizza.objects.all()
    subs = Sub.objects.all()
    pastas = Pasta.objects.all()
    salads = Salad.objects.all()
    toppings = Topping.objects.all()
    platters = DinnerPlatter.objects.all()
    extras = Extra.objects.all()
    cart_items = len(cart.objects.filter(user_id = request.user, status='Pending'))
    context = {'toppings':toppings,'regulars':regulars,'sicillians':sicillians,'subs':subs,'pastas':pastas,'salads':salads,'platters':platters,'extras':extras,'cart_items':cart_items}
    return render(request, 'orders/index.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, 'orders/login.html',{"message":"Invalid Credential!"})

def logout_view(request):
    logout(request)
    return render(request,"orders/login.html" ,{"message":"Logged out!"})

def register_page(request):
    if not request.user.is_authenticated:
        return render(request, "orders/register.html",{'message':None})
    else:
        return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        fname = request.POST["fname"]
        lname = request.POST['lname']
        email = request.POST["email"]

        my_user = User.objects.filter(username = username)
        if (len(my_user) != 0):
            return render(request,"orders/register.html",{'message':'Username already taken!'})
        else:
            user = User.objects.create_user(username,email,password)
            user.first_name = fname
            user.last_name = lname
            user.save()

            return HttpResponseRedirect(reverse("index"))


def set_cart(request):
    if request.method == 'POST':
        quantity = request.POST.get('quantity', True)
        name = request.POST['name']
        pizza_id = request.POST['id']
        arr = []
        toppings = request.POST.getlist('check')
        size = request.POST['size']

        for topping in toppings:
            arr.append(topping)
        user = request.user

        cart_object = cart.objects.create(user_id = user,product_name=name,product_id=int(pizza_id),quantity=int(quantity),extras=arr,size=size,status='Pending')
        cart_object.save()
        
        return HttpResponseRedirect(reverse("index"))


def get_all_items(request):
    user = request.user
    cart_items = cart.objects.filter(user_id = user , status='Pending')
    reg_pizzas = []
    sic_pizzas = []
    subs_arr = []
    pasta_arr = []
    platters_arr = []
    salads_arr = []
    extras = []
    total_price =[]    
    if (len(cart_items) > 0):
        for item in cart_items:
            if item.product_name == 'RP':
                regular_pizza = RegularPizza.objects.get(pk = item.product_id, size = item.size)
                regular_pizza.toppings = item.extras
                regular_pizza.size = item.size
                regular_pizza.order = item.id
                reg_pizzas.append(regular_pizza)
                total_price.append(regular_pizza.price * item.quantity)
            elif item.product_name == 'SP':
                sicillian_pizza = SicillianPizza.objects.get(pk = item.product_id, size = item.size)
                sicillian_pizza.toppings = item.extras
                sicillian_pizza.size = item.size
                sicillian_pizza.order = item.id
                sic_pizzas.append(sicillian_pizza)
                total_price.append(sicillian_pizza.price * item.quantity)
            elif (item.product_name == 'S'):
                subs = Sub.objects.get(pk = item.product_id)
                subs.extras = item.extras
                subs.size = item.size
                subs.order = item.id
                subs_arr.append(subs)
                #########
                res = np.array(literal_eval(item.extras))
                for i in res:
                    extras.append(0.50)
                if (item.size == 1):
                    total_price.append(subs.small * item.quantity)
                else:
                    total_price.append(subs.large * item.quantity)
                ######
            elif (item.product_name == 'Pa'):
                pastas = Pasta.objects.get(pk = item.product_id)
                pastas.order = item.id
                pasta_arr.append(pastas)
                total_price.append(pastas.price * item.quantity)
            elif (item.product_name == 'Sa'):
                salads = Salad.objects.get(pk = item.product_id)
                salads.order = item.id
                salads_arr.append(salads)
                total_price.append(salads.price * item.quantity)
            elif (item.product_name == 'DP'):
                platters = DinnerPlatter.objects.get(pk = item.product_id)
                platters.order = item.id
                platters_arr.append(platters)
                platters.size = item.size
                if (item.size == 1):
                    total_price.append(platters.small * item.quantity)
                else:
                    total_price.append(platters.large * item.quantity)
            else:
                pass


    cart_number = len(cart.objects.filter(user_id = request.user,status='Pending'))
    total = float(sum(total_price)) + float(sum(extras))
    #print(float(sum(extras)))
    context = {
        'regularpizzas':reg_pizzas, 
        'sicillianpizzas':sic_pizzas,
        'subs':subs_arr,
        'pastas':pasta_arr,
        'salads':salads_arr,
        'platters':platters_arr,
        'cost': total,
        'cart_number':cart_number
    }

    return render(request,"orders/cart.html",context)


def finish(request):
    if(request.method == 'POST'):
        user = request.user
        cart.objects.filter(user_id = user , status='Pending').update(status='Complete')
        return render(request,"orders/thanks.html")

def delete(request):
    if(request.method == 'POST'):
        user = request.user
        order = request.POST['order_id'] 
        cart.objects.filter(user_id = user, id=order).delete()
        return HttpResponseRedirect(reverse("get_all_items"))

######
def all_orders(request):
    if request.user.is_superuser:
        cart_items = cart.objects.filter(status='Complete')
        # all orders in a python list
        orders = []
        for item in cart_items:
            orders.append({'id':item.id, 'user':item.user_id})

        context = {
            'orders':orders
        }

        return render(request,"orders/orders.html",context)
    else:
        return HttpResponseRedirect(reverse("index"))


## final touch
def order_details(request, order_id):
    cart_items = cart.objects.filter(id = order_id)
    reg_pizzas = []
    sic_pizzas = []
    subs_arr = []
    pasta_arr = []
    platters_arr = []
    salads_arr = []
    extras = []
    total_price =[]  
    order_id = 0  
    if (len(cart_items) > 0):
        for item in cart_items:
            order_id = item.id
            if item.product_name == 'RP':
                regular_pizza = RegularPizza.objects.get(pk = item.product_id, size = item.size)
                regular_pizza.toppings = item.extras
                regular_pizza.size = item.size
                regular_pizza.order = item.id
                reg_pizzas.append(regular_pizza)
                total_price.append(regular_pizza.price * item.quantity)
            elif item.product_name == 'SP':
                sicillian_pizza = SicillianPizza.objects.get(pk = item.product_id, size = item.size)
                sicillian_pizza.toppings = item.extras
                sicillian_pizza.size = item.size
                sicillian_pizza.order = item.id
                sic_pizzas.append(sicillian_pizza)
                total_price.append(sicillian_pizza.price * item.quantity)
            elif (item.product_name == 'S'):
                subs = Sub.objects.get(pk = item.product_id)
                subs.extras = item.extras
                subs.size = item.size
                subs.order = item.id
                subs_arr.append(subs)
                #########
                res = np.array(literal_eval(item.extras))
                for i in res:
                    extras.append(0.50)
                if (item.size == 1):
                    total_price.append(subs.small * item.quantity)
                else:
                    total_price.append(subs.large * item.quantity)
                ######
            elif (item.product_name == 'Pa'):
                pastas = Pasta.objects.get(pk = item.product_id)
                pastas.order = item.id
                pasta_arr.append(pastas)
                total_price.append(pastas.price * item.quantity)
            elif (item.product_name == 'Sa'):
                salads = Salad.objects.get(pk = item.product_id)
                salads.order = item.id
                salads_arr.append(salads)
                total_price.append(salads.price * item.quantity)
            elif (item.product_name == 'DP'):
                platters = DinnerPlatter.objects.get(pk = item.product_id)
                platters.order = item.id
                platters_arr.append(platters)
                platters.size = item.size
                if (item.size == 1):
                    total_price.append(platters.small * item.quantity)
                else:
                    total_price.append(platters.large * item.quantity)
            else:
                pass
    cart_number = len(cart.objects.filter(user_id = request.user,status='Pending'))
    total = float(sum(total_price)) + float(sum(extras))
    #print(float(sum(extras)))
    context = {
        'order_id':order_id,
        'regularpizzas':reg_pizzas, 
        'sicillianpizzas':sic_pizzas,
        'subs':subs_arr,
        'pastas':pasta_arr,
        'salads':salads_arr,
        'platters':platters_arr,
        'cost': total
    }

    return render(request,"orders/details.html",context)

def completeOrder(request, order):
    if(request.method == 'POST'):
        cart.objects.filter(id = order).delete()
        print('deleted object')
        return HttpResponseRedirect(reverse("all_orders"))