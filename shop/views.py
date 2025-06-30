from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem
from .forms import OrderForm

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
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] += 1
            break
    else:
        cart.append({'product_id': product_id, 'quantity': 1})
    request.session['cart'] = cart
    return redirect('product_list')

# Удаление товара из корзины
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])
    cart = [item for item in cart if item['product_id'] != product_id]
    request.session['cart'] = cart
    return redirect('cart')

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

# Регистрация
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})

# Оформление заказа (checkout)
@login_required
def checkout_view(request):
    cart = request.session.get('cart', [])
    if not cart:
        return redirect('cart')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            for item in cart:
                product = get_object_or_404(Product, id=item['product_id'])
                OrderItem.objects.create(order=order, product=product, quantity=item['quantity'])

            request.session['cart'] = []
            return render(request, 'shop/checkout_success.html', {'order': order})
    else:
        form = OrderForm()

    return render(request, 'shop/checkout.html', {'form': form})
