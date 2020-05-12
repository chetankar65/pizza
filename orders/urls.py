from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name='login_view'),
    path("logout", views.logout_view, name='logout_view'),
    path("register", views.register, name='register'),
    path("registerpage", views.register_page, name='register_page'),
    path("set_cart",views.set_cart,name='set_cart'),
    path("cart",views.get_all_items,name='get_all_items'),
    path('finish',views.finish,name="finish"),
    path("delete",views.delete,name='delete'),
    path('orders',views.all_orders,name="all_orders"),
    path('<int:order_id>',views.order_details,name="order_details"),
    path('<int:order>/completeOrder',views.completeOrder,name="completeOrder")
]
