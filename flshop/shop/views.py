# shop/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, OrderCreateForm
from .models import Product, Order

def home(request):
    """
    Главная страница, отображающая home.html.
    """
    return render(request, 'shop/home.html')

def register(request):
    """
    Страница регистрации. После успешной регистрации перенаправляем на страницу входа.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    # Обратите внимание: здесь шаблон registration/register.html,
    # его можно разместить либо в shop/templates/registration/, либо объединить с шаблонами приложения.
    return render(request, 'registration/register.html', {'form': form})

def product_list(request):
    """
    Страница отображения каталога цветов.
    """
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, pk):
    """
    Страница деталей товара.
    """
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

def cart_detail(request):
    """
    Страница корзины пользователя.
    """
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    return render(request, 'shop/cart_detail.html', {'cart': cart, 'products': products})

@require_POST
def cart_add(request, product_id):
    """
    Добавление товара в корзину.
    """
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart_detail')

def cart_remove(request, product_id):
    """
    Удаление товара из корзины.
    """
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect('cart_detail')

@login_required
def order_create(request):
    """
    Страница оформления заказа.
    После создания заказа вызывается функция отправки уведомления в Telegram.
    """
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('product_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            # Добавляем товары в заказ.
            for product_id, quantity in cart.items():
                product = Product.objects.get(pk=product_id)
                # Если нужно учитывать количество, можно создать промежуточную модель OrderItem.
                order.products.add(product)
            order.save()
            # Очищаем корзину.
            request.session['cart'] = {}

            # Отправляем уведомление в Telegram.
            from bot.telegram_bot import notify_new_order
            notify_new_order(order)

            return render(request, 'shop/order_created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'shop/order_create.html', {'form': form})
