from django.urls import path
from . import views
from .urls_auth import urlpatterns as auth_urls

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('cart/', views.cart_view, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),  
    path('order-confirmation/', views.order_confirmation_view, name='order_confirmation'),

]

urlpatterns += auth_urls