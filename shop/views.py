from django.shortcuts import render, get_object_or_404
from .models import Product

def cart_view(request):
    cart = request.session.get('cart', [])
    cart_items = []
    total = 0

    for item in cart:
        product = get_object_or_404(Product, id=item['product_id'])
        quantity = item['quantity']
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': round(subtotal, 2)
        })

    return render(request, 'shop/cart.html', {
        'cart': cart_items,
        'total': round(total, 2)
    })
