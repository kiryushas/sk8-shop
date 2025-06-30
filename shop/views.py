from django.shortcuts import render, get_object_or_404, redirect
from .models import Product

# Главная страница — список товаров
def product_list(request):
    category = request.GET.get('category')
    products = Product.objects.all()
    if category:
        products = products.filter(category=category)
    return render(request, 'shop/product_list.html', {'products': products})

# Добавление товара в корзину
def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])

    # Проверка: если товар уже есть, увеличиваем количество
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] += 1
            break
    else:
        cart.append({'product_id': product_id, 'quantity': 1})

    request.session['cart'] = cart
    return redirect('product_list')

# Отображение корзины
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
