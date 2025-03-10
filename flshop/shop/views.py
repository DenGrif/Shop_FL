# shop/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, OrderCreateForm
from .models import Product, Order
from bot.telegram_bot import notify_new_order
from asgiref.sync import sync_to_async
import threading
from bot.telegram_bot import notify_new_order
from shop.utils import notify_order_via_http
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def notify_order_in_thread(order):
    threading.Thread(target=notify_order_via_http, args=(order,)).start()


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
    return render(request, 'registration/register.html', {'form': form})


def product_list(request):
    """
    Страница отображения каталога цветов.
    """
    category = request.GET.get('category')
    if category:
        products = Product.objects.filter(category=category)
    else:
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

    if request.method == 'POST':
        # Обновление количества и удаление товаров
        for item_id in list(cart.keys()):
            quantity_field = f'quantity_{item_id}'
            remove_field = f'remove_item_{item_id}'

            # Обновление количества товара
            if quantity_field in request.POST:
                new_quantity = int(request.POST[quantity_field])
                if new_quantity > 0:
                    cart[item_id] = new_quantity
                else:
                    del cart[item_id]  # Удаляем, если количество стало 0

            # Удаление товара из корзины
            if remove_field in request.POST:
                del cart[item_id]

        request.session['cart'] = cart
        return redirect('cart_detail')

    # Если корзина пуста
    if not cart:
        return render(request, 'shop/cart_detail.html', {'products': [], 'total_price': 0})

    # Получаем продукты, которые есть в корзине
    products = Product.objects.filter(id__in=cart.keys())

    # Вычисляем общую стоимость и добавляем в каждый товар итоговую цену
    total_price = 0
    for product in products:
        product.quantity = cart[str(product.id)]
        product.total_price = product.price * product.quantity
        total_price += product.total_price

    return render(request, 'shop/cart_detail.html', {'products': products, 'total_price': total_price})


@require_POST
def cart_add(request, product_id):
    """
    Добавление товара в корзину.
    """
    cart = request.session.get('cart', {})

    # Если товар уже есть в корзине, увеличиваем его количество
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart
    return redirect('cart_detail')


@require_POST
def cart_update(request):
    """
    Обновление количества товара в корзине или удаление товара.
    """
    cart = request.session.get('cart', {})

    for key, value in request.POST.items():
        if key.startswith('quantity_'):
            product_id = key.split('_')[1]
            new_quantity = int(value)

            if new_quantity <= 0:
                del cart[product_id]  # Если количество <= 0, удаляем товар
            else:
                cart[product_id] = new_quantity  # Обновляем количество товара

        elif key.startswith('remove_item_'):
            product_id = key.split('_')[1]
            if product_id in cart:
                del cart[product_id]  # Удаляем товар из корзины

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


# Асинхронное уведомление
def send_order_notification_in_thread(order):
    # Запускаем поток для отправки уведомления в Telegram
    thread = threading.Thread(target=notify_new_order, args=(order,))
    thread.start()


@login_required
def order_create(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('product_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            # Добавляем товары в заказ
            for product_id, quantity in cart.items():
                product = Product.objects.get(pk=product_id)
                order.products.add(product)
            order.save()

            # Очищаем корзину
            request.session['cart'] = {}

            # Логируем создание заказа
            logger.info(f"Создан заказ {order.id} для пользователя {order.user.username}")

            # Отправляем уведомление в Telegram в отдельном потоке
            notify_order_in_thread(order)

            return render(request, 'shop/order_created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'shop/order_create.html', {'form': form})






# @login_required
# def order_create(request):
#     """
#     Страница оформления заказа.
#     После создания заказа вызывается функция отправки уведомления в Telegram.
#     """
#     cart = request.session.get('cart', {})
#     if not cart:
#         return redirect('product_list')
#
#     if request.method == 'POST':
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.user = request.user
#             order.save()
#             # Добавляем товары в заказ.
#             for product_id, quantity in cart.items():
#                 product = Product.objects.get(pk=product_id)
#                 # Если нужно учитывать количество, можно создать промежуточную модель OrderItem.
#                 order.products.add(product)
#             order.save()
#             # Очищаем корзину.
#             request.session['cart'] = {}
#
#             # Отправляем уведомление в Telegram.
#             from bot.telegram_bot import notify_new_order
#             notify_new_order(order)
#
#             return render(request, 'shop/order_created.html', {'order': order})
#     else:
#         form = OrderCreateForm()
#     return render(request, 'shop/order_create.html', {'form': form})

# def product_list(request):
#     """
#     Страница отображения каталога цветов.
#     """
#     products = Product.objects.all()
#     return render(request, 'shop/product_list.html', {'products': products})