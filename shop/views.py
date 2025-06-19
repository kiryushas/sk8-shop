from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

def product_list(request):
    products = Product.objects.all()
    cart = request.session.get('cart', [])
    return render(request, 'shop/product_list.html', {
        'products': products,
        'cart': cart
    })

def add_to_cart(request, product_id):
    print("🛒 ДОБАВЛЯЕМ В КОРЗИНУ:", product_id)  # <- покажет ID товара

    cart = request.session.get('cart', [])
    if product_id not in cart:
        cart.append(product_id)
        request.session['cart'] = cart

    print("🧺 ТЕКУЩАЯ КОРЗИНА:", cart)  # <- покажет содержимое корзины
    return redirect('product_list')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])
    if product_id in cart:
        cart.remove(product_id)
    request.session['cart'] = cart
    return redirect('product_list')

def cart_view(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)
    return render(request, 'shop/cart.html', {
        'cart': products
    })