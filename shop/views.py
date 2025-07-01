from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Product, Order, OrderItem
from .forms import OrderForm

# Отображение списка товаров
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

# Просмотр корзины
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

# Оформление заказа
def checkout_view(request):
    cart = request.session.get('cart', [])
    if not cart:
        return redirect('cart')

    # Вычисляем сумму заказа
    total = 0
    for item in cart:
        product = get_object_or_404(Product, id=item['product_id'])
        quantity = item['quantity']
        total += product.price * quantity

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            # Дополнительные данные оплаты
            order.payment_method = request.POST.get('payment_method')
            if order.payment_method == 'card':
                order.card_number = request.POST.get('card_number')
                order.expiry_date = request.POST.get('expiry_date')
                order.cvv = request.POST.get('cvv')
            elif order.payment_method == 'crypto':
                order.crypto_network = request.POST.get('crypto_network')
                order.wallet_address = request.POST.get('wallet_address')

            # Привязка пользователя
            if request.user.is_authenticated:
                order.user = request.user

            order.save()

            # Создание OrderItem
            for item in cart:
                product = get_object_or_404(Product, id=item['product_id'])
                OrderItem.objects.create(order=order, product=product, quantity=item['quantity'])

            # Очистка корзины
            request.session['cart'] = []

            return redirect('order_confirmation')  # Переход на страницу "ожидание оплаты"
    else:
        form = OrderForm()

    return render(request, 'shop/checkout.html', {
        'form': form,
        'total': round(total, 2)
    })

# Подтверждение заказа
def order_confirmation_view(request):
    return render(request, 'shop/order_confirmation.html')
