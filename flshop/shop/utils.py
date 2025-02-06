# shop/utils.py
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def notify_order_via_http(order):
    """
    Отправка уведомления о новом заказе через Telegram Bot API.
    """
    # Формируем сообщение
    message = f"*Новый заказ* №{order.id} от {order.user.username}\n"
    message += f"Дата заказа: {order.created_at}\n"
    message += "Продукты в заказе:\n"
    # Перебираем все товары заказа
    for product in order.products.all():
        qty = getattr(product, 'quantity', 1)  # если поле quantity установлено временно
        total_price = product.price * qty
        message += f"- {product.name} (x{qty}) - {total_price} ₽\n"
    message += f"\nОбщая сумма заказа: {order.total_price} ₽"

    # URL для отправки запроса к Telegram API
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": settings.TELEGRAM_SUPERADMIN_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            logger.info(f"Уведомление отправлено успешно, статус: {response.status_code}")
        else:
            logger.error(f"Ошибка отправки уведомления, статус: {response.status_code}, ответ: {response.text}")
    except Exception as e:
        logger.error(f"Ошибка отправки уведомления: {e}")
